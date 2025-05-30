
#   Python Repositories
import datetime
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories
from discord.ext import  commands
from discord.embeds import Embed
from discord import utils, Member, Colour
from discord.commands import ApplicationContext

from lib.utils.logger_config import CommandWatcher
from lib.utils.exception_handler import NotFoundError, ExceptionHandler

logger = CommandWatcher(name="Moderation Utils", dir=".logs")  #   type: ignore
logger.file_handler()

class ModerationUtils(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed()
        self.now = datetime.datetime.now()

    async def create_log_entry(self, ctx:ApplicationContext, member:Member, action:str, reason:Optional[str] = None, time:Optional[str | int] = None):
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

            #   Prepare, send & Clean up embed
            self.base_embed.timestamp = self.now
            self.base_embed.color = Colour.dark_red()
            self.base_embed.title = f"**{member.name}** has been {action} by {ctx.author.name} for {int(time)}s" if time else  f"**{member.name}** has been {action} by {ctx.author.name}"
            self.base_embed.description = f"*{reason}*.\n\n User has been notified by a direct message." if reason else f"User has been notified by a direct message."
            await channel.send(embed=self.base_embed)

    async def create_error_entry(self, ctx:ApplicationContext, e:ExceptionHandler):
        self.base_embed.color = Colour.dark_red()
        self.base_embed.description =f"{e.message}, Try again !"
        self.base_embed.title = f"An {e.__class__.__name__} Occured !"

        logger.error(f"An {e.__class__.__name__} Occured: {e.message}")
        
        channel = utils.get(ctx.guild.channels, name='Exception-logs')
        
        if not channel:
            channel = await ctx.guild.create_text_channel(name='Exception-logs', topic={e.__class__.__name__}, reason="Creating a channel for exception logs")
        await channel.send(embed=self.base_embed)

    async def send_member_message(self, ctx:ApplicationContext, member:Member, action:str, reason:Optional[str] = None, time:Optional[str | int] = None):

        server = f"**{ctx.guild.name if ctx.guild else "the server"}**"
        member_message= ""
        if guidelines := ctx.guild.rules_channel:  #   type: ignore
            self.base_embed.set_footer(text=f"Please read the guidelines in {guidelines.mention} for more information.")
        
        match(action):  #   type: ignore
            case "warn":
                member_message = f"You have been warned by an moderator, as a consequence of :*{reason}*"
 
            case "sush":
                member_message = f"you will not be able to use {server}'s channels for {time}s."

            case "lift":
                member_message = "your sush has been lifted"

            case "kick":
                member_message = "you have been kicked out of the server"
    
        await member.send(f"Greetings, **{member.name}**.\nYou recieve this notification, because you're a member of {server}.\n\n{member_message}.Thank you for your patient and understand\n Sincerely Moderation team")  #   type: ignore
        await member.send(embed = self.base_embed)