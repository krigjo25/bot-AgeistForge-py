
#   Discord responsory
import discord as d


from lib.modal.BaseModal import ModalBase
from lib.dictionaries.modal import ModalDictionary

class MemberModal(ModalBase):

    """
        Member related modals
        This class inherits from ModalBase and implements specific member-related modals.
    """

    def __init__(self, *args, **kwargs):                                #   type: ignore
        #   Channel Modal - Channel related actions.
        super().__init__(*args, **kwargs)                               #   type: ignore      

        match self.title.lower():                                       #   type: ignore  
            case "bug-report": self.bug_report()
            #case "member-report": self.discord_report()
            case "member-support": self.member_support()

    def member_support(self):
        modal = ModalDictionary().discord_support()                        #   type: ignore

        for i in modal:                                                 #   type: ignore
            self.create_input(
                label = i['label'],                                     #   type: ignore
                placeholder=i.get('description'),                       #   type: ignore
                style = i.get("style") or d.InputTextStyle.short,       #   type: ignore
                required = bool(i.get("required")))                     #   type: ignore

    
    def bug_report(self): pass
