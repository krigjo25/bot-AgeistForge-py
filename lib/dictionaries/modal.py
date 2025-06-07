
from typing import Tuple, Union, Dict, Any
import discord as d

class ModalDictionary(object):

    """
        ModalDictionary class
        Provides pre-defined modal inputs for various use cases.
    """
    def __init__(self): pass

    def announcement(self):

        title = {

            "label": "Title",
            "required":True}


        url = {
            "label": "URL",
            "description": "Optional URL for the announcement"}

        message = {
            "required": True,
            "label": "Message",
            "style": d.InputTextStyle.long}

        return (title, url, message)

    def server_support(self): pass
    def discord_support(self): 
        title = {

            "label": "title",
            "description": "e.g. 'Unable to access general channel'",
            "required":True}


        image = {
            "label": "image/video",
            "description": "Image or a video link of the issue",
            "required": False,
            }

        message = {
            "required": True,
            "label": "Message",
            "description": " e.g. 'I am unable to access the general channel due to a permission error'",
            "style": d.InputTextStyle.long}

        return (title, image, message)

    def bug_report(self):
        name = {
            "required":False,
            "label": "app",
            "description": "Name of the application or game (e.g. 'MyGame')",}

        title = {
            "label": "title",
            "required":False,
            "description": "e.g. 'Game crashes on startup'"}


        image = {
            "required": False,
            "label": "image/video",
            "description": "Image or a video link of the issue (e.g https://example.com/image.png)",
            }
        
        
        message = {
            "required": False,
            "label": "Reproduction-Steps",
            "description": " e.g. '1. Open the game server\n2. Utilize the command /help\n3. Error message appears'",
            "style": d.InputTextStyle.long
            }
        
        details = {
            "required": bool(False),
            "label": "Additional-Details",
            "description": " e.g. 'This issue occurs only on mobile devices'",
            "style": d.InputTextStyle.long}

        return (name, title, image, message, details)