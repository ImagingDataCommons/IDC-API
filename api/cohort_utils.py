#
# Copyright 2015-2019, Institute for Systems Biology
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
from __future__ import absolute_import

import logging
import re
import json
import requests

from .auth import get_auth

from django.conf import settings
# from idc_collections.models import ImagingDataCommonsVersion
# from idc_collections.collex_metadata_utils import get_bq_metadata, get_bq_string
from google_helpers.bigquery.bq_support import BigQuerySupport


logger = logging.getLogger('main_logger')
BLACKLIST_RE = settings.BLACKLIST_RE

def submit_BQ_job(sql_string, params):
    results = BigQuerySupport.execute_query_and_fetch_results(sql_string, params, no_results=True)
    return results

def build_collections(objects, dois, urls):
    collections = []
    for collection in objects:
        patients = build_patients(collection, objects[collection], dois, urls)
        collections.append(
            {
                "collection_id":collection,
            }
        )
        if len(patients) > 0:
            collections[-1]["patients"] = patients
    return collections


def build_patients(collection,collection_patients, dois, urls):
    patients = []
    for patient in collection_patients:
        studies = build_studies(collection, patient, collection_patients[patient], dois, urls)
        patients.append({
                "patient_id":patient,
            }
        )
        if len(studies) > 0:
            patients[-1]["studies"] = studies
    return patients


def build_studies(collection, patient, patient_studies, dois, urls):
    studies = []
    for study in patient_studies:
        series = build_series(collection, patient, study, patient_studies[study], dois, urls)
        studies.append(
            {
                "StudyInstanceUID": study
            })
        if dois:
            studies[-1]["GUID"] = ""
        if urls:
            studies[-1]["AccessMethods"] = [
                    {
                        "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}".format(collection,study),
                        "region": "Multi-region",
                        "type": "gs"
                    }
            ]
        if len(series) > 0:
            studies[-1]["series"] = series
    return studies


def build_series(collection, patient, study, patient_studies, dois, urls):
    series = []
    for aseries in patient_studies:
        instances = build_instances(collection, patient, study, aseries, patient_studies[aseries], dois, urls)
        series.append(
            {
                "SeriesInstanceUID": aseries
            })
        if dois:
            series[-1]["GUID"] = ""
        if urls:
            series[-1]["AccessMethods"] = [
                {
                    "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}/{}".format(collection,
                                    study, aseries),
                    "region": "Multi-region",
                    "type": "gs"
                }
            ]
        if len(instances) > 0:
            series[-1]["instances"] = instances
    return series


def build_instances(collection, patient, study, series, study_series, dois, urls):
    instances = []
    for instance in study_series:
        instances.append(
            {
                "SOPInstanceUID": instance
            })
        if dois:
            instances[-1]["GUID"] = ""
        if urls:
            instances[-1]["AccessMethods"] = [
                {
                    "access_url": "gs://gcs-public-data--healthcare-tcia-{}/dicom/{}/{}/{}.dcm".format(collection,
                                    study,series,instance),
                    "region": "Multi-region",
                    "type": "gs"
                }
            ]
    return instances


def build_hierarchy(objects, rows, return_level, reorder):
#
    for raw in rows:
        rawv = [val['v'] for val in raw['f']]
        row = [rawv[i] for i in reorder]
        row[0] = row[0].replace('_','-')
        if not row[0] in objects:
            objects[row[0]] = {}
        if return_level == 'Collection':
            continue
        if not row[1] in objects[row[0]]:
            objects[row[0]][row[1]] = {}
        if return_level == 'Patient':
            continue
        if not row[2] in objects[row[0]][row[1]]:
            objects[row[0]][row[1]][row[2]] = {}
        if return_level == 'Study':
            continue
        if not row[3] in objects[row[0]][row[1]][row[2]]:
            objects[row[0]][row[1]][row[2]][row[3]] = []
        if return_level == 'Series':
            continue
        if not row[4] in objects[row[0]][row[1]][row[2]][row[3]]:
            # objects[row[0]][row[1]][row[2]][row[3]][row[4]] = {}
            objects[row[0]][row[1]][row[2]][row[3]].append(row[4])
    return objects


