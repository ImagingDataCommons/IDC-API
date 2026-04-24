#
# Copyright 2015-2024, Institute for Systems Biology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from builtins import str
import logging
from time import sleep
from uuid import uuid4
import settings
from api.bigquery.service import get_bigquery_service
from api.bigquery.abstract import BigQueryABC

logger = logging.getLogger(__name__)

MAX_INSERT = settings.MAX_BQ_INSERT
BQ_ATTEMPT_MAX = settings.BQ_MAX_ATTEMPTS


class BigQuerySupport(BigQueryABC):

    def __init__(self, project_id, dataset_id, table_id, executing_project=None, table_schema=None):
        # Project which will execute any jobs run by this class
        self.executing_project = executing_project or settings.BIGQUERY_PROJECT_ID
        # Destination project
        self.project_id = project_id
        # Destination dataset
        self.dataset_id = dataset_id
        # Destination table
        self.table_id = table_id
        self.bq_service = get_bigquery_service()
        self.table_schema = table_schema


    def insert_bq_query_job(self, query, parameters=None, write_disposition='WRITE_EMPTY', cost_est=False):

        # Make yourself a job ID
        job_id = str(uuid4())

        # Build your job description
        job_desc = {
            'jobReference': {
                'projectId': self.executing_project,  # This is the project which will *execute* the query
                'jobId': job_id
            },
            'configuration': {
                'query': {
                    'query': query,
                    'priority': 'INTERACTIVE',
                    'useLegacySql': False,
                }
            }
        }

        if parameters:
            job_desc['configuration']['query']['queryParameters'] = parameters

        if self.project_id and self.dataset_id and self.table_id:
            job_desc['configuration']['query']['destinationTable'] = {
                'projectId': self.project_id,
                'datasetId': self.dataset_id,
                'tableId': self.table_id
            }
            job_desc['configuration']['query']['writeDisposition'] = write_disposition

        if cost_est:
            job_desc['configuration']['dryRun'] = True

        return self.bq_service.jobs().insert(
            projectId=self.executing_project,
            body=job_desc).execute(num_retries=5)


    # Keep
    # Runs a basic, optionally parameterized query
    # If self.project_id, self.dataset_id, and self.table_id are set they will be used as the destination table for
    # the query WRITE_DISPOSITION is assumed to be for an empty table unless specified
    def execute_query(self, query, parameters=None, write_disposition='WRITE_EMPTY',
                      cost_est=False, with_schema=False, paginated=False, no_results=False):

        query_job = self.insert_bq_query_job(query,parameters,write_disposition,cost_est)
        logger.debug("query_job: {}".format(query_job))

        job_id = query_job['jobReference']['jobId']

        query_results = None

        # Cost Estimates don't actually run as fully-fledged jobs, and won't be inserted as such,
        # so we just get back the estimate immediately
        if cost_est:
            if query_job['status']['state'] == 'DONE':
                return {
                    'total_bytes_billed': query_job['statistics']['query']['totalBytesBilled'],
                    'total_bytes_processed': query_job['statistics']['query']['totalBytesProcessed']
                }

        job_is_done = self.await_job_is_done(query_job)

        # Parse the final disposition
        if no_results:
            # Just return the job data. Let the caller decide what to do
            query_results = job_is_done
        else:
            if job_is_done and job_is_done['status']['state'] == 'DONE':
                if 'status' in job_is_done and 'errors' in job_is_done['status']:
                    logger.error("[ERROR] During query job {}: {}".format(job_id, str(job_is_done['status']['errors'])))
                    logger.error("[ERROR] Error'd out query: {}".format(query))
                else:
                    logger.info("[STATUS] Query {} done, fetching results...".format(job_id))
                    if paginated:
                        query_results = self.fetch_job_result_page(query_job['jobReference'])
                        logger.info("[STATUS] {} results found for query {}.".format(str(query_results['totalFound']), job_id))
                    elif with_schema:
                        query_results = self.fetch_job_results_with_schema(query_job['jobReference'])
                        logger.info("[STATUS] {} results found for query {}.".format(str(len(query_results['results'])), job_id))
                    else:
                        query_results = self.fetch_job_results(query_job['jobReference'])
                        logger.info("[STATUS] {} results found for query {}.".format(str(len(query_results)), job_id))
            else:
                logger.error("[ERROR] Query took longer than the allowed time to execute--" +
                             "if you check job ID {} manually you can wait for it to finish.".format(job_id))
                logger.error("[ERROR] Timed out query: {}".format(query))

        if 'statistics' in job_is_done and 'query' in job_is_done['statistics'] and 'timeline' in \
                job_is_done['statistics']['query']:
            logger.debug("Elapsed: {}".format(str(job_is_done['statistics']['query']['timeline'][-1]['elapsedMs'])))

        return query_results

    # Keep
    # Check for a job's status for the maximum number of attempts, return the final resulting response
    def await_job_is_done(self, query_job):
        done = self.job_is_done(query_job)
        retries = 0

        while not done and retries < BQ_ATTEMPT_MAX:
            retries += 1
            sleep(1)
            done = self.job_is_done(query_job)

        return self.bq_service.jobs().get(
            projectId=self.executing_project, jobId=query_job['jobReference']['jobId']
        ).execute(num_retries=5)

    # Keep
    # Check to see if query job is done
    def job_is_done(self, query_job):
        job_is_done = self.bq_service.jobs().get(projectId=self.executing_project,
                                                 jobId=query_job['jobReference']['jobId']).execute(num_retries=5)

        return job_is_done and job_is_done['status']['state'] == 'DONE'

    # Keep
    # TODO: shim until we have time to rework this into a single method
    # Fetch the results of a job based on the reference provided
    def fetch_job_result_page(self, job_ref, page_token=None, maxResults=settings.MAX_BQ_RECORD_RESULT):

        page = self.bq_service.jobs().getQueryResults(
            pageToken=page_token,
            maxResults=maxResults,
            **job_ref).execute(num_retries=2)

        schema = page['schema']
        totalFound = page['totalRows']
        next_page = page.get('pageToken')

        return {
            'current_page_rows': page['rows'] if 'rows' in page else [],
            'job_reference': job_ref,
            'schema': schema,
            'totalFound': totalFound,
            'next_page': next_page}

    # Keep
    # TODO: shim until we have time to rework this into a single method
    # Fetch the results of a job based on the reference provided
    def fetch_job_results_with_schema(self, job_ref):
        result = []
        page_token = None
        schema = None
        totalFound = None

        while True:
            page = self.bq_service.jobs().getQueryResults(
                pageToken=page_token,
                **job_ref).execute(num_retries=2)
            if not schema:
                schema = page['schema']
            if int(page['totalRows']) == 0:
                break
            if totalFound is None:
                totalFound = page['totalRows']

            rows = page['rows']
            if len(rows) > settings.MAX_BQ_RECORD_RESULT:
                result.extend(rows[:settings.MAX_BQ_RECORD_RESULT])
            else:
                result.extend(rows)

            if len(result) >= settings.MAX_BQ_RECORD_RESULT:
                break

            page_token = page.get('pageToken')
            if not page_token:
                break

        return {'results': result, 'schema': schema, 'totalFound': totalFound}

    # Keep
    # Fetch the results of a job based on the reference provided
    def fetch_job_results(self, job_ref):
        logger.info(str(job_ref))
        result = []
        page_token = None

        while True:
            page = self.bq_service.jobs().getQueryResults(
                pageToken=page_token,
                **job_ref).execute(num_retries=2)

            if int(page['totalRows']) == 0:
                break

            rows = page['rows']
            result.extend(rows)

            if len(result) > settings.MAX_BQ_RECORD_RESULT:
                break

            page_token = page.get('pageToken')
            if not page_token:
                break

        return result


    @classmethod
    def execute_query_and_fetch_results(cls, query, parameters=None, with_schema=False, paginated=False, no_results=False):
        bqs = cls(None, None, None)
        return bqs.execute_query(query, parameters, with_schema=with_schema, paginated=paginated, no_results=no_results)


    @classmethod
    def wait_for_done(cls, query_job):
        bqs = cls(None, None, None)
        return bqs.await_job_is_done(query_job)


    @classmethod
    def get_job_result_page(cls, job_ref, page_token, maxResults=settings.MAX_BQ_RECORD_RESULT):
        bqs = cls(None, None, None)
        page = bqs.fetch_job_result_page(job_ref, page_token, maxResults=maxResults)
        return page