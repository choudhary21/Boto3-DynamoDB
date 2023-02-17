import pytest
import requests
# from ...dynamoDB_module.constants import *

class TestListTables:
    @pytest.mark.parametrize()
    @pytest.fixture(autouse=True)
    def setUp(self):
        print('************SETUP*********')

        self.request_body={""}
        self.url = "http://127.0.0.1:5000/api/dynamodb/PITR"

    def test_status_code(self):    
        response = requests.get(self.url)
        assert not response.status_code == 200
    
    if __name__ == "__main__":
        pytest.main()