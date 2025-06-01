
import discord as d
from lib.utils.logger_config import CommandWatcher
from lib.modal.BaseModal import ModalBase
from lib.dictionaries.modal import ModalDictionary
logger = CommandWatcher(name="Modal", dir=".logs")  # type: ignore
logger.file_handler()

class Channel(ModalBase):

    """
        Channel modals

        #   Author : krigjo25
        #   Date :   21.02-23
        #   Last update: 22.02-23

        #   Server announcements
        #   Create multiply channels
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        match self.title.lower():
                case "announcement": self.announcement()

    def announcement(self):

        md = ModalDictionary().announcement()
        
        print(md)
        for i in md: 
            self.create_input(
                label = i['label'], 
                placeholder=i.get('description'), 
                style = i.get("style") or d.InputTextStyle.short,
                required = bool(i.get("required")))
