import discord as d

class ModalDictionary(object):

    """
        ModalDictionary class
        Provides pre-defined modal inputs for various use cases.
    """
    def __init__(self): pass

    def announcement(self):

        list_inputs = []

        title = {

            "label": "Title",
            "required": True}

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

        list_inputs.append(ch)        # type: ignore
        list_inputs.append(url)       # type: ignore
        list_inputs.append(title)     # type: ignore
        list_inputs.append(message)   # type: ignore

        return list_inputs

    def server_report(self): pass
    def discord_report(self): pass
    def server_support(self): pass
    def discord_support(self): pass
    def bugreport(self): pass