#   Misc os utils

#   Import the necessary libraries
import os, time
from pathlib import Path
from typing import Optional

from lib.utils.logger_config import APIWatcher
from lib.utils.exception_handler import NotFoundError

logger = APIWatcher('OS-Utils', 'logs')
logger.file_handler()

class OsUtils(object):

    def __init__(self):
        pass

    def find_file(self, root:str, marker:Optional[str]):
        """
        Get the root directory of the script.
        :return: The root directory of the script.
        """
        start = time.perf_counter()

        try:
            root = self.find_project_root(root)
            if os.path.isfile(marker): return Path(marker)
            if not root: raise NotFoundError(404, "'{marker}' Not found in Root")

        except NotFoundError as e:
            logger.error(f"Error code: {e.status_code}\nError message: {e.message} \nTime Complexity: {start-time.perf_counter()}\n")

            return e

        list_dir = [os.path.join(root,marker) for root, dir, f in os.walk(root) if marker in f]

        logger.info(f"Found '{marker}' in {root} results {list_dir} \nTime Complexity: {start-time.perf_counter()}\n")

        return list_dir

    def combine_path(self, path: str, marker: str) -> str:
        """
        Combine the path with the marker.
        :param path: The path to the directory.
        :param marker: The marker to combine with the path.
        :return: The combined path.
        """

        part = path.split(os.sep)

        start_dir = part.index(marker)
        rel_path = os.sep.join(part[start_dir:])

        logger.info(f"Relative path: {rel_path} \n")
        return rel_path

    def find_directory(self, root:str, marker:Optional[str] ):
        """
        Get the root directory of the script.
        :return: The root directory of the script.
        """
        start = time.perf_counter()

        try:
            root = self.find_project_root(root)

            if os.path.isdir(marker): return Path(marker)
            if not root: raise NotFoundError(404, "Root directory not found", root)

        except NotFoundError as e:
            logger.error(f"Error code: {e.status_code}\nError message: {e.message} Error Arg: {e.arg} \nTime Complexity: {start-time.perf_counter()}\n")
            return

        finally:

            list_dir = [os.path.join(root, marker) for root, dir, f in os.walk(root) if marker in dir]

            logger.info(f"Found '{marker}' in {root} results {list_dir} \nTime Complexity: {start-time.perf_counter()}\n")

            return list_dir[0] if list_dir else None

    @staticmethod
    def find_project_root(marker: str) -> Path:
        """
        Find the root directory of the project.
        :return: The root directory of the project.
        """

        path = Path(os.getcwd()).resolve()
        
        while path.name != path.parent.name:
            
            #   Ensure that the marker is located in the directory
            if (path / marker).exists():
                logger.info(f"{marker} found in {path}\n")

                return path
                
            #   updating the path
            path = path.parent

    @staticmethod
    def create_directory(self, path:str, dir:str | tuple[str]):
        """
        Create a directory if it does not exist.
        :param path: The path to the directory.
        :return: None
        """
        if not os.path.exists(path):  os.makedirs(dir) 
        else: logger.info(f"Directory {path} already exists.")
