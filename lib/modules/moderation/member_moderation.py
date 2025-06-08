#   Python Repositories
import datetime, humanfriendly as hf

from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories

from discord.ext import  commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option
from discord import Forbidden, utils, Member, Permissions, PermissionOverwrite

from lib.modal.channel import Channel
from lib.modal.member import MemberModal

from lib.utils.moderation import ModerationUtils

from lib.selections.selections import SupportSelections
from lib.utils.exceptions import SelfReferenceError, ResourceNotFoundError, ExceptionHandler, InvalidDurationError, AuthorizationError

from lib.utils.logger_config import CommandWatcher
logger = CommandWatcher(name="Member Moderation") #   type: ignore
logger.file_handler()

class MemberModeration(commands.Cog):

    """
        Commands for Moderators with moderate members
    """

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.now = datetime.datetime.now()

    member = SlashCommandGroup(name = "member", description = "Member mananger", default_member_permissions = Permissions(moderate_members = True), guild_ids=[1044553368233848843])

    @member.before_invoke   # type: ignore
    async def check_channel(self, ctx:ApplicationContext):
    
        channel = []
        ch = ""#("auditlog", "report", "support") 
        mod_utils = ModerationUtils(self.bot)
        try :
            for i in ch:
                #   Fetch category channels
                if utils.get(ctx.guild.categories, name = "log"):     
                    if utils.get(ctx.guild.text_channels, name = i): 
                        channel.append(i)   #   type: ignore

        except (TypeError, Exception) as e: 
            await mod_utils.create_error_entry(ctx, e)  #   type: ignore



        else:
            if not len(channel) == len(ch):  #   type: ignore

                #   Creating a channel
                PERMS = {ctx.guild.default_role:PermissionOverwrite(view_channel=False)}

                for i in ch:
                    i = await ctx.guild.create_text_channel(i, overwrites=PERMS)

    @member.command(name="warn", description="Warn a community member for their behavior")      #   type: ignore
    async def warn(self, ctx:ApplicationContext, member:Member,                                 #   type: ignore
                   *, reason:Option(str,"A paragraph / rule volaition statement", required = True)):    #   type: ignore

        """
            Warn a member for the member's behavior / rules or regulation voilation
        """
        mod_utils = ModerationUtils(self.bot)

        try:
            mod_utils.fetch_member_exception(ctx, member)  #   type: ignore

        except (SelfReferenceError) as e:
            await mod_utils.create_error_entry(ctx, e)

        else:
            action = f"{ctx.command.name}ed"                                        #   type: ignore
            await mod_utils.create_log_entry(ctx, member, action, reason)           #   type: ignore
            await mod_utils.send_member_message(ctx, member, action, reason)        #   type: ignore
            await ctx.respond(f"{member.name}'s has been {action}", ephemeral=True) #   type: ignore

    @member.command(name = "sush", description="Mute a community member for their behavior")    #   type: ignore
    async def sush(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   time:Option(str, "(1s)ecound / (1m)inute / (1h)our / (1d)ay", required = True), #   type: ignore
                   *, reason:Option(str, "Provide a reason to mute the member", required = True)): #   type: ignore

        arg = ""
        week = 604800  #   1 week in seconds
        mod_utils = ModerationUtils(self.bot)

        for i in str(time):
            if i.isdigit(): arg += i

        try:
            mod_utils.fetch_member_exception(ctx, member)                                                                                                      #   type: ignore
            #if array not in test: raise ExceptionHandler(f"Please indicate the time using '{time}s', '{time}m', '{time}h' or '{time}d'")                      #   type: ignore
            if int(arg) > week: raise InvalidDurationError(f" Could not sush **{member}** due to a limitation for 1w, please consider other consequences.")    #   type: ignore

            if member.communication_disabled_until:
                if member.communication_disabled_until > datetime.datetime.now():                                               #   type: ignore
                    duration = member.communication_disabled_until - datetime.datetime.now()                                    #   type: ignore
                    raise InvalidDurationError(f"Could not sush **{member}**. **{member}** is already shushed for {duration}s") #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, ResourceNotFoundError, AuthorizationError) as e: 
            await mod_utils.create_error_entry(ctx, e)                                                              #   type: ignore

        else:
            action = f"{ctx.command.name}ed"                                                                    #   type: ignore
            time = hf.parse_timespan(time)                                                                      #   type: ignore

            await mod_utils.create_log_entry(ctx, member, action, reason, time)                       #   type: ignore
            await mod_utils.send_member_message(ctx, member, action, reason, time)                    #   type: ignore
            await member.timeout(until = utils.utcnow() + datetime.timedelta(seconds=time), reason = reason)    #   type: ignore

            await ctx.respond(f"{member.name}'s has been {action} for {time}", ephemeral=True)      #   type: ignore                                                              #   type: ignore
        return

    @member.command(name = "lift", description="Lift a community member curse")                 #   type: ignore
    async def lift(self, ctx:ApplicationContext, member:Member):

        mod_utils = ModerationUtils(self.bot)
        
        try: mod_utils.fetch_member_exception(ctx, member)  #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, ResourceNotFoundError, AuthorizationError) as e: 
            await mod_utils.create_error_entry(ctx, e)  #   type: ignore

        else:
            action = f"{ctx.command.name}ed"                                    #   type: ignore
            await member.timeout(until=None)
            await mod_utils.create_log_entry(ctx, member, action)                     #   type: ignore
            await mod_utils.send_member_message(ctx, member, action)                  #   type: ignore

            await ctx.respond(f"{member.name}'s has been {action}ed", ephemeral=True) #   type: ignore 

    @member.command(name = "kick", description="Kick a community member")                       #   type: ignore
    async def kick(self, ctx:ApplicationContext, member:Member, *, reason:Option(str, "Provide A reason to kick the member", required = True)):

        mod_utils = ModerationUtils(self.bot)

        try : mod_utils.fetch_member_exception(ctx, member)  #   type: ignore
        except (SelfReferenceError, Forbidden) as e : await mod_utils.create_error_entry(ctx, e)  #   type: ignore

        else:
            action = f"{ctx.command.name}ed"                                    #   type: ignore
            await mod_utils.create_log_entry(ctx, member, action, reason)       #   type: ignore
            await mod_utils.send_member_message(ctx, member, action, reason)    #   type: ignore

            await member.kick(reason=f"{reason}")

            await ctx.respond(f"{member.name}'s has been {action}ed", ephemeral=True) #   type: ignore 

    @member.command(name= "announce", description="Make an announcement to the community")      #   type: ignore
    async def announcement(self, ctx:ApplicationContext):
        modal = Channel(title = "Announcement")
        await ctx.send_modal(modal)

    @member.command(name="support", description="Request support from the community")           #   type: ignore
    async def community_support(self, ctx:ApplicationContext):                                  #
        await ctx.respond("Select a Fitted topic", view=SupportSelections(), ephemeral=True)    # type: ignore

    @member.command(name="bug-report", description="Report a bug in the server")                #   type: ignore
    async def bug_report(self, ctx:ApplicationContext):
        modal = MemberModal(title="bug-report") 
        await ctx.send_modal(modal)
