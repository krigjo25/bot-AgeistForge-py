#   Discord Bot
#   version       :   0.1.0 Beta
#   License      :   GNU General Public License v3.0

#   Discord Repositories
from discord.ext import commands
from discord.message import Message

#import requests
from sys import api_version


from dotenv import load_dotenv
load_dotenv()

#   custom Repositories
from lib.utils.logger_config import AppWatcher

logger = AppWatcher(name="discord-bot", dir=".logs")
logger.file_handler()

class DiscordBot(commands.Bot):


    def __init__(self, command_prefix='?', help_command=None, description=None, strip_after_prefix = True, owner_id = 340540581174575107, **options):#   type: ignore    
        super().__init__(command_prefix = command_prefix, help_command=help_command, description=description, strip_after_prefix = strip_after_prefix, owner_id = owner_id, **options)#   type: ignore    

        return

        
    async def on_ready(self):

        

        await self.sync_commands()                                      #   type: ignore    
        await self.wait_until_ready()

        logger.info(f'{self.user.name} has connected to Discord!\nCreated with Py-cord.py v{api_version}\n')    #   type: ignore
        svr = [i for i in self.guilds]
        for i in svr: 
            logger.info(f'{self.user.name} has establized an connection to {i}') #   type: ignore

    async def on_message(self, message:Message):

        await self.process_commands(message)
