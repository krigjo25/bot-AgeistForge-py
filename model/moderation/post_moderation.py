#   Python Repositories
import datetime
import asyncio
import humanfriendly as hf

#   Discord Repositories
import discord as d
from discord import utils
from discord.embeds import Embed, Colour
from discord.ext.commands import  Cog

#   Dicitionary
from model.dictionaries.permissions import ChannelPermissions
from model.moderation.model import Channel, Role

class Administrator(Cog):

    """
            Copyright (C) 2023  Kristoffer Gjøsund

        Administrator Commands

        >   Creation Date   : 21.02-23
        >   Last update     :

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        Commands for Moderators with administrator

    """
    def __init__(self, bot):

        self.bot = bot
        self.now = datetime.datetime.now().strftime('%a, %d.%b-%y')
        self.embed = Embed(color=d.Colour.dark_red())

        return

    ban = d.SlashCommandGroup(name = "ban", description = "Server Administrator", default_member_permissions = d.Permissions(administrator = True))


    @ban.command()  #   List of banned members
    async def list(self, ctx:d.ApplicationContext):
        """
            #   List of banned members
        """
        #   Initializing a list
        banned = []

        try:

            #   Iterating over the ctx.guild bans
           async for entry in ctx.guild.bans():

                dictionary = { "name": entry.user.name,
                                "discriminator": entry.user.discriminator,
                                "reason": entry.reason}

                banned.append(dictionary)

        except Exception as e : print(e)
        else:

            #   Prepare the ebeded message
            self.embed.title = 'List of banned server members'
            self.embed.description =' User name & discriminator | Reason'
            self.embed.color = Colour.dark_red()

            if banned:

                for i in banned: self.embed.add_field(name= f'{i["name"]}#{i["discriminator"]}', value = f'{i["reason"]}', inline = True)

            else: self.embed.description = "Noone banned yet, Hurray :party:"

            self.embed.add_field(name= f'Total banned users {len(banned)}\n== End of List ==', value = ':-)', inline = False)
            await ctx.send(embed=self.embed)

        #   Clear some space
        del banned, entry, dictionary

        return

    @ban.command()    #   Prohbit a user to enter the channel again
    async def member(self, ctx:d.ApplicationContext, member:d.Member, *, reason:d.Option(str, "Reason for the ban", required = True)):

        """
            #   Ban a server member
            #   Reason required
            #   Notify the user about the ban
            #   Cheeck for a moderationlog channel
            #   Log the ban

        """

        ch = utils.get(ctx.guild.channels, name='auditlog') #   Fetch channel
        try :
            if not ch : raise Exception(f"Could not find \"**auditlog**\"")
            

        except Exception as e :

            self.embed.color = Colour.dark_red()
            self.embed.title =f"An Exception Occured"
            self.embed.description = f"{e}\n"
            await ctx.send(embed = self.embed)

        else:

            #   Log the ban
            self.embed.color = Colour.dark_red()
            self.embed.description = f"due to {reason}"
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f'{member} has been banned by {ctx.author}'
            
            await ch.send(embed=self.embed)

            #   Notify the user about the ban & ban the member
            message = f'the Administrator Team has decided to probhid you for using  **{ctx.guild.name}** \n \n Due to :\n **{reason}**'
            await member.send(message)
            await member.ban(reason=reason)

            #   Clear some memory
            del reason, message
            del member, ch

        return

    @ban.command()#   Allows a user to enter the channel again
    async def unban(self, ctx:d.ApplicationContext, *, member:d.Member):

        ch = utils.get(ctx.guild.channels, name='auditlog') #   Fetch channel

        try :
            if not ch : raise Exception("auditlog channel does not exits")

        except Exception as e:

            #   Prepare emed message
            self.embed.color = Colour.dark_red()
            self.embed.title = f"An Exception Occured"
            self.description = f"{e}, try again"
            await ctx.send(embed = self.embed)

            del ch, member
            return

        else:
            
            #   Log the unban
            self.embed.color = Colour.dark_red()
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f"{member.name} has been unbanned by {ctx.author.name}"

            await ch.send(embed=self.embed)

            #  Unban the given member
            async for entry in ctx.guild.bans():
                if entry.user.name == member.name: await ctx.guild.unban(entry.user)

            await member.send(f"Greetings, {member}, the administrator team has decided to unban you from {ctx.guild}\n You are now welcome back to the server.")

        del member, ch

        return

    @ban.before_invoke
    async def CheckModChannel(self, ctx):

        print("test, before_invoke")

        return

    @ban.after_invoke
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

    async def Auditlog(self, ctx, limit = 3): pass

