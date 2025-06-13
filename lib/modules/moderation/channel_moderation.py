
#   Python Repositories
import datetime

#   Discord Repositories
from discord.ext import  commands
from discord import utils, SlashCommandGroup, ApplicationContext, Option, Permissions, Forbidden, HTTPException, InvalidArgument

from lib.modal.channel import Channel
from lib.utils.embed import EmbedFactory
from lib.utils.logger_config import UtilsWatcher
from lib.utils.moderation import ModerationUtils
from lib.utils.exceptions import ExceptionHandler
logger = UtilsWatcher(name="Channel Moderation")
logger.file_handler()

class ChannelModeration(commands.Cog):

    """
        This class contains commands for managing channels in a Discord server.
        It allows forum moderators to create, delete, modify, and clear channels.
        The commands are grouped under the "channel_group" command group.

    """

    def __init__(self, bot:commands.Bot):

        self.bot = bot
    
    #   Slash command group
    channel_group = SlashCommandGroup(name = "channel", description = "Create something", default_member_permissions = Permissions(manage_channels = True))

    @channel_group.command(name = "create", description = "Create a channel") # type: ignore
    async def create(self, ctx:ApplicationContext):
        
        modal = Channel(title = "Custom-Channel")
        await ctx.send_modal(modal)

    @channel_group.command(name = "delete", description = "Deletes the channel which the user interacts with") # type: ignore
    async def delete(self, ctx:ApplicationContext, reason:Option(str, "Reason for deletion", required = True)):

        """
            Limitations:
                - The commands works only in current channel.
        """
        #   Fetch the function name and split it to get the command name
        modUtils = ModerationUtils()
        func = modUtils.fetch_function_name(self.delete)

        ch = utils.get(ctx.guild.channels, id = ctx.channel.id)

        await modUtils.create_log_entry(ctx, reason, ch, func)
        
        await ctx.respond(f"Command Executed !", ephemeral = True)  
        await ctx.channel.delete(reason = reason) #   Deleting the channel

    @channel_group.command(name = "modify", description = "Modify a channel") # type: ignore
    async def modify(self, ctx:ApplicationContext): #   Modify a channel

        raise NotImplementedError("This feature is not implemented yet")
        """ch = utils.get(ctx.guild.channels, id = ctx.channel.id)

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
        """
    
    @channel_group.command(name = "clear", description = "Clear a channel")   # type: ignore
    async def clear(self, ctx:ApplicationContext, n:Option(int, "Number of messages to clear", default = 100, required = False)):
        """
            Limitations:
                - The commands works only in current channel.
                - The number of messages to clear must be an integer between 1 and 1000.
                - The command can only be used by users with the "manage_channels" permission.
        """

        MIN = 1
        MAX = 1000

        modUtils = ModerationUtils()
        func = ModerationUtils.fetch_function_name(self.clear)

        try:
            if n < MIN or n > MAX: raise ExceptionHandler(f"Choose an integer between {MIN}-{MAX}")

        except ExceptionHandler as e:
            await modUtils.create_error_entry(ctx, e)

        else:
            await ctx.channel.purge(limit=n)
            await modUtils.create_log_entry(ctx, function_name=func, n=n)
            await ctx.respond(f"Cleared {n} messages from the channel.", ephemeral=True)
