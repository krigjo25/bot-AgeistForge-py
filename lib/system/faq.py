#   Frequently Asked Questions Module
from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories
from discord import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option

from lib.utils.embed import EmbedFactory
from lib.utils.logger_config import UtilsWatcher
logger = UtilsWatcher(name="FAQ") 
logger.file_handler()

class FrequentlyAskedQuestions(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot

        return

    help_group = SlashCommandGroup(name = "help", description = "Help Commands for the bot")
    
    @help_group.command(name = "modules", description="Bot command menu")     #   type: ignore
    async def help_menu(self, ctx:ApplicationContext, arg:Option(str, "Optional: Enter a module's Name", required=False) = None): #   type: ignore
    
        #embed = EmbedFactory()
        match str(arg).lower():
            case "member module": embed = self.member_module()
            case "community module": embed = self.community_module()
            case "channel module": embed = self.forum_moderation_module()
            case _: embed = self.main_response(ctx) #   type: ignore

        await ctx.respond(embed = embed) #   type: ignore

    @staticmethod
    def main_response(ctx:ApplicationContext):

        fields = dict[str, str]()
        dictionary = dict[str, str]()
        
        dictionary['title'] = "Bot Command Menu"
        
        dictionary['description'] = "This is the main help menu for the bot. It provides a list of available modules and their commands."

        if ctx.author.guild_permissions.moderate_members:   #   type: ignore
            fields['Member Module'] = "List of Available Moderation commands."
        
        if ctx.author.guild_permissions.manage_channels:    #   type: ignore
            fields['Channel Module'] = "List of Available Channel commands."
        
        if ctx.author.guild_permissions.manage_roles:       #   type: ignore
            fields['Role Module'] = "List of Available Role commands."

        
        if ctx.author.guild_permissions.administrator:      #   type: ignore
            fields['Administration Module'] = "List of Available Administration commands."
        fields['Community Module'] = "List of Available Community commands."

        embed = EmbedFactory.info(dictionary=dictionary, fields = fields, team="Support")
        return embed

    @staticmethod
    def community_module() -> Embed:
        
        embed = EmbedFactory()
        prefix = "/community"
        
        dictionary = {
            'title': 'Community Module',
            'description': 'This module provides commands for managing the community in the server.',
        }
        fields = dict[str, str]()
        fields[f'{prefix} support'] = "- Provides support for the community"
        fields[f'{prefix} report'] = "- Reports an issue in the community"
        fields[f'{prefix} bug'] = "- Reports a bug / issue with the community bots / game"

        embed = embed.create_embed(dictionary, fields=fields)
        return embed
    
    @staticmethod
    def forum_moderation_module() -> Embed:

        embed = EmbedFactory()
        prefix = "/channel"
        
        dictionary = {
            'title': 'Channel Module',
            'description': 'This module provides commands for managing channels in the server.',
        }
        fields = dict[str, str]()
        fields[f'{prefix} Hide'] = "- Hides the given channel"
        fields[f'{prefix} Lock'] = "- Locks the given channel"
        fields[f'{prefix} Unlock'] = "- Unlocks the given channel"
        fields[f'{prefix} Rename'] = "- Renames the given channel"
        fields[f'{prefix} delete'] = "- Deletes a channel from the server"
        fields[f'{prefix} SetTopic'] = "- Sets the topic of the given channel"
        fields[f'{prefix} clear'] = "- Clears the messages in the given channel"
        fields[f'{prefix} SetSlowmode'] = "- Sets the slowmode of the given channel"
        fields[f'{prefix} Create'] = "- Creates a new channel with default settings (hidden)"

        embed = embed.info(dictionary, fields=fields)
        return embed
    
    @staticmethod
    def member_module():

        embed = EmbedFactory()
        prefix = "/channel"
        
        dictionary = {
            'title': 'Member Moderation Module',
            'description': 'This module provides commands for managing channels in the server.',
        }
        fields = dict[str, str]()
        fields[f'{prefix} ban'] = '- Bans a user from the server'
        fields[f'{prefix} unban'] = '- Unbans a user from the server'
        fields[f'{prefix} warn'] = '- Warns a user in the server'
        fields[f'{prefix} lift'] = '- Lifts the mute from a user'
        fields[f'{prefix} kick'] = '- Kicks a user from the server'
        fields[f'{prefix} sush'] = '- Mutes a user from using the server'
        
        embed = embed.info(dictionary, fields=fields)
        return embed

    @staticmethod
    def role_module() -> Embed:
        prefix = "/role"

        dictionary = dict[str, str]()
        dictionary['title'] = 'Administration Module'
        dictionary['description'] = 'This module provides commands for managing the server.'

        fields = dict[str, str]()
        fields[f'{prefix} rename'] = "- Renames a role in the server"
        fields[f'{prefix} delete'] = "- Deletes a role from the server"
        fields[f'{prefix} list'] = "- Lists all the roles in the server"
        fields[f'{prefix} add'] = "- Adds a role to a user in the server"
        fields[f'{prefix} create'] = "- Creates a new role with default settings"
        fields[f'{prefix} remove'] = "- Removes a role from a user in the server"
        fields[f'{prefix} info'] = "- Provides information about a role in the server"
        fields[f'{prefix} set_permissions'] = "- Sets the permissions of a role in the server"
        

        embed = EmbedFactory.create_embed(dictionary, fields=fields)
        return embed