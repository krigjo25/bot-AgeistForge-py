from discord import  Colour, Embed

import datetime
from typing import Optional

from lib.utils.exceptions import ExceptionHandler

class EmbedFactory(object):
    """
    Utility class for creating and managing Discord embeds.
    Inherits from discord.Embed to provide additional functionality.
    """

    @classmethod
    def _base_embed(cls, dictionary: dict[str,str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None, fields:Optional[dict[str,str]] = None, text:Optional[str] = None, BOOL:bool = True) -> Embed:
        """
        Returns the base embed object.
        """
        embed = Embed()
        for key, value in dictionary.items():

            match key.lower():
                case "title":
                    embed.title = value

                case "description":
                    embed.description = value

                case "url":
                    if value: embed.url = value
                
                case "image":
                    if value: embed.set_image(url=value)

                case "thumbnail":
                    if value: embed.set_thumbnail(url=value)

                case _: 
                    pass

        if fields: 
            for key, value in fields.items():
                embed.add_field(name=key, value=value, inline= BOOL)

        if not text: 
            text = f"Wish you a glorious day further,\nThe {team} Team"

        embed.timestamp = datetime.datetime.now()
        if team: embed.set_footer(text=text, icon_url=avatar or None)
        if author: embed.set_author(name=f"{author}", icon_url=avatar or None)
        return embed

    @classmethod
    def info(cls, dictionary: dict[str,str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None, fields:Optional[dict[str,str]] = None) -> Embed:
        """
        Sets the embed color to dark purple for informational messages.
        """
        embed = cls._base_embed(dictionary, author = author, team = team, avatar = avatar, fields= fields)
        embed.colour = Colour.dark_blue()
        
        return embed

    @classmethod
    def error(cls, error:ExceptionHandler) -> Embed:
        """
            Creates an embed for exceptions.
        """
        dictionary = dict[str, str]()
        dictionary["message"] = error.message
        dictionary["title"] = f"An Exception Error Occured: {error.__class__.__name__}"

        embed = cls._base_embed(dictionary)
        embed.colour = Colour.dark_red()

        return embed

    @classmethod
    def critical(cls, Error:ExceptionHandler) -> Embed:
        
        dictionary = dict[str, str]()
        dictionary["message"] = Error.message
        dictionary["title"] = f"Critical Error: {Error.__class__.__name__}"

        embed = cls._base_embed(dictionary)
        embed.colour = Colour.red()
        
        return embed
    
    @classmethod
    def warning(cls, dictionary: dict[str, str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        """
        Sets the embed color to dark red for warning messages.
        """
        embed = cls._base_embed(dictionary, author = author, team = team, avatar = avatar)
        embed.colour = Colour.dark_red()

        return embed
    
    @classmethod
    def exception(cls, dictionary: dict[str, str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None) -> Embed:
        """
        Sets the embed color to dark red for warning messages.
        """
        embed = cls._base_embed(dictionary, author = author, team = team, avatar = avatar)
        embed.colour = Colour.dark_red()

        return embed
    
    @classmethod
    def create_embed(cls, dictionary: dict[str, str], author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None, fields:Optional[dict[str,str]] = None) -> Embed:
        embed = cls._base_embed(dictionary, author = author, team = team, avatar = avatar, fields= fields)
        embed.colour = Colour.dark_purple()

        return embed