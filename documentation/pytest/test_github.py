
import os

from dotenv import load_dotenv

#  Loading the environment variables
load_dotenv()

from lib.apis.github_api import GithubAPI
from documentation.pytest.utils.data_preperation import TestCase

class TestSuccsessfullApiCall(TestCase):

    "Test the GithubAPI class and its methods."
    "Github : https://dummyjson.com/"

    REST_API_URL = os.getenv("GithubBase")

    def test_status_code_OK(self):
        mock_response = self._data_prepearation('lib.apis.github_api.requests.get')

        api = GithubAPI(URL = f"{self.REST_API_URL}http/200")
        response = api.post_issue()

        assert response.status_code == mock_response.return_value.status_code
    
    def test_json_response(self):
        mock_response = self._data_prepearation('lib.apis.github_api.requests.get')

        api = GithubAPI(URL = f"{self.REST_API_URL}http/200")
        response = api.post_issue()

        assert response.json() == mock_response.return_value.json()

class TestExceptions(TestCase):

    "Test the GithubAPI class exceptions."
    REST_API_URL = "dummyjson.com/"