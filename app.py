import os
from dotenv import load_dotenv

#    Custom library
from lib.system.botSetup import DiscordSetup

load_dotenv()

def RunBot ():

    disc = DiscordSetup()
    disc.system_setup()
    #disc.ModerationSetup()

    disc.bot.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
        RunBot()
