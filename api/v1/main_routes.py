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
logger = logging.getLogger(settings.LOGGER_NAME)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

main_bp = Blueprint(f'main_bp_{API_VERSION}', __name__, url_prefix='/{}'.format(API_VERSION))
@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
def about():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Documentation is available at <https://learn.canceridc.dev/>'
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
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
