
import requests, pytest

from lib.core.api_configurations import APIConfig
from documentation.pytest.utils.data_preperation import TestCase


class TestApi_codes(TestCase):

    "Test the APIConfig class and its methods."
    "Github : https://dummyjson.com/"

    REST_API_URL = "dummyjson.com/"

    def test_status_code(self):
        mock_response = self._data_prepearation('lib.core.api_configurations.requests.get')

        api = APIConfig(URL = f"{self.REST_API_URL}http/200")
        response = api.make_request()

        assert response.status_code == mock_response.return_value.status_code

class TestExceptions(TestCase):
    
    REST_API_URL = "dummyjson.com/"

    def test_http_error(self):
        with pytest.raises(requests.exceptions.HTTPError):
            api = APIConfig(URL = f"{self.REST_API_URL}http/404")
            api.make_request()

        with pytest.raises(requests.exceptions.HTTPError):
            api = APIConfig(URL = f"{self.REST_API_URL}http/500")
            api.make_request()

    def test_connection_error(self): pass

class TestApi_json(TestCase):

    REST_API_URL = "dummyjson.com/"

    def test_json_response(self):
        mock_response = self._data_prepearation('lib.core.api_configurations.requests.get')

        api = APIConfig(URL = f"{self.REST_API_URL}http/200")
        response = api.make_request()

        assert response.json() == mock_response.return_value.json()
