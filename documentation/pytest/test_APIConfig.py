
import requests, pytest

from lib.core.api_configurations import APIConfig
from documentation.pytest.utils.data_preperation import TestCase


class TestSuccsessfullApiCall(TestCase):

    "Test the APIConfig class and its methods."
    "Github : https://dummyjson.com/"

    REST_API_URL = "dummyjson.com/"

    def test_status_code_OK(self):
        mock_response = self._data_prepearation('lib.core.api_configurations.requests.get')

        api = APIConfig(URL = f"{self.REST_API_URL}http/200")
        response = api.make_request()

        assert response.status_code == mock_response.return_value.status_code
    
    def test_json_response(self):
        mock_response = self._data_prepearation('lib.core.api_configurations.requests.get')

        api = APIConfig(URL = f"{self.REST_API_URL}http/200")
        response = api.make_request()

        assert response.json() == mock_response.return_value.json()

class TestExceptions(TestCase):

    "Test the APIConfig class exceptions."
    REST_API_URL = "dummyjson.com/"

    def test_http_error(self):
        with pytest.raises(requests.exceptions.HTTPError):
            api = APIConfig(URL = f"{self.REST_API_URL}http/404")
            api.make_request()

        with pytest.raises(requests.exceptions.HTTPError):
            api = APIConfig(URL = f"{self.REST_API_URL}http/500")
            api.make_request()

    @pytest.mark.parametrize("method", ['PUT', 'PATCH', 'DELETE'])
    def test_not_implemented_error(self, method:str):
        with pytest.raises(NotImplementedError):
            APIConfig(URL = f"{self.REST_API_URL}http/200").make_request(method=f'{method}')

    @pytest.mark.parametrize("method", ['G3T', 'P05T', 'P4TCH', 'D3L3T3'])
    def test_value_error(self, method:str):
        with pytest.raises(requests.exceptions.RequestException):
            APIConfig(URL = f"{self.REST_API_URL}http/200").make_request(method=f'{method}')

    def test_connection_error(self):
        with pytest.raises(requests.exceptions.ConnectionError):
            APIConfig(URL = f"127.0.0.1:80").make_request()

    def test_timeout_error(self):
        with pytest.raises(requests.exceptions.Timeout):
            APIConfig(URL = f"{self.REST_API_URL}http/200").make_request(timeout=0.001)

