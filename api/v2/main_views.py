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
import os
import requests

from python_settings import settings

logger = logging.getLogger(__name__)


def get_privacy():
    try:
        result = requests.get("{}/{}".format(settings.BASE_URL, 'privacy/'))
    except:
        if result.status_code != 200:
           raise Exception("oops!")
    return result

def get_help():
    try:
        result = requests.get("{}/{}".format(settings.BASE_URL, 'help/'))
    except:
        if result.status_code != 200:
           raise Exception("oops!")
    return result


