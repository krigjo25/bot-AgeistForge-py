
from lib.core.api_configurations import APIConfig
from unittest.mock import patch, Mock
class TestCase(object): pass

class TestApi(TestCase):

    "Test the APIConfig class and its methods."
    "Github : https://api.github.com/user/"
    
    def _data_prepearation(self):
        return
    
    def test_make_request(self):

        with patch('lib.core.api_configurations.requests.get') as get:
            get.return_value = Mock(status_code=200, json=lambda: {"message": "Success", "status_code": 200})
            api = APIConfig(URL = "dummyjson.com/http/200")
            response = api.make_request()
        print(response.json())
