import json
import base64
import logging
import urllib

from google.appengine.api import urlfetch
import settings

from bq_data_access.data_access import get_feature_vector
from bq_data_access.feature_value_types import ValueType
from bq_data_access.utils import VectorMergeSupport


class PairwiseInputVector(object):
    def __init__(self, feature_id, value_type, data):
        self.feature_id = feature_id
        self.value_type = value_type
        self.data = data


class Pairwise(object):
    def __init__(self):
        pass

    @classmethod
    def prepare_features(self, cohort_id, features):
        # Get the feature data
        feature_vector_mapping = {}
        vectors = []
        for feature in features:
            value_type, vector = get_feature_vector(feature, cohort_id)

            if value_type == ValueType.INTEGER or value_type == ValueType.FLOAT:
                value_type = "N"
            elif value_type == ValueType.STRING:
                value_type = "C"
            else:
                value_type = "B"

            feature_vector_mapping[feature] = (value_type, vector)
            vectors.append(vector)

        # Create merged feature vectors
        vms = VectorMergeSupport('NA', 'sample_id', row_ids=features)

        for feature in feature_vector_mapping.keys():
            vms.add_dict_array(feature_vector_mapping[feature][1], feature, 'value')

        merged = vms.get_merged_dict()

        rows = []

        for feature in feature_vector_mapping.keys():
            current_row = [feature_vector_mapping[feature][0] + ":" + feature]

            for item in merged:
                current_row.append(item[feature])

            rows.append("\t".join(current_row))

        return rows

    @classmethod
    def prepare_feature_vector(self, input_vectors):
        feature_vector_mapping = {}
        vectors = []
        for item in input_vectors:
            feature_id, value_type, vector = item.feature_id, item.value_type, item.data
            if value_type == ValueType.INTEGER or value_type == ValueType.FLOAT:
                value_type = "N"
            elif value_type == ValueType.STRING:
                value_type = "C"
            else:
                value_type = "B"

            feature_vector_mapping[feature_id] = (value_type, vector)
            vectors.append(vector)

        # Create merged feature vectors
        feature_ids = [v.feature_id for v in input_vectors]

        vms = VectorMergeSupport('NA', 'sample_id', row_ids=feature_ids)

        for feature in feature_vector_mapping.keys():
            vms.add_dict_array(feature_vector_mapping[feature][1], feature, 'value')

        merged = vms.get_merged_dict()

        rows = []

        for feature in feature_vector_mapping.keys():
            current_row = [feature_vector_mapping[feature][0] + ":" + feature]

            for item in merged:
                current_row.append(item[feature])

            rows.append("\t".join(current_row))

        return rows

    @classmethod
    def run_pairwise(self, feature_rows):
        url = settings.get('PAIRWISE_SERVICE_URL')

        data_dict = {}
        row_count = 1
        for row in feature_rows:
            label = "row_{count}".format(count=row_count)
            data_dict[label] = row
            row_count += 1

        # Encode the data to be sent to the service
        data = urllib.urlencode(data_dict)
        decoded_response = None

        try:
            pairwise_response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST)
        except Exception as e:
            # TODO: Log error details
            logging.exception(e)
        else:
            # Return the response
            response = pairwise_response.content
            decoded_response = json.loads(base64.b64decode(response))
            logging.debug(decoded_response)
        return decoded_response
