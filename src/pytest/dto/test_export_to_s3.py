import pytest
import requests

class TestExporttoS3:

    url = "http://127.0.0.1:5002/api/dynamodb/export"

    request_body = {"TableName":"Movie", "S3Bucket":"my-demo1"
                }

    def test_export_to_S3(self):
        data = self.request_body
        response = requests.patch(self.url,json=data)
        assert response.json()=={"message": "Successfully exported the file to S3 bucket"}
        assert response.status_code == 200
        
    def test_bucket_name_notvalid(self):
        data = self.request_body.copy()
        data["S3Bucket"] = "de"
        response = requests.patch(self.url,json=data)
        assert response.json()=={"error": "bucket must have length greater than or equal to 3"}
        assert response.status_code == 400

    def test_table_name_notvalid(self):
        data = self.request_body.copy()
        data["TableName"] = "Mo"
        response = requests.patch(self.url,json=data)
        assert response.json()=={"error": "length of table name cannot be less than 3"}
        assert response.status_code == 400

    def test_table_missing(self):
        data = self.request_body.copy()
        data["TableName"] = "Movi"
        response = requests.patch(self.url,json=data)
        assert response.json()=={"error": f"Table {data['TableName']} not found"}
        assert response.status_code == 400

    def test_bucket_missing(self):
        data = self.request_body.copy()
        data["S3Bucket"] = "my-dem"
        response = requests.patch(self.url,json=data)
        assert response.json()=={"error": f"Bucket {data['S3Bucket']} does not exist."}
        assert response.status_code == 400

    def test_parameter_missing(self):
        data = self.request_body.copy()
        data.pop("TableName")
        response = requests.patch(self.url,json=data)
        assert response.json()=={"error": {"message": "Parameter validation failed","parameter": "'TableName'"}}
        assert response.status_code == 400

    if __name__ == "__main__":
        pytest.main()                                       