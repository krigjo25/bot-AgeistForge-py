
#   Python Repositories
import datetime
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories
from discord.ext import  commands

from discord import utils, Member, Colour
from discord.commands import ApplicationContext

from lib.utils.embed import EmbedFactory as Embed
from lib.utils.logger_config import CommandWatcher
from lib.utils.exception_handler import NotFoundError, ExceptionHandler, SelfReferenceError, InvalidDurationError, AuthorizationError

logger = CommandWatcher(name="Moderation Utils", dir=".logs")  #   type: ignore
logger.file_handler()

class ModerationUtils(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed()
        self.now = datetime.datetime.now()

    async def create_log_entry(self, ctx:ApplicationContext, member:Member, action:str, reason:str, time:Optional[str | int] = None):
        action = ctx.command.name if not action else action     #   type: ignore
        channel = utils.get(ctx.guild.channels, name='auditlog')

        try:
            if not channel: raise NotFoundError("Channel \"**auditlog**\" does not exists")

        except NotFoundError as e:
            await self.create_error_entry(ctx, e)  #   type: ignore
            return
        
        else:
            match(action):

                case "lift":
                    action = "unmuted"

                case _:
                    action = action + "ed"

            dictionary = {
                "title": f"**{member.name}** has been {action} by {ctx.author.name}",
                "message": f"*{reason}*.\n\n User has been notified by a direct message."
            }

            embed = self.base_embed.warning(dictionary)

            await channel.send(embed=embed)

    async def create_error_entry(self, ctx:ApplicationContext, e:ExceptionHandler):
        logger.error(f"An {e.__class__.__name__} Occured: {e.message}")
        await ctx.respond(f"An {e.__class__.__name__} Occured: {e.message}", ephemeral=True)  #   type: ignore

    async def send_member_message(self, ctx:ApplicationContext, member:Member, action:str, reason:Optional[str] = None, time:Optional[float] = None):
        """
            Send a direct message to the member about the action taken
        """

        member_message= ""
        server = f"**{ctx.guild.name if ctx.guild else "the server"}**"

        match(action):  #   type: ignore
            case "warn":
                member_message = f"You have been warned by an moderator, as a consequence of :\n*{reason}*.\n\n"
 
            case "sush":
                member_message = f"You will not be able to use {server}'s channels for {int(time) * 1}s as a consequence of :\n*{reason}*.\n\n"

            case "lift":
                member_message = "Your sush has been lifted.\n\n"

            case "kick":
                member_message = f"You have been kicked out of the server. as a conequence of \n*{reason}*.\n\n"
            
            case _:  pass

        if ctx.guild.rules_channel : 
            member_message += f"Please read the guidelines in **{ctx.guild.rules_channel.mention}** for more information.\n\n"
    
        await member.send(f"Greetings, **{member.name}**.\nYou recieve this notification, because you're a member of {server}.\n\n{member_message}Thank you for your patient and understanding\n Sincerely Moderation team")  #   type: ignore

    def fetch_member_exception(self, ctx:ApplicationContext, member:Member):
        """
            Fetch the exception and return it
        """
        if member == ctx.author: raise SelfReferenceError()
        if not member: raise NotFoundError(f"{member.name} not found")  #   type: ignore
        if member.top_role >= ctx.author.top_role: raise AuthorizationError()  #   type: ignore
        