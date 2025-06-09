
from typing import Tuple, Union, Dict, Any
import discord as d

class ModalDictionary(object):

    """
        ModalDictionary class
        Provides pre-defined modal inputs for various use cases.
    """
    def __init__(self): pass

    @staticmethod
    def announcement() -> Tuple[Dict[str, Union[str, bool]], ...]:

        title: Dict[str, Union[str, bool]] = {}
        title['label'] = "Title"
        title['required'] = True
        title['description'] = "Title of the announcement (e.g. 'Server Maintenance')"

        url: Dict[str, Union[str, bool]] = {}
        url['label'] = "URL"
        url['description'] = "Optional URL for the announcement (e.g. 'https://example.com/announcement')"
        
        message: Dict[str, Union[str, Any]] = {}
        message['required'] = True
        message['label'] = "Message"
        message['style'] = d.InputTextStyle.long
        message['description'] = "Announcement content (e.g. 'The server will be down for maintenance from 12:00 AM to 2:00 AM')"

        return (title, url, message)

    @staticmethod
    def discord_support() -> Tuple[Dict[str, Union[str, Any]], ...]: 
        title : Dict[str, Union[str, Any]] = {}
        title['label'] = "Title"
        title['required'] = True
        title['description'] = "(e.g. 'Unable to access general channel')"

        message: Dict[str, Union[str, Any]] = {}
        message['required'] = True
        message['label'] = "Message"
        message['style'] = d.InputTextStyle.long
        message['description'] = "Describe the issue you are facing (e.g. 'I am unable to access the general channel due to a permission error')"

        return (title, message)

    @staticmethod
    def server_support() -> Tuple[Dict[str, Union[str, Any]], ...]: 
        title : Dict[str, Union[str, Any]] = {}
        title['label'] = "Title"
        title['required'] = True
        title['description'] = "(e.g. 'Unable to access general channel')"

        image: Dict[str, Union[str, bool]] = {}
        image['label'] = "Image/Video"
        image['description'] = "Image or a video link of the issue (e.g https://example.com/image.png)"

        message: Dict[str, Union[str, Any]] = {}
        message['required'] = True
        message['label'] = "Message"
        message['style'] = d.InputTextStyle.long
        message['description'] = "Describe the issue you are facing (e.g. 'I am unable to access the general channel due to a permission error')"

        return (title, image, message)

    @staticmethod
    def bug_report() -> Tuple[Dict[str, Union[str, Any]], ...]:

        name : Dict[str, Union[str, str | bool]] = {}
        name['required'] = True
        name['label'] = "Application/Game Name"
        name['description'] = "Name of the application or game (e.g. 'MyGame')"

        title: Dict[str, Union[str, str | bool]] = {}
        title['required'] = True
        title['label'] = "Issue Title"
        title['description'] = "Brief description of the issue (e.g. 'Game crashes on startup')"

        image: Dict[str, Union[str, bool]] = {}
        image['required'] = True
        image['label'] = "Image/Video"
        image['description'] = "Image or a video link of the issue (e.g https://example.com/image.png)"
        
        message: Dict[str, Union[str, Any]] = {}
        message['required'] = True
        message['label'] = "Reproduction Steps"
        message['style'] = d.InputTextStyle.long
        message['description'] = "Steps to reproduce the issue (e.g. '1. Open the game\n2. Click on Start Game')"

        details: Dict[str, Union[str, Any]] = {}
        details['required'] = True
        details['label'] = "Additional Details"
        details['style'] = d.InputTextStyle.long
        details['description'] = "e.g. 'This issue occurs only on mobile devices'"

        return (name, title, image, message, details)

    @staticmethod
    def create_channel_modal() -> Tuple[Dict[str, Union[str, Any]], ...]:
        
        name: Dict[str, Union[str, bool]] = {}
        name['required'] = True
        name['label'] = "Channel Name"
        name['description'] = "(e.g. 'general' 'announcements', 'support') *Required*"

        channeltype: Dict[str, Union[str, bool]] = {}
        channeltype['required'] = True
        channeltype['label'] = "Channel Type"
        channeltype['description'] = "type of channel (e.g. Text / Voice / Stage / forum / news) *Required*"   

        category: Dict[str, Union[str, bool]] = {}
        category['required'] = False
        category['label'] = "Category"
        category['description'] = "Select the category for the channel (optional)"

        topic: Dict[str, Union[str, bool]] = {}
        topic['required'] = False
        topic['label'] = "Channel Topic"
        topic['description'] = "(e.g. 'General discussion about the server') *Optional*"

        perm: Dict[str, Union[str, Any]] = {}
        perm['required'] = False
        perm['label'] = "Channel Permissions"
        perm['style'] = d.InputTextStyle.long
        perm['description'] = "Select the permissions for the channel (/help permissions for more info) *Separated by **','**"

        return (name, channeltype, category, topic, perm)