def get_objects(return_level, cohort_info, maxResults):

    levels = {'Instance': ['collection_id', 'PatientID', 'StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID'],
              'Series': ['collection_id', 'PatientID', 'StudyInstanceUID', 'SeriesInstanceUID'],
              'Study': ['collection_id', 'PatientID', 'StudyInstanceUID'],
              'Patient': ['collection_id', 'PatientID'],
              'Collection': ['collection_id'],
              'None': []
              }

    return_level = return_level
    select = levels[return_level]

    objects = {}

    if return_level:
        results = BigQuerySupport.get_job_result_page(job_ref=cohort_info['job_reference'], page_token=cohort_info['next_page'], maxResults=maxResults)
        rowsReturned = len(results["current_page_rows"])

        # Create a list of the fields in the returned schema
        fields = [field['name'] for field in results['schema']['fields']]
        # Build a list of indices into fields that tells build_hierarchy how to reorder
        reorder = [fields.index(x) for x in select]

        # rows holds the actual data
        rows = results['current_page_rows']

        # We first build a tree of just the object IDS: collection_ids, PatientIDs, StudyInstanceUID,...
        objects = build_hierarchy(
            objects=objects,
            rows=rows,
            reorder=reorder,
            return_level=return_level)

        # Then we add the details such as DOI, URL, etc. about each object
        # dois = request.GET['return_DOIs'] in ['True', True]
        # urls = request.GET['return_URLs'] in ['True', True]
        dois = False
        urls = False
        collections = build_collections(objects, dois, urls)

        cohort_info["cohortObjects"] = {
            "totalFound": int(results['totalFound']),
            "rowsReturned": rowsReturned,
            "collections": collections,
        }
        cohort_info['next_page'] = results['next_page']

    return cohort_info