class ChannelModeration(Cog):

    """
        Commands for Moderators with manage_channels & manage_messages
        
        #   Author : Krigjo25
        #   Creation Date :  18.02-23
        #   last update :    20.02-23

        #   Create channels
        #   Delete channels
        #   modify channels
    """

    def __init__(self, bot):

        self.bot = bot
        self.embed = Embed()
        self.now = datetime.datetime.now()

        return
    
    #   Slash command group
    channel = d.SlashCommandGroup(name = "channel", description = "Create something", default_member_permissions = d.Permissions(manage_channels = True))
    @channel.command()
    async def uselesscommnd(self, ctx:d.ApplicationContext, text = None):
        print(ctx.guild.categories)
        return

    @channel.command()
    async def create(self, ctx:d.ApplicationContext, channeltype:d.Option(str, "eg. (forum / text / voice / stage)", required = True), name:d.Option(str, "Name of the channel eg. (general-talk, general)", required = True), age_restricted:d.Option(bool, "Is the channel restricted for users below 18? (True / False)", default = False) , bitrate:d.Option(int, "bitrate (voic channel)", required = False, default = 0),  category:d.Option(str, "Name of the category. (GENERAL, GENERAL TALK)", required = False, default = None), delay: d.Option(int,"Slowmode counter(s)", default = 0), user_limit:d.Option(int,"User limitation for the channel (Voice channel parameter)", required = False, default = 0), perm:d.Option(str, "permissions (custom / member / moderator / admin)", required = False, default = None), role:d.Option(str, "Server role name", required = False), *topic:d.Option(str, "Tell the users about the channel subject (general-talk, general)", required = False, default = None), **reason:d.Option(str, "Reason for creation of the channel", required = False, default = None)):

        """
            Creating a channel

            

            #   Checking the condtiions
            #   Create a channel
        """

        await self.check_channel(ctx)# Calling the function manually
        arg = [{ #  Initializing a list with the parameters
                "channeltype":channeltype, "channel_name": name, "category":category, "channel_permissions": perm,
                "slow_mode": delay,  "topic":reason.get("topic"), "reason":reason.get("reason"), # Text channels
                "nsfw": bool(age_restricted), "bitrate": bitrate, "user_limit": user_limit, "channel_roles":role #  Voice and stage channels
                }]

        for i in arg:#   Fetch the channel from the guild
            chlog = utils.get(ctx.guild.channels, name = "auditlog")
            ch = utils.get(ctx.guild.channels, name = i["channel_name"])
            category = utils.get(ctx.guild.categories, name = i["category"])
            role = utils.get(ctx.guild.roles, name = i["channel_roles"])

        try :#   Checking if the condition below is met, if the condition is met then raise exception
 
            if str(channeltype) not in ["forum", "text", "voice", "stage",  ]: raise Exception(" channeltype argument, has only four types, (forum / text / voice or stage )")
            if not chlog : raise Exception("Channel auditlog does not exists")

            for i in arg:
                if i["slow_mode"] < 0: raise ValueError("**delay** argument has to be greater than 0")
                if i["bitrate"] < 0: raise ValueError("Bitrate argument has to be  equal (or grater) to 0")
                 
        except (ValueError, TypeError, Exception) as e:#   If something goes wrong output a message

            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}"
            self.embed.color = Colour.dark_red()
            self.embed.timestamp = self.now
            await ctx.respond(embed = self.embed)

            return

        else:#   If everythings fine, continue 

            for i in arg:
                
                if i["category"] != None:#   Automatically creates a category if it does not exists
                    if not category :await ctx.guild.create_category_channel(name = i["category"], reason = "User implied category, did not exist.")
                    else:
                        for j in ctx.guild.categories:
                            if category == j.name: i["category"] = int(j.id)

                if i["channel_permissions"] == None: i["channel_permissions"] = await ChannelPermissions().SelectPermissions(ctx, i["channel_permissions"])
                else:i["channel_permissions"] = await ChannelPermissions().SelectPermissions(i["channel_permissions"], role)

                match str(i["channeltype"]).lower(): #   Matching the type of channel

                    case "forum":

                        try: await ctx.guild.create_forum_channel(name = i["channel_name"], category = utils.get(ctx.guild.categories, name = i["category"]), snsfw = i["nsfw"], slowmode_delay = i["slow_mode"], topic = i["topic"], reason = i["reason"], overwrites = dict(i["channel_permissions"]))
                        except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                            self.embed.title = "An Exception Occured"
                            self.embed.description = f"{e}"
                            self.embed.color = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

                    case "text":
                        try :await ctx.guild.create_text_channel(name = i["channel_name"], category = utils.get(ctx.guild.categories, name = i["category"]), nsfw = i["nsfw"], slowmode_delay = i["slow_mode"], topic = i["topic"], reason = i["reason"], overwrites = dict(i["channel_permissions"]))
                        except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                            self.embed.title = "An Exception Occured"
                            self.embed.description = f"{e}"
                            self.embed.color = Colour.dark_red()
                            await ctx.respond(embed = self.embed)

                            return

                    case "voice":
                        try: await ctx.guild.create_voice_channel(name = i["channel_name"], category = utils.get(ctx.guild.categories, name = i["category"]),bitrate = i["bitrate"], user_limit = i["user_limit"], topic = i["topic"], reason = i["reason"], overwrites = i["channel_permissions"])
                        except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                            self.embed.title = "An Exception Occured"
                            self.embed.description = f"{e}"
                            self.embed.color = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

                    case "stage":
                        try: await ctx.guild.create_stage_channel(name = i["channel_name"], category = utils.get(ctx.guild.categories, name = i["category"]), topic = i["topic"], reason = i["channel_permissions"])
                        except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                            self.embed.title = "An Exception Occured"
                            self.embed.description = f"{e}"
                            self.embed.color = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

            self.embed.color = Colour.dark_red()
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f"{ctx.author.name} has created a  {str(channeltype).capitalize()} Channel, called **\"{name}\"**"

            await chlog.send(embed=self.embed)

        #   Clearing some space
        del name, bitrate, category
        del delay, user_limit, role
        del topic, reason, age_restricted
        del channeltype, chlog, ch, arg

        return

    @channel.command()
    async def delete(self, ctx:d.ApplicationContext, ch:d.Option(str, "Channel name", required = True)):

        """
            #   Delete a channel

            #   Fetch both channels
            #   Check if they exist
            #   Delete the channel
        """

        await self.check_channel(ctx)# Calling the function manually
        #   Fetch channels
        ch = utils.get(ctx.guild.channels, name = ch)
        chlog = utils.get(ctx.guild.channels, name = "auditlog")

        try:   # If one of the channels does not exist raise exception
            if not chlog: raise Exception(f"Channel \"{chlog}\" does not exists")
            if not ch: raise Exception(f"Channel \"{chlog}\" does not exists")

        except Exception as e: 
            self.embed.title = "An Exception Occured"
            self.embed.description = e
            ctx.send(emed = self.embed)
            return

        self.embed.color = Colour.dark_red()
        self.embed.timestamp = datetime.datetime.now()
        self.embed.title = f"{ctx.author.name} has deleted the channel\"**{ch}**\""

        await chlog.send(embed=self.embed)

        ctx.send_response
        await ctx.channel.delete()
        del ch, chlog # Clear memory
        return 

    @channel.command()
    async def modify(self, ctx:d.ApplicationContext, channeltype, name, age_restricted = False, archived = False, category = None, delay = 0, locked = False, newname = None, overwrites = None, reason = None, region = None, require_tags = False, thread_slowmode = 0, topic = None, quality = None): #   Modify a channel

        await self.check_channel(ctx)# Calling the function manually
        ch = utils.get(ctx.guild.channels, name = name) #   Fetching the channel

        try :#  Checking for exceptions

            if str(channeltype).isdigit() : raise Exception("channeltype argument, can not be integers") #   Checking if the channelType contains integers
            elif str(channeltype) not in ["forum","text", "voice", "category", "stage" ]: raise Exception(" channeltype argument, has only four types, (forum / text / voice or category)")

            #   Boolean values
            if str(archived).isalpha():
                if str(archived) == "True": archived == True
                elif str(archived) == "False": archived == False
                else : raise TypeError("archived argument accepts only boolean expression \"True\" or \"False\"")
            else : raise TypeError("archived argument accepts only boolean expression \"True\" or \"False\" ")

            if str(age_restricted).isalpha():
                if str(age_restricted) == "True": age_restricted == True
                elif str(age_restricted) == "False": age_restricted == False
                else : raise TypeError("age_restricted argument accepts only boolean expression \"True\" or \"False\"") 
            else: raise TypeError("age_restricted accepts only boolean expression \"True\" or \"False\"")

            if str(locked).isalpha():
                if str(locked) == "True": locked == True
                elif str(locked) == "False": locked == False
                else : raise TypeError("locked argument accepts only boolean expression \"True\" or \"False\"") 
            else: raise TypeError("locked argument accepts only boolean expression \"True\" or \"False\"")

            if str(require_tags).isalpha():
                if str(require_tags) == "True": require_tags == True
                elif str(require_tags) == "False": require_tags == False
                else : raise TypeError("require_tags argument accepts only boolean expression \"True\" or \"False\"") 
            else: raise TypeError("require_tags argument accepts only boolean expression \"True\" or \"False\"")

            #   Integer values
            if str(thread_slowmode).isdigit(): 
                if int(thread_slowmode) < 0: raise ValueError("thread_slowmode argument accepts only integers greater or equal to zero")
            else: raise ValueError("thread_slowmode argument accepts only integers greater or equal to zero")

            if str(delay).isdigit(): 
                if int(delay) < 0: raise ValueError("delay argument accepts only integers greater or equal to zero")
            else: raise ValueError("delay argument accepts only integers greater or equal to zero")

            if not ch: raise Exception("Channel does not exist")
    
        except (ValueError, TypeError, Exception) as e :
            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}"
            self.embed.color = Colour.dark_red()
            ctx.respond(embed = self.embed)
            return


        arg = [{#   Adding values into a list
                "archived": archived, "category":category,
                "default_thread_slowmode": thread_slowmode,
                "locked":locked, "name":newname,"nsfw":age_restricted,
                "overwrites":overwrites,"require_tag": require_tags,
                "reason":reason, "region":region, "slow_mode": delay,
                "topic":topic,"video_quality":quality,
                

                }]
        
        for i in arg: # for each element in the dictionary, change values if None
            if i["name"] == None: i["name"] == ch.name 
            elif i["overwrites"] == None: i["overwrites"] == ch.overwrites
            elif i["topic"] == None: i["name"] == ch.topic
            elif i["category"] == None: i["category"] = ch.category
            elif i["region"] == None: i["region"] == ch.rtc_region  # Voice
            elif i["video_quality"] == None: i["video_quality"] == ch.video_quality_mode    #   Voice
            elif i["nsfw"] == False: i["nsfw"] == ch.nsfw # text
            elif i["slow_mode"] == 0: i["slow_mode"] == ch.slowmode_delay # text
            elif i["default_thread_slowmode"] == 0: i["default_thread_slowmode"] == ch.default_thread_slowmode_delay #text
            elif i["sync_permissions"] == False: i["sync_permissions"] == ch.permissions_synced
            elif i["require_tag"] == False: i["require_tag"] == ch.requires_tag

        #   Clear some memory
        del name, newname, topic
        del reason, category


        for i in arg:
            match channeltype:  #   Matching the type of channel
                case "forum": 
                    try : await ctx.channel.edit(reason = i["reason"], name = i["name"], nsfw = i["nsfw"], overwrites = i["overwrites"])
                    except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                        self.embed.title = "An Exception Occured"
                        self.embed.description = f"{e}"
                        self.embed.color = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "text" : 
                    try : await ctx.channel.edit(reason = i["reason"], name = i["name"], topic = i["topic"], nsfw = i["nsfw"], sync_permissions = i["sync_permissions"], category = i["category"], slowmode_delay = i["slow_mode"], default_thread_slowmode_delay=i["default_thread_slowmode"], require_tag = i["require_tag"])
                    except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                        self.embed.title = "An Exception Occured"
                        self.embed.description = f"{e}"
                        self.embed.color = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "voice" : 
                    try : await ctx.channel.edit(name = i["name"], topic = i["topic"], reason = i["reason"])
                    except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                        self.embed.title = "An Exception Occured"
                        self.embed.description = f"{e}"
                        self.embed.color = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "stage" : 
                    try : await ctx.channel.edit(reason = i["reason"], name = i["name"], topic = i["topic"], nsfw = i["nsfw"], sync_permissions = i["sync_permissions"], category = i["category"], slowmode_delay = i["slow_mode"], default_thread_slowmode_delay=i["default_thread_slowmode"], require_tag = i["require_tag"])
                    except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                        self.embed.title = "An Exception Occured"
                        self.embed.description = f"{e}"
                        self.embed.color = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "category": 
                    try: await ctx.channel.edit(name = name, archived = i["archived"], slowmode_delay=i["slow_mode"], reason = i["reason"])
                    except (d.Forbidden, d.HTTPException, d.InvalidArgument) as e: 

                        self.embed.title = "An Exception Occured"
                        self.embed.description = f"{e}"
                        self.embed.color = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

        return

    @channel.command()
    async def clear(self, ctx:d.ApplicationContext, name, x):

        """
            #   Initializing the channels
            #   Checking wheter the values are correct or not
            #   Print a message
            #   Clearing a selected chat
        """

        ch = utils.get(ctx.guild.channels, name = name)#   Fetch channel
        chlog = utils.get(ctx.guild.channels, name = "auditlog")#   Fetch channel

        try :#   if channel does not exits

            if not ch : raise Exception(f"Channel \"{ch}\" does not exist in the server")
            elif not chlog : raise Exception("Could not find the auditlog channel")

            if str(x).isdigit():  
                x = int(x)
                if x < 0 or x > 1000: raise Exception("Choose an integer between 1-1000")
            else : raise Exception("You can not use alphabetical or ghlupical letters")


        except Exception as e: # Handle exceptions

            self.embed.color = Colour.dark_red()
            self.embed.title = f"An Exception Occured"
            self.embed.description = f'The channel {ch}, were not cleared as requested due to\n{e}'
            await ctx.send(embed = self.embed)

            del ch, chlog, x, name  #   Clear some memory
            return

        #   Prepare & send the embed message
        self.embed.color = Colour.dark_red()
        self.embed.timestamp = datetime.datetime.now()
        self.embed.title = f"{ctx.author.name} has cleared {x} chat lines in {ch} channel."
        await chlog.send(embed = self.embed)

        await ctx.channel.purge(limit=x)#   Remove content from the channel
        del ch, chlog, x, name  #   Clear some memory

        return

    @channel.before_invoke
    async def check_channel(self, ctx:d.ApplicationContext):

        print("test, before_invoke")
        ch = ["auditlog", "member-reports", "member-support"]

        category = utils.get(ctx.guild.categories, name = "log")

        if not category:
            category = utils.get(ctx.guild.categories, name = "log")
            await ctx.guild.create_category(name = "log", reason = "")

        for i in ch:
            i = utils.get(ctx.guild.channels, name = i)#  Fetch channel
            if not i: await ctx.channel.create_text_channel(name = i, category = category, reason = "Auto generated channel")

        del ch, i, ctx  #   Clear some memory
        del category

        return

    @channel.after_invoke
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

