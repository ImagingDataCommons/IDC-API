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

main_bp = Blueprint(f'main_bp_{API_VERSION}', __name__, url_prefix='/{}'.format(API_VERSION))

@main_bp.route('/about/', methods=['GET'], strict_slashes=False)
def about():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response

@main_bp.route('/versions/', methods=['GET'], strict_slashes=False)
def versions():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/collections/', methods=['GET'], strict_slashes=False)
def collections():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/analysis_results/', methods=['GET'], strict_slashes=False)
def analysis_results():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/attributes/', methods=['GET'], strict_slashes=False)
def attributes():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/', methods=['GET'], strict_slashes=False)
def cohorts():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/manifest/', methods=['GET'], strict_slashes=False)
def cohortsmanifest():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/manifest/preview/', methods=['GET'], strict_slashes=False)
def cohortsmanifestpreview():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/manifest/nextPage/', methods=['GET'], strict_slashes=False)
def cohortsmanifestnextPage():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/query/', methods=['GET'], strict_slashes=False)
def cohortsquery():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response


@main_bp.route('/cohorts/query/preview/', methods=['GET'], strict_slashes=False)
def cohortsquerypreview():
    response = jsonify({
        'code': 410,
        'message': 'IDC v1 API endpoints have been deprecated',
        'documentation': 'SwaggerUI interface available at <{}/{}/swagger/>.'.format(settings.BASE_API_URL, 'v1') +
                         ' Historical documentation available at <https://learn.canceridc.dev/api/v1-api/>'
    })
    response.status_code = 410
    return response

# Swagger UI
@main_bp.route('/swagger/', methods=['GET'], strict_slashes=False)
def swagger():
    return render_template('swagger/index.html')


# # @main_bp.route('/oauth2callback/', strict_slashes=False)
def oauth2callback():
    return render_template('swagger/oauth2-redirect.html')
