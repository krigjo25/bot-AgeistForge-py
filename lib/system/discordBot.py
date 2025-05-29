#   Discord Bot
#   version       :   0.1.0 Beta
#   License      :   GNU General Public License v3.0

#   Discord Repositories
import discord as d, sys, os
from discord.ext import commands
from discord.message import Message

from dotenv import load_dotenv
load_dotenv()

#   custom Repositories
from lib.utils.logger_config import AppWatcher

logger = AppWatcher(name="DISCORD-APP", dir=".logs")
logger.file_handler()

class DiscordBot(commands.Bot):


    def __init__(self, command_prefix="None", help_command=None, description=None, strip_after_prefix = True, owner_id = 340540581174575107, **options):#   type: ignore    
        super().__init__(command_prefix = command_prefix, help_command=help_command, description=description, strip_after_prefix = strip_after_prefix, owner_id = owner_id, **options)#   type: ignore    

        return

    async def on_ready(self):
        logger.info(f"---- Environment Check: ----\n Python Executeable {sys.executable}\n Working Directory: {os.getcwd()}\n * Application Module Info:\nVersion of Discord :{d.__version__}\n Discord module loaded from: {d.__file__}")    #   type: ignore
        
        try:
            await self.wait_until_ready()
            await self.sync_commands() #   type: ignore

        except AttributeError as e:
            logger.critical(f"An AttributeError occured !\n {e}\n")

        except Exception as e:
            logger.error(f"An unexpected error occurred:\n {e}\n")
        

        else:
            svr = [i for i in self.guilds]
            for i in svr: logger.info(f'{self.user.name} has establized an connection to {i}') #   type: ignore

        logger.info
    async def on_message(self, message:Message):

        await self.process_commands(message)
