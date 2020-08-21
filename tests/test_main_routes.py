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


def test_about(client, app):
    response = client.get('/v1/about')
    assert client.get('/v1/about').status_code == 200
    assert 'NCI IDC API' in response.json['message']

def test_help(client,app):
    response = client.get('v1/help/')
    assert response.status_code == 200
    assert "System Documentation" in response.json['data']

def test_oauth2callback(client, app):
    response = client.get('v1/oauth2callback')
    print(response)