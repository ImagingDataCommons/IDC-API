#
# Copyright 2020, Institute for Systems Biology
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

import json
# from settings import API_VERSION
from testing_config import VERSIONS, API_VERSION
from api.v1.schemas.filters import COHORT_FILTERS_SCHEMA

levels = ["collections", "patients", "studies", "series", "instances"]


def gen_query(filter_set, query_string):
    schema = {
    }
    for filter, value in COHORT_FILTERS_SCHEMA['properties'].items():
        schema[filter.lower()] = value

    query = f"""
SELECT DISTINCT @fields
FROM `idc-dev-etl.idc_v{VERSIONS}_pub.dicom_pivot{'_v'+VERSIONS if VERSIONS < 15 else ''}` da
LEFT JOIN `idc-dev-etl.idc_v{VERSIONS}_pub.tcga_clinical_rel9` tc
ON da.PatientID = tc.case_barcode
WHERE @filters
            """
    fields = [key for key, value in query_string.items() if value in [True,'True'] and \
                        key not in ['sql', 'Patient_ID', 'CRDC_Instance_GUID', 'CRDC_Series_GUID', 'CRDC_Study_GUID']]
    if 'CRDC_Instance_GUID' in query_string.keys():
        fields.append(f"CONCAT('dg.4DFC/', crdc_instance_uuid) CRDC_Instance_GUID")
    if 'CRDC_Series_GUID' in query_string.keys():
        fields.append(f"CONCAT('dg.4DFC/', crdc_Series_uuid) CRDC_Series_GUID")
    if 'CRDC_Study_GUID' in query_string.keys():
        fields.append(f"CONCAT('dg.4DFC/', crdc_study_uuid) CRDC_Study_GUID")
    if 'Patient_ID' in query_string.keys():
        fields.append('PatientID Patient_ID')
    fields = ", ".join(fields)

    query = query.replace('@fields', fields)
    filters = []
    for filter, value in filter_set.items():
        try:
            property = schema[filter.lower()]
            if property["items"]["type"] == "number":
                try:
                    suffix = filter.split('_')[-1]
                    op = filter.rsplit('_',1)[0]
                except:
                    suffix = ''
                    op = filter
                if suffix == '':
                    filters.append(f'({op} = {value[0]})' )
                elif suffix in ['lt', 'lte']:
                    filters.append( f'({op} <= {value[0]})')
                elif suffix in ['btw', 'ebtw', 'ebtwe', 'btwe']:
                    filters.append(f'({op} BETWEEN {value[0]} AND {value[1]})')
                elif suffix == 'lte':
                    filters.append(f'({op} <= {value[0]})')
                else:
                    filters.append(f'({op} < {value[0]})')
            else:
                # filters.append(f"{filter} in [{','.join([v for v in value])}]")
                if filter.lower() == 'collection_id':
                    for x, v in enumerate(value):
                        value[x] = v.lower().replace('-','_').replace(' ','_')
                filters.append(f"(lower({filter}) in {str(value).lower()})".replace('[', '(').replace(']',')'))
        except Exception as exc:
            print(f'{exc}')
    query = query.replace('@filters', '\nAND '.join(filters))
    return query

def pretty_print_cohortObjects(cohortObjects, indent=4):
    print(json.dumps(cohortObjects, sort_keys=True, indent=indent))

# This routine merges results from the /cohorts/{cohort_id} API with previously obtained results.
# It is intended for use when that API is used in a paged manner.
def merge(src, dst, level):
    keys = ["collection_id", "patient_id", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    for src_item in src:
        found = False
        for dst_item in dst:
            # if src_item["id"] == dst_item["id"]:
            if src_item[keys[level]] == dst_item[keys[level]]:
                if not len(levels) == level+1:
                    merge(src_item[levels[level+1]], dst_item[levels[level+1]], level+1)
                found = True
                break
        if not found:
            dst.append(src_item)

 # Utility to create a "standard" cohort for testing
def create_cohort(client):
    # Define the filters
    filters = {
        "collection_id": ["tcga_luad", "tcga_kirc"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']

    return cohortResponse, cohortSpec


# Create a cohort with filter as expected by the test_get_cohort_xxx() functions
def create_cohort_for_test_get_cohort_xxx(client, filters=None):
    # Create a cohort to test against
    if not filters:
        filters = {
            "collection_id": ["TCGA-READ"],
            "Modality": ["CT", "MR"],
            "race": ["WHITE"]
        }

        cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']
    id = cohortResponse['cohort_id']
    return (id, cohortSpec)


# Find a previously created V1 cohort with filter expected by the test_get_cohort_xxx() functions
def find_v1_cohort_for_test_get_cohort_xxx(client, filterset):

    # Get a list of existing cohorts
    response = client.get("{}/".format('v1/cohorts'))
    cohorts = response.json['cohorts']

    for cohort in cohorts:
        # if cohort["filterSet"]["filters"] == filters and cohort["filterSet"]['idc_data_version'] == '1.0':
        if cohort["filterSet"] == filterset:
                return (cohort['cohort_id'], cohort["filterSet"])

    # Didn't find a matching cohort
    return(-1, -1)

# Create a big cohort with filter as expected by the test_get_cohort_xxx() functions
def create_big_cohort_for_test_get_cohort_xxx(client):
    # Create a cohort to test against
    filters = {
        "collection_id": ["tcga_luad"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filters": filters}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(f'/{API_VERSION}/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.status_code == 200
    cohortResponse = response.json['cohort_properties']
    id = cohortResponse['cohort_id']
    return (id, filters)

# Find a previously created V1 cohort with filter expected by the test_get_cohort_xxx() functions
def find_v1_big_cohort_for_test_get_cohort_xxx(client):
    filters = {
        "collection_id": ["tcga_luad"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]
    }

    # Get a list of existing cohorts
    response = client.get("{}/".format('v1/cohorts'))
    cohorts = response.json['cohorts']

    for cohort in cohorts:
        if cohort["filterSet"]["filters"] == filters and cohort["filterSet"]['idc_data_version'] == '1.0':
            return (cohort['cohort_id'], cohort["filterSet"])

    # Didn't find a matching cohort
    return(-1, -1)

# Utility to delete an existing cohort
def delete_cohort(client, id):
    response = client.delete(f"{API_VERSION}/cohorts/{id}/")
    assert response.content_type == 'application/json'
    assert response.status_code == 200

def current_version(client):
    response = client.get(f'/{API_VERSION}/versions')
    data = response.json['versions']
    current = str(max([float(v['idc_data_version']) for v in data]))
    return current




