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
from testing_config import VERSIONS, API_VERSION, NUM_COLLECTIONS
from api.v1.schemas.queryfields import QUERY_FIELDS


def test_versions(client, app):
    response = client.get(f'/{API_VERSION}/versions')
    assert response.status_code == 200
    data = response.json['versions']
    versions = {version['idc_data_version']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    assert len(versions) == VERSIONS
    for version in range(1, VERSIONS+1):
        v = f"{version}.0"
        assert v in versions
        assert versions[v]['active'] == (version == VERSIONS)


def test_collections(client, app):

    response = client.get(f'/{API_VERSION}/collections')
    assert response.status_code == 200
    data = response.json['collections']
    collections = {collection['collection_id']: \
                   {key: collection[key] for key in collection.keys() if key != 'collection_id'} \
                   for collection in data}
    assert len(collections) == NUM_COLLECTIONS
    assert "tcga_prad" in collections
    collection = collections['tcga_prad']
    assert collection['cancer_type'] == 'Prostate Cancer'
    # assert collection['description'] == '<p>The <a href="http://imaging.cancer.gov/" target="_blank"><u>Cancer Imaging Program (CIP)</u></a> is working directly with primary investigators from institutes participating in TCGA to obtain and load images relating to the genomic, clinical, and pathological data being stored within the <a href="http://tcga-data.nci.nih.gov/" target="_blank">TCGA Data Portal</a>.&nbsp;Currently this image collection of prostate adenocarcinoma (PRAD) patients can be matched by each unique case identifier with the extensive gene and expression data of the same case from The Cancer Genome Atlas Data Portal to research the link between clinical phenome and tissue genome.<br /><br /></p>\n <p>Please see the <a href="https://doi.org/10.7937/K9/TCIA.2016.YXOGLM4Y" target="_blank">TCGA-PRAD</a> page to learn more about the images and to obtain any supporting metadata for this collection.</p>\n'
    assert '10.7937/K9/TCIA.2016.YXOGLM4Y'.lower() in collection['doi'].lower()
    assert collection['image_types'] == 'CT, MR, PT, SM, ANN, SEG'
    assert collection['location'] == 'Prostate'
    assert collection['species'] == 'Human'
    assert collection['subject_count'] == 500
    assert collection['supporting_data'] == 'Clinical, Genomics, Histopathology'


def test_analysis_results(client, app):
    response = client.get(f'/{API_VERSION}/analysis_results')
    assert response.status_code == 200
    data = response.json['analysisResults']
    results = {r['description']: \
                   {key: r[key] for key in r.keys() if key != 'description'} \
                   for r in data}
    # assert len(results) == 6
    assert 'Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' in results
    collection = results['Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' ]
    # assert collection['idc_data_versions'] == ['1.0','2.0']
    assert collection['analysisArtifacts'] == 'Tumor segmentations, image features, Software/Source Code'
    assert collection['cancer_type'] == 'Lung Cancer'
    assert collection['collections'].lower() =='lidc_idri'
    # assert collection['date_updated'] == '2016-08-29'
    assert collection['doi'].lower() == '10.7937/TCIA.2018.h7umfurq'.lower()
    assert collection['location'] == 'Chest'
    assert collection['subject_count'] == 875


def test_attributes(client, app):

    # query_string = dict(
    #     # idc_data_version = f'{v}.0',
    #     data_source = f'idc-dev-etl.idc_v4.dicom_pivot_v4'
    # )
    # response = client.get('/v1/attributes',
    #                       query_string = query_string)

    response = client.get('/v1/attributes')
    assert response.status_code == 200
    data = response.json
    data_sources = data["data_sources"]

    # source_name = f'bigquery-public-data.idc_v{VERSIONS}.dicom_pivot'
    source_name = f'idc-dev-etl.idc_v{VERSIONS}_pub.dicom_pivot'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'Modality' in attributes
    assert attributes['Modality'] == {'active': True, 'data_type': 'Categorical String', 'units': None}

    # query_string = dict(
    #     # idc_data_version=f'{v}.0',
    #     data_source = 'isb-cgc.TCGA_bioclin_v0.Biospecimen'
    # )
    # response = client.get('/v1/attributes',
    #                       query_string = query_string)
    # assert response.status_code == 200
    # data = response.json['data_sources']

    source_name = 'bigquery-public-data.idc_v4.tcga_biospecimen_rel9'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'sample_type' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['sample_type'] == {'active': True, 'data_type': 'Categorical String', 'units': None}

    # query_string = dict(
    #     # idc_data_version=f'{v}.0',
    #     data_source = 'isb-cgc.TCGA_bioclin_v0.clinical_v1_1'
    # )
    # response = client.get('/v1/attributes',
    #                       query_string = query_string)
    # assert response.status_code == 200
    # data = response.json['data_sources']

    source_name = 'bigquery-public-data.idc_v4.tcga_clinical_rel9'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'disease_code' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['disease_code'] == {'active': True, 'data_type': 'Categorical String', 'units': None}



# def test_queryFields(client, app):
#     response = client.get(f'/{API_VERSION}/queryFields')
#     assert response.status_code == 200
#     fields = response.json
#
#     assert set(fields['queryFields']) == set(QUERY_FIELDS["properties"]['fields']['items']['enum'])