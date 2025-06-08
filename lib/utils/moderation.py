
#   Python Repositories
import datetime
from typing import Optional, Dict
from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories
from discord.ext import  commands

from discord import utils, Member, Interaction, PermissionOverwrite, Permissions
from discord.commands import ApplicationContext

from lib.utils.embed import EmbedFactory as Embed
from lib.utils.logger_config import CommandWatcher
from lib.utils.exceptions import ResourceNotFoundError, ExceptionHandler, SelfReferenceError, AuthorizationError

logger = CommandWatcher(name="Moderation Utils", dir=".logs")  #   type: ignore
logger.file_handler()

class ModerationUtils(object):

    def __init__(self):
        self.base_embed = Embed()
        self.now = datetime.datetime.now()

    @staticmethod
    def fetch_member_exception(interaction:Interaction, member:Member) -> None:
        """
            Fetch the exception and return it
        """
        
        if not member: raise ResourceNotFoundError(f"Member not found")
        if member == interaction.user: raise SelfReferenceError(" You cannot moderate yourself")
        if member.top_role >= interaction.user.top_role : raise AuthorizationError("You cannot moderate this member, because they have a higher role than you")                                                         # type: ignore
    

    async def create_log_entry(self, interaction:Interaction, member:Member, action:str, reason:str, time:Optional[str | int] = None):
        channel = utils.get(interaction.guild.channels, name='auditlog')                                                        #   type: ignore

        try:
            if not channel: raise ResourceNotFoundError("Channel \"**auditlog**\" does not exists")

        except ResourceNotFoundError:
            permissions: Dict[str, PermissionOverwrite] = {}
            permissions['forum_moderators'] = PermissionOverwrite(view_channel=True)
            permissions['Admins'] = PermissionOverwrite(view_channel=True, send_messages=False)
            permissions['Moderators'] = PermissionOverwrite(view_channel=True, send_messages=False)
            permissions[interaction.guild.default_role] = PermissionOverwrite(view_channel=False, send_messages=True)           #   type: ignore
            self.create_channel(name = "auditlog", interaction=interaction, channel_type = Channel.Text, perms = permissions)   #   type: ignore
        
        else:

            dictionary = {
                "title": f"**{member.name}** has been {action} by {interaction.user.name}",
                "message": f"*{reason}*.\n\n User has been notified by a direct message."
            }

            embed = self.base_embed.warning(dictionary)

            await channel.send(embed=embed)     #   type: ignore

    @staticmethod
    async def create_error_entry(ctx:ApplicationContext | Interaction, e:ExceptionHandler) -> None:
        logger.error(f"An {e.__class__.__name__} Occured: {e.message}")
        await ctx.respond(f"An {e.__class__.__name__} Occured: {e.message}\nPlease report if you think this is a mistake **/community bug-report**\n**Errors are Saved in the bot, but not supervised.**", ephemeral=True)  #   type: ignore

    @staticmethod
    async def send_member_message(ctx:ApplicationContext, member:Member, action:str, reason:Optional[str] = None, time:Optional[int] = None):
        """
            Send a direct message to the member about the action taken
        """

        member_message= ""
        server = f"**{ctx.guild.name if ctx.guild else "the server"}**"

        match(action):  #   type: ignore

            case "ban":
                member_message = f"You have been banned from {server} as a consequence of :\n*{reason}*.\n\n"

            case "sush":
                member_message = f"You will not be able to use {server}'s channels for {time}s as a consequence of :\n*{reason}*.\n\n"

            case "lift":
                member_message = "Your sush has been lifted.\n\n"

            case _:
                member_message = f"You have been {action}ed by an moderator, as a consequence of :\n*{reason}*.\n\n"

        if ctx.guild.rules_channel : 
            member_message += f"Please read the guidelines in **{ctx.guild.rules_channel.mention}** for more information.\n"
    
        await member.send(f"Greetings, **{member.name}**.\nYou recieve this notification, because you're a member of {server}.\n\n{member_message}Thank you for your patient and understanding\n Sincerely Moderation team")  #   type: ignore

    async def create_channel(self, name:str, interaction:Interaction, channel_type:Optional[str] = None, perms:Optional[Dict[str, PermissionOverwrite]] = None) -> None:
        raise NotImplementedError("This method is not implemented yet, please use the Channel class to create a channel")