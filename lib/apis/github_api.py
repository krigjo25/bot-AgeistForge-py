#   Github API
#   Fetching the repositories
import os, uuid, datetime, time

from dotenv import load_dotenv

#  Loading the environment variables
load_dotenv()

from typing import Optional, Union, Any
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

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

    async def fetch_data(self, endpoint:str) -> Optional[list[dict[str, Union[str, list[str]]]]]:
        """
            Fetching the repositories
            API : https://api.github.com/users/repos

            :param endpoint: The endpoint to fetch data from
            :return: A list of dictionaries containing the repository data
            :rtype: Optional[list[dict[str, Union[str, list[str]]]]]
        """
        start = time.perf_counter()

        #   Initialize an API call
        try:
            response = self.get(f"{self.API_URL}{endpoint}", head=self.head)

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            logger.error(f"An Exception Occured : {e.__class__.__name__}\nMessage from API:{self.API_URL}\n{endpoint}: {e}")
            raise e

        else:
            #   Initialize a list
            repo = []

            #   fetch the response
            for i in range(len(response)):

                #   Initialize a dictionary
                repoObject = {}
                repoObject['id'] = uuid.uuid4().hex
                repoObject['name'] = response[i]['name']

                repoObject['owner'] = response[i]['owner']['login']
                repoObject['description'] = response[i]['description']
                repoObject['date'] = datetime.datetime.strptime(response[i]['updated_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d-%m-%y')
                repoObject['lang'] = [await self.fetch_languages(repoObject, f"{self.API_URL}/repos/{repoObject['owner']}/{repoObject['name']}/languages")]
                repoObject['links'] = [
                    {
                        'code': 'bi bi-code',
                        'globe':'bi bi-globe',
                        'ytube': "bi bi-youtube",
                        
                        'demo_url': None,
                        'ytube_url': None,                    
                        'github_url': response[i]['html_url'],
                    }]
                if response[i]['homepage'] or response[i]['homepage'] == "None":

                    repoObject['links'].append(
                        {
                            'icon':"bi bi-globe", 
                            'url':response[i]['homepage']
                        })

                repo.append(repoObject)

            logger.info(f"Repositories fetched successfully. {repo}\nTime Complexity: {time.perf_counter() - start:.2f}s\n")
            return repo

    async def fetch_languages(self, repo: object, endpoint: str) -> Optional[dict[str, Union[str, list[Any]]]]:

        #   Request a languages les problemos
        response = self.get(endpoint, head=self.head)

        language = {}
        language['lang'] = []

        for lang, value in response.items():
        
            match(str(lang).lower()):
                case "c#":
                    lang = "CS"

                case "c++":
                    lang = "CP"
                
                case "jupyter notebook":
                    lang = "jp-nb"

                case _:
                    lang = lang

        language['lang'].append(lang)   #   type: ignore
        language['id'] = uuid.uuid4().hex

        logger.info(f"Languages fetched successfully. {language}")

        return language

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
            
