from discord import utils, Colour, Embed

import datetime
from typing import Optional

from lib.utils.exception_handler import ExceptionHandler





class EmbedFactory(object):
    """
    Utility class for creating and managing Discord embeds.
    Inherits from discord.Embed to provide additional functionality.
    """
    def __init__(self, author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_embed = Embed()

    def _base_embed(self, dictionary: dict, author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        """
        Returns the base embed object.
        """
        for key, value in dictionary.items():

            match str(key).lower():
                case "title":
                    self.base_embed.title = value
                
                case "url":
                    if value: self.base_embed.url = value
                                
                case "message":
                    self.base_embed.description = value

        self.base_embed.timestamp = datetime.datetime.now()
        if author: self.base_embed.set_author(name=f"{author}", icon_url=avatar or None)
        if team: self.base_embed.set_footer(text=f"Wish you a glorious day further,\nThe {team} Team", icon_url=avatar or None)

        return self.base_embed
    def info(self) -> Embed:
        """
        Sets the embed color to dark purple for informational messages.
        """
        self.base_embed.colour = Colour.dark_blue()

    def error(self, error:ExceptionHandler) -> Embed:
        """
            Creates an embed for exceptions.
        """
        self.base_embed.colour = Colour.dark_red()
        self.base_embed.title = "An error occurred"
        self.base_embed.description = f"```{error.message}```"
        self.base_embed.timestamp = datetime.datetime.now()

        return self.base_embed

    def critical(self):
        self.base_embed.colour = Colour.red()
        pass

    def create_embed(self, title: str, description: str, url: Optional[str] = None):
        self.base_embed.colour = Colour.dark_purple()
        pass

    def embed_exception(self, exception: Exception) -> Embed:

        