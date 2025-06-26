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
API_request = APIWatcher(name='API-Request')
API_request.file_handler()

class APIConfig(object):

    def __init__(self, URL:Optional[str], KEY:Optional[str] = None, GET:str = "GET", POST:str = "POST", PUT:str='PUT', PATCH:str='PATCH', DELETE:str = 'DELETE') -> None:
        self.GET = GET
        self.PUT = PUT
        self.POST = POST
        self.API_URL = f"https://{URL}"
        self.API_KEY = KEY
        self.PATCH = PATCH
        self.DELETE = DELETE

    def make_request(self, method: Optional[str] = "GET", data:Optional[Dict[str, Union[str, list[str]]]] = None, timeout: Optional[int] = 30) -> requests.Response:

        #   Initialize the start time
        start = perf_counter()
        playload = json.dumps(data) if data else None        
        API_request.info(f"Attempting to '{method}' from {self.API_URL}\n")

        try:
            match str(method).upper():
                case self.GET:
                    response = requests.get(self.API_URL, timeout=timeout, headers=self.API_KEY)
            
                case self.POST: 
                    response = requests.request(f"{self.POST}",f"{self.API_URL}{self.API_URL}", data = playload, timeout=timeout, headers=self.API_KEY)

                case self.PUT:
                    raise NotImplementedError(f"{method} Not Implemented")
                
                case self.PATCH:
                    raise NotImplementedError(f"{method} Not Implemented")
                
                case self.DELETE:
                    raise NotImplementedError(f"{method} Not Implemented")

                case _:
                    raise ValueError(f"Unsupported HTTP method: '{method}'")

            response.raise_for_status() #   Raise an HTTPError if not a 2xx response

            API_request.info(f"'{self.API_URL}{self.API_URL}' Returned Ok.\n")
            API_request.critical(f"Time elapsed: {perf_counter()-start}\n")
            return response.json() if response.content else None        #   type: ignore

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            data_text = ""
            if data:
                data_text = f"{self.POST}ING Data : {data}"

            API_request.error(f"Headers: {self.API_KEY}\nAPI Endpoint: {self.API_URL}\n")
            API_request.error(f"An Exception Occurred: {e.__class__.__name__}\n")
            API_request.error(f"Message from API: {self.API_URL}\n{self.API_URL}: {e}\n{data_text}\n")
            API_request.critical(f"Time elapsed: {perf_counter()-start}\n")
                        
            raise e
        else:
            return 

    def calculate_n(self, endpoint: str, header:dict[str, str]): pass
        #return self.make_request(self.API_URL f"{self.API_URL}{endpoint}", self.API_KEY = header)
