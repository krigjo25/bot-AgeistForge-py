#   Frequently Asked Questions Module

import os
#   Discord Repositories
from discord import Colour
from discord.embeds import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext, Option

from lib.utils.logger_config import CommandWatcher

from dotenv import load_dotenv
load_dotenv()
logger = CommandWatcher(name="FAQ", dir=".logs") #   type: ignore
logger.file_handler()


class FrequentlyAskedQuestions(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed(color=Colour.dark_purple())

    help_group = SlashCommandGroup(name = "help", description = "Bot Documentation")
    
    @help_group.command(name = "modules", description="Bot command menu", guild_ids=os.getenv("DEV_GUILD"))     #   type: ignore
    async def help_menu(self, ctx:ApplicationContext, arg:Option(str, "Optional: Enter a module's Name", required=False)): #   type: ignore
    
        match str(arg).lower(): #   type: ignore
            case "moderator module": self.forum_moderation_module()
            case "administrator module": self.administration_module()
            case "forum moderator module": self.forum_moderation_module()
            case _: self.main_response(ctx) #   type: ignore

        await ctx.respond(embed = self.base_embed) #   type: ignore

    def main_response(self, ctx:ApplicationContext):
        self.base_embed.title = "Help Menu"
        self.base_embed.description = f""" 
            For assistance with a spesific module, please utilize the command `/help module <module name>`.
            Alternatively, the command `/help module` will return a list of all available modules."""

        if ctx.author.guild_permissions.kick_members:       #   type: ignore
            self.base_embed.add_field(name=f'Moderator Module', value="List of available moderation commands.", inline=True)
        
        if ctx.author.guild_permissions.manage_channels:    #   type: ignore
            self.base_embed.add_field(name=f'Forum Moderator Module', value="List of available forum moderation commands.", inline=True)

        if ctx.author.guild_permissions.administrator:      #   type: ignore
            self.base_embed.add_field(name=f'Administrator Module', value="List of administration commands available to administrators.", inline=True)

    def forum_moderation_module(self):

        self.base_embed.title = 'Forum Moderator Module'
        self.base_embed.color = Colour.dark_purple()

        self.base_embed.add_field(name=f'/clear', value='- Clears messages in a channel', inline=True)
        #self.base_embed.add_field(name=f'/channel Hide', value='- Hides the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Lock', value='- Locks the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Unlock', value='- Unlocks the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Rename', value='- Renames the given channel ', inline=True)
        self.base_embed.add_field(name=f'/channel Delete', value='- Deletes a channel from the server ', inline=True)
        #self.base_embed.add_field(name=f'/channel SetTopic', value='- Sets the topic of the given channel ', inline=True)
        self.base_embed.add_field(name=f'/channel Create', value='- Create a new channel default : hidden ', inline=True)
        self.base_embed.add_field(name=f'/channel Clear', value= '- Clears the given channel Chat:bangbang:', inline=True)
        
        self.base_embed.add_field(name=f'/channel SetSlowmode', value='- Sets the slowmode of the given channel ', inline=True)
    
    def moderation_module(self):

        self.base_embed.title = 'Moderator Module'
        self.base_embed.color = Colour.dark_purple()

        self.base_embed.add_field(name=f'/ban', value='- Bans a user from the server', inline=True)
        self.base_embed.add_field(name=f'/kick', value='- Kicks a user from the server', inline=True)
        self.base_embed.add_field(name=f'/kick', value='- Kicks a user from the server', inline=True)
        

    async def administration_module(self, ctx:ApplicationContext): 
        #   Initializing analysis commands
        #   Initializing auditlog commands
        pass
    
    @help_group.after_invoke #   type: ignore
    async def clear_memory(self, ctx:ApplicationContext):

        #   Clearing embeds
        self.base_embed.clear_fields()                   #   type: ignore
        self.base_embed.remove_image()                   #   type: ignore
        self.base_embed.remove_author()                  #   type: ignore
        self.base_embed.remove_footer()                  #   type: ignore
        self.base_embed.description = ""                 #   type: ignore
        self.base_embed.remove_thumbnail()               #   type: ignore
        self.base_embed.color = Colour.dark_purple()     #   type: ignore