import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict


class CustomRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Check if the data is an error response
        response = ''
        print(data)
        key = data.get('key')
        del data['key']
        if 'ErrorDetail' in str(data):
            response = json.dumps({'error': True, 'key': key, 'data': data})

        else:
            response = json.dumps({'error': False, 'key': key, 'data': data})

        return response
