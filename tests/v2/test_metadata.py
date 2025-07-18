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

from testing_branch import test_branch
from testing_config import VERSION, NUM_COLLECTIONS, API_URL
from testing_utils import  _testMode, get_data
from api.v2.schemas.fields import FIELDS

mimetype = 'application/json'
headers = {
    'Accept': mimetype,
    'Content-Type': mimetype
}

@_testMode
def test_versions(client, app):
    response = client.get(f'{API_URL}/versions',
                          headers=headers)
    assert response.status_code == 200
    data = get_data(response)['versions']
    versions = {version['idc_data_version']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    assert len(versions) == VERSION
    for version in range(1, VERSION+1):
        v = f"{version}.0"
        assert v in versions
        assert versions[v]['active'] == (version == VERSION)


@_testMode
def test_collections(client, app):

    response = client.get(f'{API_URL}/collections')
    assert response.status_code == 200
    data = get_data(response)['collections']
    collections = {collection['collection_id']: \
                   {key: collection[key] for key in collection.keys() if key != 'collection_id'} \
                   for collection in data}
    assert len(collections) == NUM_COLLECTIONS
    assert "tcga_prad" in collections
    collection = collections['tcga_prad']
    assert collection['cancer_type'] == 'Prostate Cancer'
    assert collection['source_doi'].lower() == '10.7937/k9/tcia.2016.yxoglm4y 10.5281/zenodo.12689935 10.5281/zenodo.11099004'.lower()
    assert collection['image_types'] == 'CT, MR, PT, SM, ANN, SEG'
    assert collection['location'] == 'Prostate'
    assert collection['species'] == 'Human'
    assert collection['subject_count'] == 500
    assert collection['supporting_data'] == 'Clinical, Genomics, Histopathology'


@_testMode
def test_analysis_results(client, app):
    response = client.get(f'{API_URL}/analysis_results')
    assert response.status_code == 200
    data = get_data(response)['analysisResults']
    results = {r['title']: \
                   {key: r[key] for key in r.keys() if key != 'description'} \
                   for r in data}
    # assert len(results) == 6
    assert 'Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' in results
    collection = results['Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' ]
    # assert collection['idc_data_versions'] == ['1.0','2.0']
    assert collection['analysisArtifacts'] == 'Tumor segmentations, image features, Software/Source Code'
    assert collection['analysis_result_id'] == 'DICOM-LIDC-IDRI-Nodules'
    assert collection['cancer_type'] == 'Lung Cancer'
    assert collection['collections'].lower() =='lidc_idri'
    # assert collection['date_updated'] == '2016-08-29'
    assert collection['doi'].lower() == '10.7937/TCIA.2018.h7umfurq'.lower()
    assert collection['location'] == 'Chest'
    # assert collection['subject_count'] == 1010

@_testMode
def test_filters(client, app):
    response = client.get(f'{API_URL}/filters')
    assert response.status_code == 200
    data = get_data(response)
    data_sources = data["data_sources"]

    source_name = 'bigquery-public-data.idc_v4.tcga_biospecimen_rel9'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    filters = {filter['name']: {key: filter[key] for key in filter.keys() if key != 'name'} for filter in data_source['filters']}
    assert 'sample_type' in filters
    # assert filters['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert filters['sample_type'] == {'data_type': 'Categorical String', 'units': None}

    source_name = 'bigquery-public-data.idc_v4.tcga_clinical_rel9'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    filters = {filter['name']: {key: filter[key] for key in filter.keys() if key != 'name'} for filter in data_source['filters']}
    assert 'disease_code' in filters
    # assert filters['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert filters['disease_code'] == {'data_type': 'Categorical String', 'units': None}

    # source_name = f'bigquery-public-data.idc_v{VERSION}.dicom_pivot' if test_branch!="LOCAL" else f'idc-dev-etl.idc_v{VERSION}_pub.dicom_pivot'
    try:
        source_name = f'bigquery-public-data.idc_v{VERSION}.dicom_pivot'
        data_source = next(source for source in data_sources if source['data_source'] == source_name)
    except StopIteration:
        source_name = f'idc-dev-etl.idc_v{VERSION}_pub.dicom_pivot'
        data_source = next(source for source in data_sources if source['data_source'] == source_name)

    filters = {filter['name']: {key: filter[key] for key in filter.keys() if key != 'name'} for filter in data_source['filters']}
    assert 'Modality' in filters
    assert filters['Modality'] == {'data_type': 'Categorical String', 'units': None}



@_testMode
def test_categorical_field_values(client, app):
    filter = 'nodality'
    response = client.get(f'{API_URL}/filters/values/{filter}')
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Invalid filter ID'

    filter = 'volume_eq'
    response = client.get(f'{API_URL}/filters/values/{filter}')
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Filter data type is Ranged Number not Categorical String or Categorical Number'

    filter = 'age_at_diagnosis_eq'
    response = client.get(f'{API_URL}/filters/values/{filter}')
    assert response.status_code == 400
    assert get_data(response)['message'] == 'Filter data type is Ranged Integer not Categorical String or Categorical Number'

    filter = 'modality'
    response = client.get(f'{API_URL}/filters/values/{filter}')
    assert response.status_code == 200
    values = get_data(response)['values']
    modalities = set([
        "CR",
        "CT",
        "DX",
        "FUSION",
        "KO",
        "MG",
        "MR",
        "NM",
        "OT",
        "PR",
        "PT",
        "REG",
        "RTDOSE",
        "RTPLAN",
        "RTSTRUCT",
        "RWV",
        "SC",
        "SEG",
        "SM",
        "SR",
        "US",
        "XC"
      ])
    assert modalities - set(values) == set()


    filter = 'race'
    response = client.get(f'{API_URL}/filters/values/{filter}')
    assert response.status_code == 200
    values = get_data(response)['values']
    modalities = set([None, 'AMERICAN INDIAN OR ALASKA NATIVE', 'ASIAN', 'BLACK OR AFRICAN AMERICAN', 'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER', 'WHITE'])
    assert modalities - set(values) == set()

@_testMode
def test_fields(client, app):
    #Test the current version
    response = client.get(f'{API_URL}/fields/{VERSION}.0')
    fields = get_data(response)
    all_fields = set()
    assert fields['idc_data_version'] == f'{VERSION}.0'
    for source in fields['data_sources']:
        all_fields  = all_fields.union(source['fields'])
    assert set(all_fields) == set(FIELDS["properties"]['fields']['items']['enum'])

    # An integer is not a version
    response = client.get(f'{API_URL}/fields/14')
    assert response.status_code == 400
    assert get_data(response)['message'] == "Supplied idc_data_version '14' is invalid. Query the /versions endpoint for defined versions."

    # No arbitrary strings
    response = client.get(f'{API_URL}/fields/foo')
    assert response.status_code == 400
    assert get_data(response)['message'] == "Supplied idc_data_version 'foo' is invalid. Query the /versions endpoint for defined versions."

    # The empty string is an error
    response = client.get(f'{API_URL}/fields/')
    if test_branch=="LOCAL":
        assert response.status_code == 400
        assert get_data(response)['message'] == 'No version was provided'
    else:
        assert response.status_code == 404
        assert get_data(response)['message'] == "Method does not exist."

    # Leading whitespace is an error
    response = client.get(f'{API_URL}/fields/ 17.0')
    assert response.status_code == 400
    assert get_data(response)['message'] == "Supplied idc_data_version ' 17.0' is invalid. Query the /versions endpoint for defined versions."

    # 'current' gets tjhe current version
    response = client.get(f'{API_URL}/fields/current')
    fields = get_data(response)
    assert fields['idc_data_version'] == f'{VERSION}.0'
    all_fields = set()
    for source in fields['data_sources']:
        all_fields  = all_fields.union(source['fields'])
    assert set(all_fields) == set(FIELDS["properties"]['fields']['items']['enum'])

    # Returns something for each version
    response = client.get(f'{API_URL}/versions',
                          headers=headers)
    data = get_data(response)['versions']
    versions = {version['idc_data_version']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    for version in versions:
        response = client.get(f'{API_URL}/fields/{version} ')
        assert response.status_code == 200
        fields = get_data(response)
        assert fields['idc_data_version'] == version
        print(f'Version: {version}')
        for source in fields['data_sources']:
            print(f"\t{source['data_source']}")
            n=1
            for field in source['fields']:
                print(f'\t\t{n} {field}')
                n+=1


