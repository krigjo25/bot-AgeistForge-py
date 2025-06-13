
import discord as d
from lib.utils.logger_config import ModalWatcher
from lib.modal.BaseModal import ModalBase
from lib.dictionaries.modal import ModalDictionary

logger = ModalWatcher(name="Modal")
logger.file_handler()

class Channel(ModalBase):

    """
        Channel related modals
        This class inherits from ModalBase and implements specific member-related modals.
    """
    def __init__(self, *args, **kwargs):                            #   type: ignore
        super().__init__(*args, **kwargs)                           #   type: ignore

        self.HandleModal()

    def HandleModal(self) -> None:
         match self.title.lower():                                  #   type: ignore
            case "announcement": self.announcement()
            case "custom-channel": self.custom_channel()
            case "discord-support": self.server_support()

            case _:
                logger.error(f"Modal title '{self.title}' not recognized.")
                raise ValueError(f"Modal title '{self.title}' not recognized.")

    def announcement(self) -> None:
        modal = ModalDictionary().announcement()

        for i in modal:                                             #   type: ignore
            self.create_input(
                label = i['label'],                                 #   type: ignore
                placeholder=i.get('description'),                   #   type: ignore
                style = i.get("style") or d.InputTextStyle.short,   #   type: ignore
                required = bool(i.get("required")))                 #   type: ignore

    def custom_channel(self) -> None:
        modal = ModalDictionary().create_channel_modal()

        for i in modal:                                             #   type: ignore
            self.create_input(
                label = i['label'],                                 #   type: ignore
                placeholder=i.get('description'),                   #   type: ignore
                style = i.get("style") or d.InputTextStyle.short,   #   type: ignore
                required = bool(i.get("required")))                 #   type: ignore

    def server_support(self) -> None:
        modal = ModalDictionary().server_support()

        for i in modal:                                             #   type: ignore
            self.create_input(
                label = i['label'],                                 #   type: ignore
                placeholder=i.get('description'),                   #   type: ignore
                style = i.get("style") or d.InputTextStyle.short,   #   type: ignore
                required = bool(i.get("required")))                 #   type: ignore