def get_manifest(request, func, url, data=None, user=None):
    blacklist = re.compile(BLACKLIST_RE, re.UNICODE)
    manifest_info = None

    path_params = {
        "sql": False,
        "Collection_IDs": False,
        "Patient_IDs": False,
        "StudyInstanceUIDs": False,
        "SeriesInstanceUIDs": False,
        "SOPInstanceUIDs": False,
        "Collection_DOIs": False,
        "access_method": "doi",
    }

    if user:
        path_params["email"] = user

    local_params = {
        "format": "json",
        "job_reference": None,
        "next_page": "",
        "page_size": 10000
    }

    access_methods = ["url", "doi"]
    formats = ['json', 'csv', 'tsv']

    # Get and validate parameters
    for key in request.args.keys():
        match = blacklist.search(str(key))
        if match:
            return dict(
                message = "Key {} contains invalid characters; please edit and resubmit. " +
                           "[Saw {}]".format(str(key, match)),
                code = 400
            )
        if key in path_params:
            path_params[key] = request.args.get(key)
        elif key in local_params:
            local_params[key] = request.args.get(key)

        else:
            manifest_info = dict(
                message="Invalid key {}".format(key),
                code=400
            )
            return manifest_info

    local_params['page_size'] = int(local_params['page_size'])
    for s in ['sql', 'Collection_IDs', 'Patient_IDs', 'StudyInstanceUIDs',
              'SeriesInstanceUIDs', 'SOPInstanceUIDs', 'Collection_DOIs']:
        if s in path_params:
            path_params[s] = path_params[s] in [True, 'True']
    if path_params["access_method"] not in access_methods:
        return dict(
            message = "Invalid access_method {}".format(path_params['access_method']),
            code = 400
        )
    if local_params["format"] not in formats:
        return dict(
            message = "Invalid format {}".format(path_params['format']),
            code = 400
        )
    if manifest_info == None:

        try:
            if local_params["job_reference"] and local_params['next_page']:
                job_reference = json.loads(local_params["job_reference"].replace("'",'"'))
                # We don't return the project ID to the user
                job_reference['projectId'] = settings.BIGQUERY_PROJECT_ID
                next_page = local_params['next_page']
                manifest_info = dict(
                    cohort = {},
                    job_reference = job_reference,
                    next_page = next_page
                )
            else:
                auth = get_auth()
                if func == requests.post:
                    results = func(url, params=path_params, json=data, headers=auth)
                else:
                    results = func(url, params=path_params, headers=auth)

                manifest_info = results.json()

                if "message" in manifest_info:
                    return manifest_info

                # Start the BQ job, but don't get any data results, just the job info.
                job_is_done = submit_BQ_job(manifest_info['query']['sql_string'],
                                            manifest_info['query']['params'])
                if job_is_done and job_is_done['status']['state'] == 'DONE':
                    if 'status' in job_is_done and 'errors' in job_is_done['status']:
                        job_id = job_is_done['jobReference']['jobId']
                        logger.error("[ERROR] During query job {}: {}".format(job_id, str(
                            job_is_done['status']['errors'])))
                        logger.error("[ERROR] Error'd out query: {}".format(manifest_info['query']['sql_string']))
                        return dict(
                            message="[ERROR] During query job {}: {}".format(job_id, str(
                                job_is_done['status']['errors'])),
                            code=500)
                    else:
                        manifest_info['job_reference'] = job_is_done['jobReference']
                else:
                    logger.error("[ERROR] API query took longer than the allowed time to execute. " +
                                 "Retry the query.")
                    logger.error("[ERROR] Timed out on query: {}".format(manifest_info['query']['sql_string']))
                    return dict(
                        message="[ERROR] API query took longer than the allowed time to execute. " +
                                "Retry the query",
                        code=503)

                print(("[STATUS] manifest_info with job_ref: {}").format(manifest_info))

                # Don't return the query in this form
                manifest_info.pop('query')

                # job_reference = cohort_data['job_reference']
                manifest_info['next_page'] = None

            manifest_info = get_job_results(manifest_info,
                                maxResults=local_params['page_size'], format=local_params['format'],
                                first=local_params['next_page'] in [None,''])
            # We don't return the project ID to the user
            manifest_info['job_reference'].pop('projectId')

        except Exception as e:
            logger.exception(e)
            manifest_info = dict(
                message='[ERROR] get_manifest(): Error trying to preview a cohort',
                code=400)

    return manifest_info


# Get a list of GCS URLs or CRDC DOIs of the instances in the cohort
def get_job_results(manifest_info, maxResults, format, first):

    results = BigQuerySupport.get_job_result_page(job_ref=manifest_info['job_reference'],
                                                  page_token=manifest_info['next_page'], maxResults=maxResults)
    manifest_info['next_page'] = results['next_page']

    schema_names = ['doi' if field['name'] == 'crdc_instance_uuid' else 'url' if field['name'] == 'gcs_url' else field['name'] for field in results['schema']['fields']]

    manifest_info["manifest"] = dict(
                totalFound = int(results['totalFound']),
                rowsReturned = len(results["current_page_rows"])
    )
    rows = form_rows_json(results['current_page_rows'], schema_names)
    manifest_info["manifest"]['json_manifest'] = rows

    # rowsReturned = len(results["current_page_rows"])
    return manifest_info


def form_rows_json(data, schema_names):
    rows = []
    for row in data:
        row_vals = [ val['v'] for val in row['f']]
        rows.append(dict(zip(schema_names,row_vals)))

    return rows


def form_rows_csv(data, schema_names, first):
    rows = []
    if first:
        rows.append(','.join(schema_names))
    for row in data:
        rows.append(','.join([val['v'] for val in row['f']]))
    table = '\n'.join(rows)

    return table


def form_rows_tsv(data, schema_names, first):
    rows = []
    if first:
        rows.append('\t'.join(schema_names))
    for row in data:
        rows.append('\t'.join([val['v'] for val in row['f']]))
    table = '\n'.join(rows)

    return table

