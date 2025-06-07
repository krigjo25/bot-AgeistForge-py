#   Base Classes for the application

#   Importing required dependencies
import requests, json

from time import perf_counter
from typing import Optional, Union, Dict
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from dotenv import load_dotenv
load_dotenv()

#   Imporiting custom dependencies
from lib.utils.logger_config import  APIWatcher
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

    def _make_request_(self, endpoint: str, head: Dict[str, str], method: Optional[str] = "GET", data:Optional[Dict[str, Union[str, list[str]]]] = None, timeout: Optional[int] = 30) -> requests.Response:

        #   Initialize the start time
        start = perf_counter()
        playload = json.dumps(data) if data else None        
        APILog.info(f"Attempting to '{method}' from {endpoint}\n")

        try:
            match str(method).upper():
                case self.GET:
                    response = requests.get(endpoint, timeout=timeout, headers=head)
            
                case self.POST: 
                    response = requests.request(f"{self.POST}",f"{self.API_URL}{endpoint}", data = playload, timeout=timeout, headers=head)

                case self.PUT:
                    raise NotImplementedError(f"{method} Not Implemented")
                
                case self.PATCH:
                    raise NotImplementedError(f"{method} Not Implemented")
                
                case self.DELETE:
                    raise NotImplementedError(f"{method} Not Implemented")

                case _:
                    raise ValueError(f"Unsupported HTTP method: '{method}'")

            response.raise_for_status() #   Raise an HTTPError if not a 2xx response

            APILog.info(f"'{self.API_URL}{endpoint}' Returned Ok.\n")
            APILog.critical(f"Time elapsed: {perf_counter()-start}\n")
            return response.json() if response.content else None        #   type: ignore

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            data_text = ""
            if data:
                data_text = f"{self.POST}ING Data : {data}"

            APILog.error(f"Headers: {head}\nAPI Endpoint: {endpoint}\n")
            APILog.error(f"An Exception Occurred: {e.__class__.__name__}\n")
            APILog.error(f"Message from API: {self.API_URL}\n{endpoint}: {e}\n{data_text}\n")
            APILog.critical(f"Time elapsed: {perf_counter()-start}\n")
                        
            raise e

    def calculate_n(self, endpoint: str, header:dict[str, str]):
        return self._make_request_(endpoint = f"{self.API_URL}{endpoint}", head = header)
