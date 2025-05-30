#   Python Repositories
import datetime, humanfriendly as hf, os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
#   Discord Repositories
from discord.ext import  commands
from discord.embeds import Embed, Colour
from discord import utils, Member, Permissions
from discord.commands import SlashCommandGroup, ApplicationContext, Option

from lib.utils.exception_handler import SelfReferenceError, NotFoundError, ExceptionHandler, InvalidDurationError
class MemberModeration(commands.Cog):

    """
        Commands for Moderators with moderate members
        
        #   Author : krigjo25
        #   Date :   21.02-23
        #   Last update :

        #   Warn a member
        #   Sush a member
        #   lift a member
        #   kick a member
    """

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed()
        self.now = datetime.datetime.now()

    member = SlashCommandGroup(name = "member", description = "Member mananger", default_member_permissions = Permissions(moderate_members = True), guild_ids=[1044553368233848843])

    @member.before_invoke   # type: ignore
    async def check_channel(self, ctx:ApplicationContext):
        #   TODO: Check if auditlog channel exists, if not create one
        pass

    @member.command(name="warn", description="Warn a community member for their behavior")       #   type: ignore
    async def warn(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   *, reason:Option(str, "A paragraph / rule volaition statement", required = True)):  #   type: ignore

        """
            Warn a member for the member's behavior / rules or regulation voilation
        """

        #   Check for an auditlog channel
        chlog = utils.get(ctx.guild.channels, name='auditlog')#   Fetch the channel log

        try:
            if member == ctx.author: raise SelfReferenceError(400, "You tried to warn your self")
            if not chlog : raise NotFoundError(404,"Channel \"**auditlog**\" does not exists")

        except (SelfReferenceError, NotFoundError) as e :

            self.base_embed.color = Colour.dark_red()
            self.base_embed.title = f"An {e.__class__.__name__} Occured !"
            self.base_embed.description =f"{e.message}, Try again !"
            ctx.respond(embed = self.base_embed)
            return

        else:
            await self.create_log_entry(ctx, member, ctx.command.name, reason) #   type: ignore

            #   Message the user about the warn
            self.base_embed.timestamp = self.now
            self.base_embed.title = f"You have been warned by {ctx.author}"
            self.base_embed.description = f"You have been warened by an moderator, as a consequence of :*{reason}*\nPlease read and follow the suggested guidelines for behavior in {ctx.guild}*"
            await member.send(f"Greetings **{member}**.\n You recieve this Notification, because you are a member of {ctx.guild}.", embed = self.base_embed) # type: ignore
            await ctx.respond("Command executed.")#   type: ignore

    '''@member.command()   #   type: ignore
    async def sush(self, ctx:ApplicationContext, member:Member, #   type: ignore
                   time:Option(str, "(1s)ecound / (1m)inute / (1h)our / (1d)ay", required = True), #   type: ignore
                   *, reason:Option(str, "Provide a reason to mute the member", required = True)): #   type: ignore

        ch = utils.get(ctx.guild.channels, name='auditlog')

        try:#   Checking if the selected member is the command invoker
            if not ch : raise NotFoundError(404, "Required channel does not exists")
            if member == ctx.author: raise SelfReferenceError(400,"Could not sush your self.")
            elif len(time) < 2: raise ExceptionHandler(400,f"Please indicate the time using '{time}s', '{time}m', '{time}h' or '{time}d'")                                  #   type: ignore
            elif int(time[0]) > 604800: raise InvalidDurationError(400, f" Could not sush **{member}** due to a limitation for 1w, please consider other consequences.")    #   type: ignore

        except (SelfReferenceError, ExceptionHandler, InvalidDurationError, NotFoundError) as e: 
            self.base_embed.color = Colour.dark_red()
            self.base_embed.title = f"An {e.__class__.__name__} Occured"
            self.base_embed.description = f"{e.message}"
            await ctx.respond(embed = self.base_embed)

            return

        else:

            time = hf.parse_timespan(time)  #   type: ignore

            #   Prepare, send & Clean up embed
            self.base_embed.timestamp = self.now
            self.base_embed.color = Colour.dark_red()
            self.base_embed.title = f"**{member.display_name}** has been sushed by {ctx.author.name} for {datetime.timedelta(seconds=time)}"
            self.base_embed.description = f"*{reason}*.\n\n User has been notified by a direct message."
            
            await self.create_log_entry(member = member, reason = reason, time = time) #   type: ignore
            
            await self.send_member_message(member, ctx, time) #   type: ignore
            await member.timeout(until = utils.utcnow() + datetime.timedelta(seconds=time), reason = reason)
        return

    @member.command()
    async def lift(self, ctx:ApplicationContext, member:Member):

        """
            #   Fetching the channel and role
            #   Checking for exceptions
            #   Remove the member role
            4   send the selected member a message
        """

        #   Fetch channel and role
        await self.check_channel(ctx)# Calling the function manually
        ch = utils.get(ctx.guild.channels, name='auditlog')

        try :#   Check for exceptions

            if not ch: raise Exception("Auditlog channel were not created")

        except Exception as e:

            self.embed.description = f"{e}"
            self.embed.color = Colour.dark_red()
            self.embed.title = "An Exception Occured"
            await ctx.send(embed = self.embed)

            del ch
            return

        else:

            #   Prepare & send embed message
            self.embed.timestamp = self.now
            self.embed.color = Colour.dark_red()
            self.embed.title = f'The Sush Has Been Lifted For {member} by {ctx.author}'
            self.embed.description = f"User has been notified by a direct message."
        
            await ch.send(embed= self.embed)

        await member.timeout(until=None) # remove timeout
        self.embed.title = f"The Sush Has Been Lifted !"
        self.embed.description = f"This means you can use {ctx.guild.name}"

        await member.send(f"Greetings **{member}**, you recieve this message because you're a member in {ctx.guild.name}.")# Notify the member
        await member.send(embed = self.embed)

        
        del ch, member#   Clear some memory
        return


    @member.command()   #   type: ignore
    async def kick(self, ctx:ApplicationContext, member:Member, *, reason:Option(str, "Provide A reason to kick the member", required = True)):

        """
            Kick a member out of the channel
            #   Checks for exceptions
            #   Prepare the embed message
            #   Sending the member notification for the kick
            #   Kicking the member
        """
        await self.check_channel(ctx)# Calling the function manually
        ch = utils.get(ctx.guild.channels, name='auditlog')#   Fetching the channel

        try :

            if member == ctx.author: raise Exception("Can not kick your self")
            if not ch : raise Exception("The Channel \"**auditlog**\" were not created")

        except Exception as e :

            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}, try again."
            self.embed.color = Colour.dark_red()
            await ctx.send(embed=self.embed)

            del ch, reason, member#   Clear some memory
            return 

        else:

            #   Prepare embed
            self.embed.timestamp = self.now
            self.embed.color = Colour.dark_red()
            self.embed.description = f' *{reason}*.'
            self.embed.title = f'**{member}** has been kicked from the server by {ctx.author.name} Date : {self.now}'

            #   Creating a message to the user, send it to his DM, then kick
            self.embed.timestamp = self.now
            self.embed.title = f"You Have Been Kicked Out From {ctx.guild.name}"
            self.embed.description = f"*{reason}*"
            await member.send(f"Greetings **{member}**.\nYou recieve this notification because you're a member of {ctx.guild.name}")
            await member.send(embed = self.embed)
            await member.kick(reason=reason)#   Kick the member out

        await ch.send(embed=self.embed)

        del ch, reason, member #    Clear some memory

        return

    @member.command()
    async def announcement(self, ctx:ApplicationContext):

        """
            Community announcements

        """
        modal = Channel(title = "Channel Announcement")
        await ctx.send_modal(modal)'''

    async def create_log_entry(self, ctx:ApplicationContext, member:Member, action:str, reason:str, time:Optional[str | int] = 0):
        channel = utils.get(ctx.guild.channels, name='auditlog')


        try:
            if not channel: raise NotFoundError(404, "Channel \"**auditlog**\" does not exists")
        except Exception as e:
            print(e)

        else:
            match(action):
                case "warn":
                    action = "warned"
                case _:
                    action = action

            #   Prepare, send & Clean up embed
            self.base_embed.timestamp = self.now
            self.base_embed.color = Colour.dark_red()
            self.base_embed.title = f"**{member.name}** has been {action} by {ctx.author.name} for {time}" if time else  f"**{member.name}** has been {action} by {ctx.author.name}"
            self.base_embed.description = f"*{reason}*.\n\n User has been notified by a direct message."
            await channel.send(embed=self.base_embed)

    async def send_member_message(self, member:Member, ctx:ApplicationContext, time:str | int):

        await member.send(f"""Greetings, **{member.name}**.
                          You recieve this notification, because you're a member of {ctx.guild}, you will not be able to use {ctx.guild}'s channels for {time}.
                          Please read and follow the suggested guidelines for behavior in {ctx.guild}.""")
        await member.send(embed = self.base_embed)

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
