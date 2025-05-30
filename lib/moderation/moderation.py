#   Python Repositories
import datetime, humanfriendly as hf

from dotenv import load_dotenv
load_dotenv()
#   Discord Repositories
from discord import Forbidden, Colour
from discord.ext import  commands
from discord.embeds import Embed
from discord import Member, Permissions
from discord.commands import SlashCommandGroup, ApplicationContext, Option

from lib.modal.channel import Channel
from lib.utils.moderation import ModerationUtils
from lib.utils.logger_config import CommandWatcher
from lib.utils.exception_handler import SelfReferenceError, NotFoundError, ExceptionHandler, InvalidDurationError

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
        #   TODO: Check if auditlog / exception  channel exists, if not create one
        pass

    @member.command(name="warn", description="Warn a community member for their behavior")       #   type: ignore
    async def warn(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   *, reason:Option(str, "A paragraph / rule volaition statement", required = True)):  #   type: ignore

        """
            Warn a member for the member's behavior / rules or regulation voilation
        """
        mod_utils = ModerationUtils(self.bot)

        try:pass
            #if member == ctx.author: raise SelfReferenceError(400, "You tried to warn your self")

        except (SelfReferenceError) as e:
            #await mod_utils.create_error_entry(ctx,e)
            return

        else:
            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason)      #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason)   #   type: ignore
            await ctx.respond("Command executed.")                                  #   type: ignore

    @member.command(name = "sush", description="Mute a community member for their behavior")   #   type: ignore
    async def sush(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   time:Option(str, "(1s)ecound / (1m)inute / (1h)our / (1d)ay", required = True), #   type: ignore
                   *, reason:Option(str, "Provide a reason to mute the member", required = True)): #   type: ignore
        
        mod_utils = ModerationUtils(self.bot)
        try:
            if member == ctx.author: raise SelfReferenceError(400,"Could not sush your self.")
            elif len(time) != 2: raise ExceptionHandler(400,f"Please indicate the time using '{time}s', '{time}m', '{time}h' or '{time}d'")                                  #   type: ignore
            elif int(time[0]) > 604800: raise InvalidDurationError(400, f" Could not sush **{member}** due to a limitation for 1w, please consider other consequences.")    #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, NotFoundError) as e: 
            await mod_utils.create_error_entry(ctx, e)  #   type: ignore

            return

        else:
            
            time = hf.parse_timespan(time)                                                                          #   type: ignore
            

            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason, time)                           #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason, time)                        #   type: ignore
            #await member.timeout(until = utils.utcnow() + datetime.timedelta(seconds=time), reason = reason)       #   type: ignore

            await ctx.respond("Command executed.")                                                                  #   type: ignore
        return

    '''@member.command(name = "lift", description="Lift a community member curse")   #   type: ignore
    async def lift(self, ctx:ApplicationContext, member:Member):

        await self.create_log_entry(ctx, member, "unmuted")  #   type: ignore
        try:
            await member.timeout(until=None)
        except Forbidden:
            await self.create_error_entry(ctx, ExceptionHandler(403, "I do not have permission to lift the mute for this member."))  #   type: ignore
        else:
            await self.create_log_entry(ctx, member, ctx.command.name)      #   type: ignore
            await self.send_member_message(ctx, member, ctx.command.name)   #   type: ignore
            await ctx.respond("Command executed.")                                  #   type: ignore
'''
    @member.command(name = "kick", description="Kick a community member")   #   type: ignore
    async def kick(self, ctx:ApplicationContext, member:Member, *, reason:Option(str, "Provide A reason to kick the member", required = True)):

        mod_utils = ModerationUtils(self.bot)
        try : pass
            #if member == ctx.author: raise SelfReferenceError("Can not kick your self")
            
        except (SelfReferenceError, Forbidden) as e :

            await mod_utils.create_error_entry(ctx, e)  #   type: ignore
            return 

        else:
            
            await mod_utils.create_log_entry(ctx, member, ctx.command.name, reason)         #   type: ignore
            await mod_utils.send_member_message(ctx, member, ctx.command.name, reason)      #   type: ignore

            await member.kick(reason=reason)                                                #   type: ignore

    @member.command(name= "announce", description="Make an announcement to the community")  #   type: ignore
    async def announcement(self, ctx:ApplicationContext):

        """
            Community announcements

        """
        modal = Channel(title = "Channel Announcement")
        await ctx.send_modal(modal)

    @member.after_invoke                            #   type: ignore
    async def clear_memory(self, ctx:ApplicationContext):

        #   Clearing embeds
        self.base_embed.clear_fields()
        self.base_embed.remove_image()
        self.base_embed.remove_author()
        self.base_embed.remove_footer()
        self.base_embed.description = ""
        self.base_embed.remove_thumbnail()
        self.base_embed.color = Colour.dark_purple()
