import requests
import json
from .utils import parse_json_response, check_status_code

class APIClient:
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.base_url = 'https://staging.api.docta.ai/api-key-'
        self.user_id = user_id

    def get(self, model, params=None):
        headers = {
            'apiKey': self.api_key, 
            'userId': self.user_id
        }
        payload = {
            "message": params
        }
        response = requests.get(f'{self.base_url + model}', headers=headers, params=payload)
        check_status_code(response)
        return parse_json_response(response)

    def post(self, model, data=None):
        headers = {
            'apiKey': self.api_key, 
            'userId': self.user_id
        }
        payload = {
            "message": json.dumps(data)
        }
        response = requests.post(f'{self.base_url + model}', headers=headers, json=payload)
        check_status_code(response)
        return parse_json_response(response)
