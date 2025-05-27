#   Python Repositories
import datetime
import humanfriendly as hf

#   Discord Repositories
import discord as d
from discord import utils
from discord.embeds import Embed, Colour
from discord.ext import  commands


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
        self.embed = Embed()
        self.now = datetime.datetime.now()

    member = d.SlashCommandGroup(name = "member", description = "Member mananger", default_member_permissions = d.Permissions(moderate_members = True))

    @member.command()
    async def warn(self, ctx:d.ApplicationContext, member:d.Member, *, reason:d.Option(str, "A paragraph / rule volaition statement", required = True)):

        """
            Warn a member for the member's behavior / rules or regulation voilation
        """

        await self.check_channel(ctx)  #   Manually call the function 

        chlog = utils.get(ctx.guild.channels, name='auditlog')#   Fetch the channel log

        try:
            if member == ctx.author: raise Exception("Can not warn your self")
            if not chlog : raise Exception("audit channel does not exits")

        except Exception as e :

            self.embed.color = Colour.dark_red()
            self.embed.title = "An Exception Occured"
            self.embed.description =f"{e}, Try again !"
            ctx.send(embed = self.embed)
            
            del chlog, reason, member # Clear som data
            return

        else:

            #   Prepare the embed message
            self.embed.timestamp = self.now
            self.embed.color = Colour.dark_red()
            self.embed.description = f'*{reason}*\n\n User has been notified by a direct message.'
            self.embed.title = f'**{member}** has been warned by {ctx.author.name}'
            await chlog.send(embed=self.embed)


            #   Message the user about the warn
            self.embed.timestamp = self.now
            self.embed.title = f"You have been warned by {ctx.author}"
            self.embed.description = f"*{reason}*\n\nPlease read and follow the suggested guidelines for behavior in {ctx.guild}*"
            await member.send(f"Greetings **{member}**.\n You recieve this Notification, because you are a member of {ctx.guild}.", embed = self.embed)

        #   Clear some memory
        del member, reason, chlog

        return

    @member.command()#   Mute Members
    async def sush(self, ctx:d.ApplicationContext, member:d.Member, time:d.Option(str, "Counting time, (1s / 1m / 1h / 1day)", required = True), *, reason:d.Option(str, "Provide a reason to mute the member", required = True)):

        """
            Give a member a timeout

            #   Role & Channel
            #   Check if "time" argument is digits
            #   #   Set the time as int if it is a digit
            #   Check if the channel exists
            #   Check if there is a reason for unmute
            #   Check if the time is less than 1 week
            #   Check if the author is the member
            #   Calculate the time
            #   Prepare and messages
            #   timeout and send the message
        """

        await self.check_channel(ctx)# Calling the function manually
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try:#   Checking if the selected member is the command invoker

            if member == ctx.author: raise Exception(f"Could not sush your self.")
            elif len(time) < 2: raise Exception(f"{time}s / {time}m / {time}h / {time}d)")
            elif int(time[0]) > 604800: raise Exception(f' Could not sush **{member}** due to a limitation for 1w')
            
            if not ch : raise Exception("Auditlog does not exists")

        except Exception as e: 

            self.embed.color = Colour.dark_red()
            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}"
            await ctx.send(embed = self.embed)
            
            del time, ch, reason, member #   Clear some memory

            return

        else:

            time = hf.parse_timespan(time)#   Calculating the time

            #   Prepare, send & Clean up embed
            self.embed.timestamp = self.now
            self.embed.color = Colour.dark_red()
            self.embed.title = f"**{member.name}** has been sushed by {ctx.author.name} for {datetime.timedelta(seconds=time)}"
            self.embed.description = f"*{reason}*.\n\n User has been notified by a direct message."
            await ch.send(embed=self.embed)

            #   Prepare and send the member, the message and sush the member
            self.embed.timestamp = self.now
            self.embed.title = f"You have been sushed by {ctx.author} for {datetime.timedelta(seconds=time)}"
            self.embed.description = f"*{reason}*\n\n Please read"
            await member.send(f"Greetings, **{member.name}**.\nYou recieve this notification, because you're a member of {ctx.guild}, You will not be able to use {ctx.guild}'s channels for {time}.\n")
            await member.send(embed = self.embed)
            await member.timeout(until = utils.utcnow() + datetime.timedelta(seconds=time), reason = reason)

        #   Clear some memory
        del member, reason, time
        del ch

        return

    @member.command()
    async def lift(self, ctx:d.ApplicationContext, member:d.Member):

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
    async def kick(self, ctx:d.ApplicationContext, member:d.Member, *, reason:d.Option(str, "A reason to kick the member", required = True)):

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
    async def announcement(self, ctx:d.ApplicationContext):

        """
            Community announcements

        """
        modal = Channel(title = "Channel Announcement")
        await ctx.send_modal(modal)
        return

    @member.after_invoke
    async def clear_memory(self, ctx: d.ApplicationContext):

        #   Clearing embeds
        self.embed.clear_fields()
        self.embed.remove_image()
        self.embed.remove_author()
        self.embed.remove_footer()
        self.embed.description = ""
        self.embed.remove_thumbnail()
        self.embed.color = Colour.dark_purple()

        del ctx #   Clearing some memory
        return
