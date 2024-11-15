from os import getenv
from dotenv import load_dotenv

#    Custom library
from model.system.botSetup import DiscordSetup

load_dotenv()

def RunBot ():

    disc = DiscordSetup()
    disc.SystemSetup()
    disc.ModerationSetup()

    disc.bot.run(getenv('Token'))

if __name__ == '__main__':
        RunBot()
