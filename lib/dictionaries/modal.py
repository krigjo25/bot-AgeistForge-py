import discord as d

from typing import TypedDict, 
class ModalDictionary(object):

    """
        ModalDictionary class
        Provides pre-defined modal inputs for various use cases.
    """
    def __init__(self): pass

    def announcement(self):

        title = {

            "label": "Title",
            "required":b (True)}

        ch = {

            "required": True,
            "label": "Channel Name"}
        url = {
            "label": "URL",
            "description": "Optional URL for the announcement"}

        message = {
            "required": True,
            "label": "Message",
            "style": d.InputTextStyle.long}

        return (title, ch, url, message)

    def server_report(self): pass
    def discord_report(self): pass
    def server_support(self): pass
    def discord_support(self): pass
    def bugreport(self): pass