class MiscModeration(Cog):

    """
        Miscerillious commands
        #   Author : krigjo25
        #   Date :   21.02-23
        #   Last update: 22.02-23

        #   Create a role
        #   Delete a role
        #   modify a role
    """

    def __init__(self, bot):

        self.bot = bot
        self.embed = Embed()
        self.now = datetime.datetime.now().strftime('%H:%M, %d.%b - %y')

        return

    #   Slash command group
    misc = d.SlashCommandGroup(name = "misc", description = "misc moderator commands", default_member_permissions = d.Permissions(manage_channels = True))

    @misc.command()
    async def announcement(self, ctx:d.ApplicationContext):

        """
            Community announcements

        """
        modal = Channel(title = "Channel Announcement")
        await ctx.send_modal(modal)
        return

    @misc.after_invoke
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

class MemberModeration(Cog):

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

    def __init__(self, bot):

        self.bot = bot
        self.now = datetime.datetime.now()
        self.embed = Embed()

        return

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

    @member.command()#  Kick member
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

    @member.before_invoke
    async def check_channel(self, ctx:d.ApplicationContext):

        ch = ["auditlog", "member.-reports"]

        category = utils.get(ctx.guild.categories, name = "log")#   Fetch category

        if not category:#   Create a new category if not exists
            category = utils.get(ctx.guild.categories, name = "log")
            await ctx.guild.create_category(name = "log", reason = "")

        category = utils.get(ctx.guild.categories, name = "log")

        for i in ch: 
            ch = utils.get(ctx.guild.channels, name = i) # Fetch channels
            
            if not ch: #    Create channels for administrators / head moderators
                match i:
                    case "auditlog": await ctx.guild.create_text_channel(name = i, category = category, topic = "A place where head moderator / administrators can monitor moderators", reason = "Auto generated channels for administrators / head moderators")
                    case "members-report": await ctx.guild.create_text_channel(name = i, category = category, topic = "Review reports from members", reason = "Auto generated channels for moderators")

        del ch, i, ctx  #   Clear some memory
        del category

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

