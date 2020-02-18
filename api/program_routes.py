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
from flask import jsonify
from django.conf import settings
from django.db import close_old_connections
from . program_views import get_programs, get_collections, get_collection_info

from flask import Blueprint

program_bp = Blueprint('program_bp', __name__, url_prefix='/v1')

logger = logging.getLogger(settings.LOGGER_NAME)


@program_bp.route('/programs/', methods=['GET'], strict_slashes=False)
def programs():
    """Retrieve the list of programs and builds currently available for cohort creation."""

    response = None
    
    try:
        program_info = get_programs()
        
        if program_info:   
            response = jsonify({
                'code': 200,
                'programs': program_info.text
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the program list.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving program information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the program list.'
        })
        response.status_code = 500
    finally:
        close_old_connections()
        
    return response


@program_bp.route('/programs/<program_name>', methods=['GET'], strict_slashes=False)
def collections(program_name):
    """Retrieve the list of collections and versions in program <program_name>."""
    collections_info = None

    try:

        collections_info = get_collections(program_name)

        if collections_info:
            response = jsonify({
                'code': 200,
                'collections': collections_info.text
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the collection list.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving collection information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the collection list.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response


@program_bp.route('/programs/<program_name>/<collection_name>/', methods=['GET'], strict_slashes=False)
def collection(program_name, collection_name):
    """"Get a list of the available fields for a specific version of a collection."""
    collection_info = None

    try:
        collection_info = get_collection_info(program_name, collection_name)
        if collection_info:
            response = jsonify({
                'code': 200,
                'collection': collection_info.text
            })
            response.status_code = 200
        else:
            response = jsonify({
                'code': 500,
                'message': 'Encountered an error while retrieving the collection list.'
            })
            response.status_code = 500
    except Exception as e:
        logger.error("[ERROR] While retrieving collection information:")
        logger.exception(e)
        response = jsonify({
            'code': 500,
            'message': 'Encountered an error while retrieving the collection metadata.'
        })
        response.status_code = 500
    finally:
        close_old_connections()

    return response

