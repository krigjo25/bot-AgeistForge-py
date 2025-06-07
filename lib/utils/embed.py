from discord import  Colour, Embed

import datetime
from typing import Optional

from lib.utils.exceptions import ExceptionHandler


class EmbedFactory(object):
    """
    Utility class for creating and managing Discord embeds.
    Inherits from discord.Embed to provide additional functionality.
    """

    BASE_EMBED = Embed()

    @classmethod
    def _base_embed(cls, dictionary: dict[str,str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None, add_fields:Optional[dict[str,str]] = None, text:Optional[str] = None):
        """
        Returns the base embed object.
        """

        for key, value in dictionary.items():

            match key.lower():
                case "title":
                    cls.BASE_EMBED.title = value

                case "message":
                    cls.BASE_EMBED.description = value

                case "url":
                    if value: cls.BASE_EMBED.url = value
                
                case "image":
                    if value: cls.BASE_EMBED.set_image(url=value)

                case "thumbnail":
                    if value: cls.BASE_EMBED.set_thumbnail(url=value)

                case _: pass

        if  add_fields: cls.add_new_fields(add_fields)

        if not text: text = f"Wish you a glorious day further,\nThe {team} Team"

        cls.BASE_EMBED.timestamp = datetime.datetime.now()
        if author: cls.BASE_EMBED.set_author(name=f"{author}", icon_url=avatar or None)
        if team: cls.BASE_EMBED.set_footer(text=text, icon_url=avatar or None)

    @classmethod
    def add_new_fields(cls, dictionary: dict[str,str]):

        for key, value in dictionary.items():
            cls.BASE_EMBED.add_field(name=key, value=value, inline=False)

    @classmethod
    def info(cls, dictionary: dict[str,str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        """
        Sets the embed color to dark purple for informational messages.
        """

        cls._base_embed(dictionary, author = author, team = team, avatar = avatar)
        cls.BASE_EMBED.colour = Colour.dark_blue()
        
        return cls.BASE_EMBED

    @classmethod
    def error(cls, error:ExceptionHandler) -> Embed:
        """
            Creates an embed for exceptions.
        """
        dictionary = {
            "title": f"An {error.__class__.__name__} Occurred",
            "message": error.message
        }

        cls._base_embed(dictionary)
        cls.BASE_EMBED.colour = Colour.dark_red()

        return cls.BASE_EMBED

    @classmethod
    def critical(cls):
        cls.BASE_EMBED.colour = Colour.red()
        return cls.BASE_EMBED
    
    @classmethod
    def warning(cls, dictionary: dict[str, str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        """
        Sets the embed color to dark red for warning messages.
        """
        cls._base_embed(dictionary, author = author, team = team, avatar = avatar)
        cls.BASE_EMBED.colour = Colour.dark_red()

        return cls.BASE_EMBED
    
    @classmethod
    def create_embed(cls, dictionary: dict[str, str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        cls._base_embed(dictionary, author = author, team = team, avatar = avatar)
        cls.BASE_EMBED.colour = Colour.dark_purple()

        return cls.BASE_EMBED