class RoleModeration(Cog):

    """
        Commands for Moderators with manage_role

        #   Author : krigjo25
        #   Date :   21.02-23
        #   Last update :

        #   Create a role
        #   Delete a role
        #   Demote a member
        #   Set a member as role
        #   modify a role
    """

    def __init__(self, bot):

        self.bot = bot
        self.embed = Embed()
        self.now = datetime.datetime.now()

        return

    #   Slash command group
    role = d.SlashCommandGroup(name = "role", description = "Role mananger", default_member_permissions = d.Permissions(manage_roles = True))

    #@role.commend()
    async def create(): pass

    @role.command() # delete a role
    async def delete(self, ctx:d.ApplicationContext, role:d.Option(str, "Server role", required = True) ):

        """
            Delete a server role
            #
            #   Checking if there is any channels called 'moderationlog'
            #   Ask the user for comfirmation before removing the role

        """

        await self.check_channel(ctx)# Calling the function manually
        #   Fetch role and channel
        role = utils.get(ctx.guild.roles, name= role)#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try:
            if not role : raise Exception(f"Could not find \"**{role}**\" in the server")
            elif not ch : raise Exception("The channel \"**auditlog**\" were not created")

        except Exception as e:

            self.embed.title = "An Exception Occured"
            self.embed.description = f'{e}, Try again...'
            await ctx.send(embed = self.embed)

            del role, ch#   Clear some memory
            return

        else:   #   Confirming the deletion
            modal = Role(title = "Role Deletion")
            ctx.send_modal(modal)

        del role, ch, modal

        return
 
    @role.command()# remove a member from a role
    async def remove(self, ctx:d.ApplicationContext, member:d.Member, role:d.Option(str, "Server role", required = True), *, reason:d.Option(str, "Reason to remove the member from the role", required = True)):

        """
            Removing the member from the selected role

            #   Fetch the role & audit channel
            #   Checking if there is any channels called 'auditlog'
            #   When the command is invoked, ask the user for a confirmation
            #   Confirmation to remove the user from the role

        """

        await self.check_channel(ctx)# Calling the function manually
        role = utils.get(ctx.guild.roles, name=f'{role}')#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try: 
            if not role : raise Exception(f"Role \"{role}\" Not found")
            if not ch: raise Exception(f"The auditlog channel were not created")

        except Exception as e: 

            self.embed.color = Colour.dark_red()
            self.embed.title = 'An Exception Occured'
            self.embed.description = f"{e}, try again."
            await ctx.send(embed = self.embed)
            return

        else:

            #  Prepare, remove & send
            modal = Role(title = "Remove member")
            ctx.send_modal(modal)

        return

    @role.command() # add someone to a role
    async def add(self, ctx:d.ApplicationContext, member:d.Member, role:d.Option(str, "Server role", required = True)):

        """
            Add a member to given role

            #   Fetch role and channel and check if they actually exists
            #   Except exception if not exists
            #   add member to role
        """
        await self.check_channel(ctx)# Calling the function manually
        role = utils.get(ctx.guild.roles, name=f'{role}')#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try :
            if not role: raise Exception("Role does not exist")
            elif not ch: raise Exception("The channeld \"**auditlog**\" were not created")

        except Exception as e:

            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}, try again"
            await ctx.send(embed = self.embed)

            del role, ch, member
            return
        else:

            #  Prepare, remove, send & Clean up
            self.embed.color = Colour.dark_red()
            self.embed.title = f'{member} has been added to {role} by {ctx.author}'

            await member.add_roles(role)
            await ch.send(embed = self.embed)

        return

    @role.command()#    Modify permissions, roles
    async def modify(self, ctx:d.ApplicationContext, role:d.Option(str, "Server role", required = True), *, reason = None):  return

    @role.before_invoke
    async def check_channel(self, ctx: d.ApplicationContext):

        channel = []
        ch = ["auditlog", "report", "support"]

        try :
            for i in ch:
                if utils.utils.get(ctx.guild.text_channels, name = i): return 


        except TypeError as e: print(e)
        else:

            #   Creating a channel
            perms = {ctx.guild.default_role:d.PermissionOverwrite(view_channel=False)}

            for i in ch:

                #   Prepare and send embeded message
                self.embed.color = Colour.dark_red()
                self.embed.title = f'Auto Generated Channel'



                match i:

                    case "auditlog": 
                        self.embed.description = "Created to have easy accsess to bot commands used by admin / moderator"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                    case "report": 
                        self.embed.description = "Member report channel"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                    case "support": 
                        self.embed.description = "Member support channel"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                self.embed.timestamp = datetime.datetime.now()
                await i.send(embed=self.embed)
    
        #   Clear some memory
        del perms, ch, channel
        self.embed.description =""

        return

    @role.after_invoke
    async def clear_memory(self, ctx: d.ApplicationContext):

        #   Clear some Memory
        self.embed.clear_fields()
        self.embed.remove_image()
        self.embed.remove_author()
        self.embed.remove_footer()
        self.embed.remove_thumbnail()
        self.embed.color = Colour.dark_purple()
        self.embed.description = ""

        return
