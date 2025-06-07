#   Github API
#   Fetching the repositories
import os

from dotenv import load_dotenv

#  Loading the environment variables
load_dotenv()

from typing import Optional, Union

from lib.core.APIConfig import APIConfig
from lib.utils.logger_config import APIWatcher

logger = APIWatcher(name='Github-API')
logger.file_handler()

class GithubAPI(APIConfig):

    """ Github API Configuration
        API : https://api.github.com/
    """

    def __init__(self, URL:Optional[str] = os.getenv("GithubBase"), KEY:Optional[str] = os.getenv('GithubToken'), GET:str = "GET", POST:str = "POST", PUT:str='PUT', PATCH:str='PATCH', DELETE:str = 'DELETE') -> None:
        super().__init__(URL, KEY, GET, POST, PUT, PATCH, DELETE)
        self.GET = GET
        self.PUT = PUT
        self.POST = POST
        self.API_URL = URL
        self.API_KEY = KEY
        self.PATCH = PATCH
        self.DELETE = DELETE
        self.head = {'Content-Type': 'application/json','Authorization': f"{self.API_KEY}"}

    async def post_issue(self, data:dict[str, Union[str, list[str]]], endpoint:str) -> None:
        """
            Posting an issue to the repository
            API : https://api.github.com/repos/{owner}/{repo}/issues
        """
        #   Check for duplicated issues before making a request
        try:
            
            self._make_request_(endpoint, self.head, self.POST, data)

        except Exception as e:
            logger.error(f"An error occurred while posting the issue: {e.__class__.__name__}\nMessage from API: {self.API_URL}{endpoint}\n{e}")
            
            print(f"An error occurred while posting the issue: {e.__class__.__name__}\nMessage from API: {self.API_URL}{endpoint}\n{e}")
            
