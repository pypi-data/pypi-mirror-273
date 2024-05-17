from .base_client import APIClient
from .models import ModelType
import json

class DoctaHTTPClient(APIClient):
    def __init__(self, api_key, user_id):
        super().__init__(api_key, user_id)
        self.model = None
    
    def set_model(self, model: ModelType):
        self.model = model
    
    def get_model(self):
        return self.model
    
    def run_docta(self, data):
        if not self.model:
            raise ValueError("model is not set")
        return json.loads(self.post(self.model._value_, data)["response"])
