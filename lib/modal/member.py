#   Python responsories
import datetime

#   Discord responsory
import discord as d
from discord import utils, Colour
from discord.ui import InputText, Modal

from lib.modal.BaseModal import ModalBase

class Member(ModalBase):

    """
        Member related modals
        This class inherits from ModalBase and implements specific member-related modals.
    """

    def __init__(self, *args, **kwargs):                                #   type: ignore
        #   Channel Modal - Channel related actions.
        super().__init__(*args, **kwargs)                               #   type: ignore      

        match self.title.lower():                                       #   type: ignore  
            case "bug-report": self.bug_report()
            case "member-report": self.member_report()
            case "member-support": self.member_support()
                

    def member_report(self):

        self.add_item(InputText(label = "Member", placeholder= "Member Name"))
        self.add_item(InputText(label = "Uniform Resource Locator (URL)", style=d.InputTextStyle.long, required= True, placeholder= "https://google.com"))
        self.add_item(InputText(label = "Reason", style=d.InputTextStyle.long, required= False, placeholder= ""))
        self.embed.colour = d.Colour.dark_red()

        return

    def member_support(self):

        self.add_item(InputText(label = "Title Of The Document", placeholder= "eg. How To Use Commands", style=d.InputTextStyle.short))
        self.add_item(InputText(label = "Image", placeholder= "Member", style=d.InputTextStyle.short))
        self.add_item(InputText(label = "Challange", placeholder= "What do you need help with?", style=d.InputTextStyle.long))
        self.embed.colour = d.Colour.dark_red()
        return
    
    def bug_report(self): pass
