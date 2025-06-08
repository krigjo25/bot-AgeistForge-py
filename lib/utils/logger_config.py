#  Handling the application logging

#   Importing required dependencies
import os, logging
from typing import Optional, Union, TextIO

class Log(object):

    """
        Responsibility to handle application logging
    """
    def __init__(self, name:str, dir:str):

        """
            *   Initialize the logger
            *   Set the logging level to DEBUG
            *   Set the logging format
            *   Set the logging handler

            *   param dir: str - default: None
            *   param name: str - default: Class name
        """
        
        #   Initialize the handler
        self.dir = dir
        self.name = name if name else self.__class__.__name__

        self.log = logging.getLogger(f"{self.name}")
        self.log.setLevel(logging.DEBUG)
        
        #   Initialize the Flags
        self.file_flag = False
        self.console_flag = False

    def setup_handler(self, handler:Union[logging.FileHandler, logging.StreamHandler[TextIO]]):
        
        """
            *   Setup the logging handler
            *   param handler:[logging.FileHandler, logging.StreamHandler]
        """
        #   Initializing the formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s -\t %(name)s -\t %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
    
    def console_handler(self):
        """
            *   Add a console handler to the logger
        """
        
        #   Ensure that the Flag is not set to True
        if not self.console_flag:
            
            #   Set the flag
            self.console_flag = True
            
            #   Initializing the handler
            handler = logging.StreamHandler()
            self.setup_handler(handler)

            self.log.info(f"Console handler has been initalized as {self.name}\n")

    def file_handler(self):

        """
            *   Add a file handler to the logger
        """

        #   Ensure that the Flag is not set to True
        if not self.file_flag:

            #   Initializing the handler
            if self.dir:
                if not os.path.exists(self.dir): os.makedirs(self.dir)

                handler = logging.FileHandler(self.dir + "/" + self.name)

            else: handler = logging.FileHandler(self.name)

            self.file_flag = True

            self.setup_handler(handler)
            
            self.log.info(f"File handler has been initalized as {self.name}\n")
            
        else:
            self.log.warning(f"{self.name} File handler already initialized")

    def info(self, message:str): self.log.info(message)
    def error(self, message:str): self.log.error(message)
    def debug(self, message:str): self.log.debug(message)
    def warn(self, message:str): self.log.warning(message)
    def critical(self, message:str): self.log.critical(message)
    def exception(self, message:str): self.log.exception(message)
    

class AppWatcher(Log):

    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

class APIWatcher(Log):
    
    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

class DatabaseWatcher(Log):

    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

class AdminWatcher(Log):

    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

class CommandWatcher(Log):
    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

class ModalWatcher(Log):
    def __init__(self, name:Optional[str], dir:Optional[str] = None):
        super().__init__(dir = dir if dir else ".logs", name=f"{self.__class__.__name__} -- {name}.log")

