import pytest
import requests
from collections.abc import Iterable
# from ...dynamoDB_module.constants import *

class TestListExports:
    request_body= {"bucket":"my-demo1"}
    url = "http://127.0.0.1:5000/api/dynamodb/listExport"

    def test_response_is_json(self):
        data = self.request_body
        response = requests.get(self.url, json=data)   
        for filepath in response.json():       
            assert filepath.endswith(".json.gz")
            assert response.status_code == 200       

    def test_bucket_missing(self):
        data = self.request_body.copy()
        data.pop("bucket")
        response = requests.get(self.url, json=data)
        assert response.json()=={"error": "Parameter 'bucket' is mising"}
        assert response.status_code == 400

    def test_bucket_is_string(self):
        data = self.request_body.copy()
        data["bucket"] = True
        response = requests.get(self.url, json=data)
        assert response.json()=={"error": "expected string or bytes-like object"}
        assert response.status_code == 400

    def test_bucket_availability(self):
        data = self.request_body.copy()
        data["bucket"] = "my-dem"
        response = requests.get(self.url, json=data)
        assert response.json()=={"error": "bucket does not exist"}
        assert response.status_code == 400

    def test_bucket_access(self):
        data = self.request_body.copy()
        data["bucket"] = "my-demo"
        response = requests.get(self.url, json=data)
        assert response.json()=={"error": "access denied for this bucket"}
        assert response.status_code == 400
    
    if __name__ == "__main__":
            pytest.main()