#   Base Classes for the application

#   Importing required dependencies
import requests, json

from time import perf_counter
from dotenv import load_dotenv
from typing import Optional, Union
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


#   Imporiting custom dependencies
from lib.utils.logger_config import  APIWatcher
from lib.utils.exceptions import ResourceNotFoundError
#  Loading the environment variables
load_dotenv()


APILog = APIWatcher(name='API-Calls')
APILog.file_handler()


class APIConfig(object):

    def __init__(self, URL:Optional[str] = None, KEY:Optional[str] = None, GET:str = "GET", POST:str = "POST", PUT:str='PUT', PATCH:str='PATCH', DELETE:str = 'DELETE') -> None:
        self.GET = GET
        self.PUT = PUT
        self.POST = POST
        self.API_URL = URL
        self.API_KEY = KEY
        self.PATCH = PATCH
        self.DELETE = DELETE
        

    def get(self, endpoint: str, head: dict[str, str], timeout:Optional[int] = 30) -> Optional[dict[str, Union[str, list[str]]]]:

        """
            Calling the API

        """

        #   Initialize the start time
        start = perf_counter()
        req = requests.get(f"{endpoint}", timeout=timeout, headers=head)
        APILog.info(f"Attempting to fetch data from {self.API_URL}{endpoint}")
        
        try:
            match (req.status_code):
                case 200 | 201 | 202 | 204:
                    APILog.warn(f"Request code :{req.status_code} Time elapsed: {perf_counter()-start}\n")
                    return req.json()

                case 401 | 403: raise ConnectionError("Unauthorized Access")
                case 404: raise HTTPError("Resource not found")
                case 410: raise ResourceNotFoundError("The requested resource is no longer available")
                case 500 | 502 | 503 | 504: raise Timeout("The request timed out")
                case _: raise RequestException(f"An Exception which was not encounted for arised. status code: {req.status_code}")
            
        except (HTTPError, ConnectionError, Timeout, RequestException) as e: 
            APILog.error(f"""
                        Headers: {head}\nAPI Endpoint: {endpoint}\n
                        Request code :{req.status_code}\nException arised : {e.__class__.__name__}\n
                        Error: {e}, Time elapsed: {perf_counter()-start}\nPlease check the API endpoint and app network connection.\n""")
            raise e
        
    def post(self,endpoint:str, head:dict[str, str], data:Optional[dict[str, Union[str, list[str]]]] = None, timeout:Optional[int] = 30) -> Optional[dict[str, Union[str, list[str]]]]:
        """
            Submitting data to the API
            API : https://api.github.com/users/repos/{owner}/{repo}/import/issues

            :param endpoint: The API endpoint to submit data to
            :param head: The headers to include in the request
            :param data: The data to submit to the API
            :param timeout: The timeout for the request in seconds
        """
        start = perf_counter()
        playload = json.dumps(data) if data else None
        print(endpoint, head, playload, head)
        try:
            req = requests.request(f"{self.POST}",f"{self.API_URL}{endpoint}", data = playload, timeout=timeout, headers=head)
            APILog.info(f"Attempting to post data to {self.API_URL}{endpoint} {req.status_code} : {req.content}")

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            APILog.error(f"""Headers: {head}\nAPI Endpoint: {endpoint}\n
                        Exception arised : {e.__class__.__name__}\n
                        Error: {e}, Time elapsed: {perf_counter()-start}\n
                        Headers: {head}\nPlease check the API endpoint and app network connection.\n""")
            raise e

    def calculate_n(self, endpoint: str, header:dict[str, str]):

        return self.get(endpoint = f"{self.API_URL}{endpoint}", head = header)
