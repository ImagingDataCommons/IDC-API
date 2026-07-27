# 
# Copyright 2019, Institute for Systems Biology
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


import logging
from flask import jsonify, render_template
from python_settings import settings
from flask import Blueprint
from .version_config import API_VERSION
logger = logging.getLogger(__name__)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

main_bp = Blueprint(f'main_bp_{API_VERSION}', __name__, url_prefix='/{}'.format(API_VERSION))
@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
@main_bp.route('/collections/', methods=['GET'], strict_slashes=False)
@main_bp.route('/analysis_results/', methods=['GET'], strict_slashes=False)
@main_bp.route('/filters', methods=['GET'], strict_slashes=False)
@main_bp.route('/filters/values/<string:filter_id>', methods=['GET'], strict_slashes=False)
@main_bp.route('/fields/', methods=['GET'], strict_slashes=False, defaults={'version': ''})
@main_bp.route('/fields/<string:version>', methods=['GET'], strict_slashes=False)
@main_bp.route('/cohorts/manifest/preview', methods=['GET'], strict_slashes=False)
@main_bp.route('/cohorts/manifest/preview/nextPage', methods=['GET'], strict_slashes=False)
def about():
    response = jsonify({
        'code': 410,
        'message': 'IDC v2 API endpoints have been deprecated',
        'documentation': 'The IDC v2 API has been deprecated, and replaced by the IDC v3 API' +
                         'See https://learn.canceridc.dev/api/api> for details of the IDC v3 API'
    })
    response.status_code = 410
    return response


# Swagger UI
@main_bp.route('/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    return render_template('swagger/index.html')


# @main_bp.route('/oauth2callback/', strict_slashes=False)
def oauth2callback():
    return render_template('swagger/oauth2-redirect.html')
