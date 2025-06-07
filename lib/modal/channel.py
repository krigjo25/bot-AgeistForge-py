
import discord as d
from lib.utils.logger_config import CommandWatcher
from lib.modal.BaseModal import ModalBase
from lib.dictionaries.modal import ModalDictionary

logger = CommandWatcher(name="Modal", dir=".logs")  # type: ignore
logger.file_handler()

class Channel(ModalBase):

    """
        Channel related modals
        This class inherits from ModalBase and implements specific member-related modals.
    """
    def __init__(self, *args, **kwargs):                #   type: ignore
        #   Channel Modal - Channel related actions.
        super().__init__(*args, **kwargs)               #   type: ignore      e
        
        self.HandleModal()
        

    def HandleModal(self):
         match self.title.lower():                                       #   type: ignore
            case "announcement": self.announcement()

    def announcement(self):

        modal = ModalDictionary().announcement()                    #   type: ignore

        for i in modal:                                             #   type: ignore
            self.create_input(
                label = i['label'],                                 #   type: ignore
                placeholder=i.get('description'),                   #   type: ignore
                style = i.get("style") or d.InputTextStyle.short,   #   type: ignore
                required = bool(i.get("required")))                 #   type: ignore
