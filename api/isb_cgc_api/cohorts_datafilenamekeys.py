"""

Copyright 2015, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import endpoints
import logging
import MySQLdb
import django

from django.conf import settings
from django.core.signals import request_finished
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, are_there_bad_keys, construct_parameter_error_message
from api.api_helpers import sql_connection
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class CohortsFilesQueryBuilder(object):

    def build_query(self, platform=None, pipeline=None, limit=None):

        query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                    'FROM metadata_data ' \
                    'JOIN cohorts_samples ON metadata_data.SampleBarcode=cohorts_samples.sample_id ' \
                    'WHERE cohorts_samples.cohort_id=%s ' \
                    'AND DataFileNameKey != "" AND DataFileNameKey is not null '

        query_str += ' and metadata_data.Platform=%s ' if platform is not None else ''
        query_str += ' and metadata_data.Pipeline=%s ' if pipeline is not None else ''

        query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository '
        query_str += ' LIMIT %s' if limit is not None else ' LIMIT 10000'

        return query_str


class DataFileNameKeyList(messages.Message):
    datafilenamekeys = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


@ISB_CGC_Endpoints.api_class(resource_name='cohorts')
class CohortsDatafilenamekeysAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(cohort_id=messages.IntegerField(1, required=True),
                                               limit=messages.IntegerField(2),
                                               platform=messages.StringField(3),
                                               pipeline=messages.StringField(4))

    @endpoints.method(GET_RESOURCE, DataFileNameKeyList,  http_method='GET',
                      path='cohorts/{cohort_id}/datafilenamekeys')
    def datafilenamekeys(self, request):
        """
        Takes a cohort id as a required parameter and returns cloud storage paths to files
        associated with all the samples in that cohort, up to a default limit of 10,000 files.
        Authentication is required. User must have READER or OWNER permissions on the cohort.
        """
        user_email = None
        cursor = None
        db = None

        limit = request.get_assigned_value('limit')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')
        cohort_id = request.get_assigned_value('cohort_id')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        if endpoints.get_current_user() is not None:
            user_email = endpoints.get_current_user().email()

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register with the web application."
                    .format(BASE_URL))

        django.setup()

        try:
            user_id = Django_User.objects.get(email=user_email).id
            django_cohort = Django_Cohort.objects.get(id=cohort_id)
            cohort_perm = Cohort_Perms.objects.get(cohort_id=cohort_id, user_id=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            err_msg = "Error retrieving cohort {} for user {}: {}".format(cohort_id, user_email, e)
            if 'Cohort_Perms' in e.message:
                err_msg = "User {} does not have permissions on cohort {}. Error: {}" \
                    .format(user_email, cohort_id, e)
            request_finished.send(self)
            raise endpoints.UnauthorizedException(err_msg)

        query_str = CohortsFilesQueryBuilder().build_query()

        query_tuple = (cohort_id,)
        if platform is not None: query_tuple += (platform,)
        if pipeline is not None: query_tuple += (pipeline,)
        if limit is not None: query_tuple += (limit,)

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            datafilenamekeys = []
            bad_repo_count = 0
            bad_repo_set = set()
            for row in cursor.fetchall():
                if not row.get('DataFileNameKey'):
                    continue

                if 'controlled' not in str(row['SecurityProtocol']).lower():
                    # this may only be necessary for the vagrant db
                    path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                        else row.get('DataFileNameKey').replace('gs://' + settings.OPEN_DATA_BUCKET, '')
                    datafilenamekeys.append(
                        "gs://{}{}".format(settings.OPEN_DATA_BUCKET, path))
                else:  # not filtering on dbGaP_authorized
                    if row['Repository'].lower() == 'dcc':
                        bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                    elif row['Repository'].lower() == 'cghub':
                        bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                    else:  # shouldn't ever happen
                        bad_repo_count += 1
                        bad_repo_set.add(row['Repository'])
                        continue
                    # this may only be necessary for the vagrant db
                    path = row.get('DataFileNameKey') if row.get('DataFileNameKey') is None \
                        else row.get('DataFileNameKey').replace('gs://' + bucket_name, '')
                    datafilenamekeys.append("gs://{}{}".format(bucket_name, path))
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return DataFileNameKeyList(datafilenamekeys=datafilenamekeys, count=len(datafilenamekeys))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for cohort {} not found.".format(cohort_id))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\t query: {} {}'.format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)