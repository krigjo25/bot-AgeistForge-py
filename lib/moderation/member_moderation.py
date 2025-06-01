#   Python Repositories
import datetime, humanfriendly as hf

from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories
from discord.embeds import Embed
from discord.ext import  commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option
from discord import Forbidden, Colour, utils, Member, Permissions, PermissionOverwrite

from lib.modal.channel import Channel
from lib.utils.moderation import ModerationUtils
from lib.utils.logger_config import CommandWatcher
from lib.utils.exception_handler import SelfReferenceError, NotFoundError, ExceptionHandler, InvalidDurationError, AuthorizationError

logger = CommandWatcher(name="Member Moderation", dir=".logs") #   type: ignore
logger.file_handler()

class MemberModeration(commands.Cog):

    """
        Commands for Moderators with moderate members
    """

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed()
        self.now = datetime.datetime.now()

    member = SlashCommandGroup(name = "member", description = "Member mananger", default_member_permissions = Permissions(moderate_members = True), guild_ids=[1044553368233848843])

    @member.before_invoke   # type: ignore
    async def check_channel(self, ctx:ApplicationContext):
    
        channel = []
        ch = ""#("auditlog", "report", "support") 

        try :
            for i in ch:
                #   Fetch category channels
                if utils.get(ctx.guild.categories, name = "log"):     
                    if utils.get(ctx.guild.text_channels, name = i): 
                        channel.append(i)
            
            if len(channel) == len(ch): 
                raise ExceptionHandler(f"Channels already exists, please try again with another name or delete the existing channels: {channel}")  #   type: ignore

        except (TypeError, ExceptionHandler) as e: 
            print(e)

        else:

            #   Creating a channel
            PERMS = {ctx.guild.default_role:PermissionOverwrite(view_channel=False)}

            for i in ch:

                self.base_embed.color = Colour.dark_red()
                self.base_embed.title = f'Auto Generated Channel'

                match i:

                    case "auditlog": 
                        self.base_embed.description = "Created to have easy accsess to bot commands used by admin / moderator"

                    case "report": 
                        self.base_embed.description = "Member report channel"

                    case "support": 
                        self.base_embed.description = "Member support channel"
                
                i = await ctx.guild.create_text_channel(i, overwrites=PERMS)

                self.base_embed.timestamp = datetime.datetime.now()
                await i.send(embed=self.base_embed)

    @member.command(name="warn", description="Warn a community member for their behavior")       #   type: ignore
    async def warn(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   *, reason:Option(str, "A paragraph / rule volaition statement", required = True)):  #   type: ignore

        """
            Warn a member for the member's behavior / rules or regulation voilation
        """
        mod_utils = ModerationUtils(self.bot)

        try:
            mod_utils.fetch_member_exception(ctx, member)  #   type: ignore

        except (SelfReferenceError) as e:
            await mod_utils.create_error_entry(ctx,e)

        else:
            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason)      #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason)   #   type: ignore
            await ctx.respond("Command executed.")                                  #   type: ignore

    @member.command(name = "sush", description="Mute a community member for their behavior")   #   type: ignore
    async def sush(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   time:Option(str, "(1s)ecound / (1m)inute / (1h)our / (1d)ay", required = True), #   type: ignore
                   *, reason:Option(str, "Provide a reason to mute the member", required = True)): #   type: ignore

        arg = ""
        week = 604800  #   1 week in seconds
        mod_utils = ModerationUtils(self.bot)

        for i in str(time):
            if i.isdigit(): arg += i

        try:
            mod_utils.fetch_member_exception(ctx, member)  #   type: ignore
            #if array not in test: raise ExceptionHandler(f"Please indicate the time using '{time}s', '{time}m', '{time}h' or '{time}d'")                                  #   type: ignore
            if int(arg) > week: raise InvalidDurationError(f" Could not sush **{member}** due to a limitation for 1w, please consider other consequences.")    #   type: ignore

            if member.communication_disabled_until:
                if member.communication_disabled_until > datetime.datetime.now(): #   type: ignore
                    duration = member.communication_disabled_until - datetime.datetime.now()  #   type: ignore
                    raise InvalidDurationError(f"Could not sush **{member}**. **{member}** is already shushed for {duration}s")  #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, NotFoundError, AuthorizationError) as e: 
            await mod_utils.create_error_entry(ctx, e)  #   type: ignore

        else:
            time = hf.parse_timespan(time)                                                                          #   type: ignore

            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason, time)                           #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason, time)                        #   type: ignore
            await member.timeout(until = utils.utcnow() + datetime.timedelta(seconds=time), reason = reason)       #   type: ignore

            await ctx.respond("Command executed.")                                                                  #   type: ignore
        return

    @member.command(name = "lift", description="Lift a community member curse")   #   type: ignore
    async def lift(self, ctx:ApplicationContext, member:Member):

        mod_utils = ModerationUtils(self.bot)
        
        try: mod_utils.fetch_member_exception(ctx, member)  #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, NotFoundError, AuthorizationError) as e: 
            await mod_utils.create_error_entry(ctx, e)  #   type: ignore

        else:
            await member.timeout(until=None)
            await mod_utils.create_log_entry(ctx, member, ctx.command.name)  #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name)   #   type: ignore
            await ctx.respond("Command executed.")                                  #   type: ignore

    @member.command(name = "kick", description="Kick a community member")   #   type: ignore
    async def kick(self, ctx:ApplicationContext, member:Member, *, reason:Option(str, "Provide A reason to kick the member", required = True)):

        mod_utils = ModerationUtils(self.bot)

        try : mod_utils.fetch_member_exception(ctx, member)  #   type: ignore
        except (SelfReferenceError, Forbidden) as e : await mod_utils.create_error_entry(ctx, e)  #   type: ignore

        else:
            
            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason)         #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason)      #   type: ignore

            await member.kick(reason=reason)                                                #   type: ignore

    @member.command(name= "announce", description="Make an announcement to the community")  #   type: ignore
    async def announcement(self, ctx:ApplicationContext):

        """
            Community announcements

        """
        modal = Channel(title = "Announcement")
        await ctx.send_modal(modal)


    @member.after_invoke                            #   type: ignore
    async def after_invoke(self, ctx:ApplicationContext):

        self.base_embed.title = ""
        self.base_embed.clear_fields()
        self.base_embed.remove_image()
        self.base_embed.remove_author()
        self.base_embed.remove_footer()
        self.base_embed.description = ""
        self.base_embed.remove_thumbnail()
        self.base_embed.color = Colour.dark_purple()
