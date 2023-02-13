import pytest
import requests
import json

class TestUpdatePITR:
    request_body={
                    "table":"Movie",
                    "pitr":True
                }
    url = "http://127.0.0.1:5002/api/dynamodb/PITR"

    def test_pitr_enabled(self):
        data = self.request_body
        data["pitr"] = True
        response = requests.patch(self.url,json=data)
        assert response.json()=={"message": "Point-in-time-recovery is already enabled"}
        assert response.status_code == 200

    def test_pitr_disabled(self):
        data = self.request_body.copy()
        data["pitr"] = False
        response = requests.patch(self.url,json=data)
        assert response.json()=={"message": "Point-in-time-recovery is already disabled"}
        assert response.status_code == 200

    def test_table_not_string(self):
        data = self.request_body.copy()
        data['table'] = 41
        response = requests.patch(self.url, json=data)
        assert response.json() == {"error": f"Parameter validation failed:\nInvalid type for parameter TableName, value: {data['table']}, type: <class 'int'>, valid types: <class 'str'>"}
        assert response.status_code == 400

    def test_pitr_not_bool(self):    
        data = self.request_body.copy()
        data["pitr"] = "kedar"
        response = requests.patch(self.url, json=data)
        assert response.json() == {"error": "pitr value should be Bool"} 
        assert response.status_code == 400

    def test_table_availability(self):
        data = self.request_body.copy()
        data["table"] = "Move"
        response = requests.patch(self.url, json=data)  
        assert response.json() == {"error": "Table not found"}
        assert response.status_code == 400

    if __name__ == "__main__":
        pytest.main()



    


    