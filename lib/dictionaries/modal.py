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

    def server_report(self): pass

    def discord_report(self):
        title = {

            "label": "Report Title",
            "description": "Discord name - Spamming(E.G Jhon Doe - Spamming)",
            "required":True}


        url = {
            "label": "URL",
            "description": "Image or a video link of the rule voilation",
            "required": True,
            }

        message = {
            "required": True,
            "label": "Reason",
            "description": "Please provide a detailed reason for the report",
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
    def bugreport(self): pass