
#   Python Repositories
import datetime

#   Discord Repositories
from discord.ext import  commands
from discord import utils, SlashCommandGroup, ApplicationContext, Option, Permissions, Forbidden, HTTPException, InvalidArgument

from lib.modal.channel import Channel
from lib.utils.embed import EmbedFactory
from lib.utils.exceptions import ExceptionHandler
from lib.utils.logger_config import CommandWatcher
logger = CommandWatcher(name="Channel Moderation")
logger.file_handler()

class ChannelModeration(commands.Cog):

    """
        Commands for Moderators with manage_channels & manage_messages
    """

    def __init__(self, bot:commands.Bot):

        self.bot = bot
        self.now = datetime.datetime.now()

    
    #   Slash command group
    channel = SlashCommandGroup(name = "channel", description = "Create something", default_member_permissions = Permissions(manage_channels = True))
    
    @channel.before_invoke  # type: ignore
    async def check_channel(self, ctx:ApplicationContext):

        ch = "auditlog"

        category = utils.get(ctx.guild.categories, name = ".log")
        channel = utils.get(ctx.guild.text_channels, name = "auditlog") #  Fetch channel
        
        if not category:
            await self.create_category(ctx, ".log", "Automatically generated category for the auditlog channel")

        if not channel:
            await self.create_channel(ctx, ch, "Automatically generated channel for admin / moderator logging")

        return

    @channel.command(name = "create", description = "Create a channel") # type: ignore
    async def create(self, ctx:ApplicationContext):

        """
            Creating a channel
        """
        modal = Channel(title = "Custom-Channel")
        await ctx.send_modal(modal)
        """
        arg = [{ #  Initializing a list with the parameters
                "channeltype":channeltype, "channel_name": name, "category":category, "channel_permissions": perm,
                "slow_mode": delay,  "topic":reason.get("topic"), "reason":reason.get("reason"), # Text channels
                "nsfw": bool(age_restricted), "bitrate": bitrate, "user_limit": user_limit, "channel_roles":role #  Voice and stage channels
                }]

        for i in arg:#   Fetch the channel from the guild
            
            self.create_category(ctx, i["category"], i["reason"])
            self.create_channel(ctx, i["channel_name"], i["reason"])
            
            role = utils.get(ctx.guild.roles, name = i["channel_roles"])

        try :#   Checking if the condition below is met, if the condition is met then raise exception
 
            if str(channeltype) not in ["forum", "text", "voice", "stage",  ]: raise Exception(" channeltype argument, has only four types, (forum / text / voice or stage )")
            if not chlog : raise Exception("Channel auditlog does not exists")

            for i in arg:
                if i["slow_mode"] < 0: raise ValueError("**delay** argument has to be greater than 0")
                if i["bitrate"] < 0: raise ValueError("Bitrate argument has to be  equal (or grater) to 0")
                 
        except (ValueError, TypeError, Exception) as e:#   If something goes wrong output a message

            self.embetitle = "An Exception Occured"
            self.embedescription = f"{e}"
            self.embecolor = Colour.dark_red()
            self.embetimestamp = self.now
            await ctx.respond(embed = self.embed)

            return

        else:#   If everythings fine, continue 

            for i in arg:
                
                if i["category"] != None:#   Automatically creates a category if it does not exists
                    if not category :await ctx.guilcreate_category_channel(name = i["category"], reason = "User implied category, did not exist.")
                    else:
                        for j in ctx.guilcategories:
                            if category == j.name: i["category"] = int(j.id)

                if i["channel_permissions"] == None: i["channel_permissions"] = await ChannelPermissions().SelectPermissions(ctx, i["channel_permissions"])
                else:i["channel_permissions"] = await ChannelPermissions().SelectPermissions(i["channel_permissions"], role)

                match str(i["channeltype"]).lower(): #   Matching the type of channel

                    case "forum":

                        try: await ctx.guilcreate_forum_channel(name = i["channel_name"], category = utils.get(ctx.guilcategories, name = i["category"]), snsfw = i["nsfw"], slowmode_delay = i["slow_mode"], topic = i["topic"], reason = i["reason"], overwrites = dict(i["channel_permissions"]))
                        except (Forbidden, HTTPException, InvalidArgument) as e: 

                            self.embetitle = "An Exception Occured"
                            self.embedescription = f"{e}"
                            self.embecolor = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

                    case "text":
                        try :await ctx.guilcreate_text_channel(name = i["channel_name"], category = utils.get(ctx.guilcategories, name = i["category"]), nsfw = i["nsfw"], slowmode_delay = i["slow_mode"], topic = i["topic"], reason = i["reason"], overwrites = dict(i["channel_permissions"]))
                        except (Forbidden, HTTPException, InvalidArgument) as e: 

                            self.embetitle = "An Exception Occured"
                            self.embedescription = f"{e}"
                            self.embecolor = Colour.dark_red()
                            await ctx.respond(embed = self.embed)

                            return

                    case "voice":
                        try: await ctx.guilcreate_voice_channel(name = i["channel_name"], category = utils.get(ctx.guilcategories, name = i["category"]),bitrate = i["bitrate"], user_limit = i["user_limit"], topic = i["topic"], reason = i["reason"], overwrites = i["channel_permissions"])
                        except (Forbidden, HTTPException, InvalidArgument) as e: 

                            self.embetitle = "An Exception Occured"
                            self.embedescription = f"{e}"
                            self.embecolor = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

                    case "stage":
                        try: await ctx.guilcreate_stage_channel(name = i["channel_name"], category = utils.get(ctx.guilcategories, name = i["category"]), topic = i["topic"], reason = i["channel_permissions"])
                        except (Forbidden, HTTPException, InvalidArgument) as e: 

                            self.embetitle = "An Exception Occured"
                            self.embedescription = f"{e}"
                            self.embecolor = Colour.dark_red()
                            ctx.respond(embed = self.embed)

                            return

            self.embecolor = Colour.dark_red()
            self.embetimestamp = datetime.datetime.now()
            self.embetitle = f"{ctx.author.name} has created a  {str(channeltype).capitalize()} Channel, called **\"{name}\"**"

            await chlog.send(embed=self.embed)

        #   Clearing some space
        del name, bitrate, category
        del delay, user_limit, role
        del topic, reason, age_restricted
        del channeltype, chlog, ch, arg

        return
        """

    @channel.command(name = "delete", description = "Delete a channel") # type: ignore
    async def delete(self, ctx:ApplicationContext, ch:Option(str, "Channel name", required = True)):

        """
            #   Delete a channel

            #   Fetch both channels
            #   Check if they exist
            #   Delete the channel
        """

        await self.check_channel(ctx)# Calling the function manually
        
        #   Fetch channels
        ch = utils.get(ctx.guilchannels, name = ch)
        chlog = utils.get(ctx.guilchannels, name = "auditlog")

        try:   # If one of the channels does not exist raise exception
            if not chlog: raise Exception(f"Channel \"{chlog}\" does not exists")
            if not ch: raise Exception(f"Channel \"{chlog}\" does not exists")

        except Exception as e: 
            self.embetitle = "An Exception Occured"
            self.embedescription = e
            ctx.send(emed = self.embed)
            return

        self.embecolor = Colour.dark_red()
        self.embetimestamp = datetime.datetime.now()
        self.embetitle = f"{ctx.author.name} has deleted the channel\"**{ch}**\""

        await chlog.send(embed=self.embed)

        ctx.send_response
        await ctx.channel.delete()
        del ch, chlog # Clear memory
        return 

    @channel.command(name = "modify", description = "Modify a channel") # type: ignore
    async def modify(self, ctx:ApplicationContext, channeltype, name, age_restricted = False, archived = False, category = None, delay = 0, locked = False, newname = None, overwrites = None, reason = None, region = None, require_tags = False, thread_slowmode = 0, topic = None, quality = None): #   Modify a channel

        ch = utils.get(ctx.guilchannels, name = name) #   Fetching the channel

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
            self.embetitle = "An Exception Occured"
            self.embedescription = f"{e}"
            self.embecolor = Colour.dark_red()
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
                    except (Forbidden, HTTPException, InvalidArgument) as e: 

                        self.embetitle = "An Exception Occured"
                        self.embedescription = f"{e}"
                        self.embecolor = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "text" : 
                    try : await ctx.channel.edit(reason = i["reason"], name = i["name"], topic = i["topic"], nsfw = i["nsfw"], sync_permissions = i["sync_permissions"], category = i["category"], slowmode_delay = i["slow_mode"], default_thread_slowmode_delay=i["default_thread_slowmode"], require_tag = i["require_tag"])
                    except (Forbidden, HTTPException, InvalidArgument) as e: 

                        self.embetitle = "An Exception Occured"
                        self.embedescription = f"{e}"
                        self.embecolor = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "voice" : 
                    try : await ctx.channel.edit(name = i["name"], topic = i["topic"], reason = i["reason"])
                    except (Forbidden, HTTPException, InvalidArgument) as e: 

                        self.embetitle = "An Exception Occured"
                        self.embedescription = f"{e}"
                        self.embecolor = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "stage" : 
                    try : await ctx.channel.edit(reason = i["reason"], name = i["name"], topic = i["topic"], nsfw = i["nsfw"], sync_permissions = i["sync_permissions"], category = i["category"], slowmode_delay = i["slow_mode"], default_thread_slowmode_delay=i["default_thread_slowmode"], require_tag = i["require_tag"])
                    except (Forbidden, HTTPException, InvalidArgument) as e: 

                        self.embetitle = "An Exception Occured"
                        self.embedescription = f"{e}"
                        self.embecolor = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

                case "category": 
                    try: await ctx.channel.edit(name = name, archived = i["archived"], slowmode_delay=i["slow_mode"], reason = i["reason"])
                    except (Forbidden, HTTPException, InvalidArgument) as e: 

                        self.embetitle = "An Exception Occured"
                        self.embedescription = f"{e}"
                        self.embecolor = Colour.dark_red()
                        ctx.respond(embed = self.embed)

                        return

        return

    @channel.command(name = "clear", description = "Clear a channel")   # type: ignore
    async def clear(self, ctx:ApplicationContext, name:str, x:Option(int, "Number of messages to clear", default = 100, min_value = 1, max_value = 1000)):

        """
            #   Initializing the channels
            #   Checking wheter the values are correct or not
            #   Print a message
            #   Clearing a selected chat
        """

        
        ch = utils.get(ctx.guilchannels, name = name)#   Fetch channel

        try :#   if channel does not exits

            if not ch : raise Exception(f"Channel \"{ch}\" does not exist in the server")
            elif not chlog : raise Exception("Could not find the auditlog channel")

            if str(x).isdigit():  
                x = int(x)
                if x < 0 or x > 1000: raise Exception("Choose an integer between 1-1000")
            else : raise Exception("You can not use alphabetical or ghlupical letters")


        except Exception as e: # Handle exceptions

            self.embecolor = Colour.dark_red()
            self.embetitle = f"An Exception Occured"
            self.embedescription = f'The channel {ch}, were not cleared as requested due to\n{e}'
            await ctx.send(embed = self.embed)

            del ch, chlog, x, name  #   Clear some memory
            return

        #   Prepare & send the embed message
        self.embecolor = Colour.dark_red()
        self.embetimestamp = datetime.datetime.now()
        self.embetitle = f"{ctx.author.name} has cleared {x} chat lines in {ch} channel."
        await chlog.send(embed = self.embed)

        await ctx.channel.purge(limit=x)#   Remove content from the channel
        del ch, chlog, x, name  #   Clear some memory

        return
    
    @staticmethod
    async def create_category(ctx:ApplicationContext, category:str, reason:str):
        """
            #   Create a category for the auditlog channel
        """
        try:
            if not category: raise Exception("Category name can not be empty")
            elif len(category) > 100: raise Exception("Category name can not be longer than 100 characters")

        except Exception as e:
            embed = EmbedFactory.exception(e)

            ctx.respond(embed = embed)

        else:
            await ctx.guild.create_category(name = category, reason = reason)

    @staticmethod
    async def create_channel(ctx:ApplicationContext, name:str, channel_type:str, permissions:str,reason:str):
        """
            #   Create a channel
        """
        ch = utils.get(ctx.guild.channels,  name = name)

        try:
            if ch: raise Exception(f"Channel \"{ch}\" Already exists in the server")
            if len(name) > 100: raise Exception("Channel name can not be longer than 100 characters")

        except Exception as e:
            embed = EmbedFactory.exception(e)

            ctx.respond(embed = embed)

        else:
            #   Create a channel
            await ctx.guild.create_text_channel(name = name, reason = reason)
        
    @staticmethod
    async def auditlog(ctx:ApplicationContext, name:str, reason:str):
        """
            #   Audit log for the channel moderation commands
        """
        ch = utils.get(ctx.guild.channels,  name = name)
        try :
            if not ch : raise ExceptionHandler(f"Channel \"{ch}\" does not exist in the server")

        except ExceptionHandler as e:
            embed = EmbedFactory.exception(e)

            ctx.respond(embed = embed)

        else:
            #   Prepare & send the embed message
            dictionary = dict[str, str]()
            dictionary["title"] = f"Channel Moderation Audit Log"
            dictionary["message"] = f"Channel moderation commands were executed by {ctx.author.name} in {ctx.channel.name} channel."
 
            embed = EmbedFactory.warning(e)

            await ch.send(embed = embed)

