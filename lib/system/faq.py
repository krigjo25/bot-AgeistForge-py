
#   Discord Repositories
import discord as d
from typing import Optional
from discord import Color

from discord.embeds import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup, ApplicationContext

#   Copyright (C) 2023  Kristoffer Gjøsund

class FrequentlyAskedQuestions(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.base_embed = Embed(color=Color.dark_purple())

        return

    help_group = SlashCommandGroup(name = "help", description = "Bot Documentation")

    @help_group.command(name = "help", description="Available help commands")     #   type: ignore
    async def faq_main(self, ctx:ApplicationContext, arg:Optional[str]):
        print("[FAQ] - Help command invoked")
        if not arg: arg = str(arg)
        
        cmd = ctx.command.name if ctx.command else "help" #   type: ignore
    
        self.base_embed.title = "List of available commands"
        self.base_embed.description = f"""
            Use the command `{cmd} <module>` to get help on a specific module.\n 
            Other wise '{cmd}' will return a list of all available modules."""

        
        self.base_embed.add_field(name = "Forum Moderation Module", value = " List of available forum moderation commands.")

        match arg.lower():
            case "forum moderator module": self.embed = self.forum_moderation_module(ctx)
            case "moderator module": self.embed = self.forum_moderation_module(ctx)
            case "administrator module": self.embed = self.administration_module(ctx)
            case _:

                match (ctx.author.guild_permissions): #   type: ignore
                    case d.Permissions(ban_members=True):   self.base_embed.add_field(name=f'Forum Moderator Module', value="List of available forum moderation commands.")
                    case d.Permissions(kick_members=True):  self.base_embed.add_field(name=f'Moderator Module', value="List of available moderation commands.", inline=True)
                    case d.Permissions(administrator=True):   self.base_embed.add_field(name=f'Administrator Module', value="List of administration commands available to administrators.")

        ctx.send(embed = self.base_embed) #   type: ignore

    def forum_moderation_module(self, ctx:d.ApplicationContext):

        self.base_embed.title = 'Moderator Module'
        self.base_embed.color = Color.dark_purple()

        #self.base_embed.add_field(name=f'/channel Hide', value='- Hides the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Lock', value='- Locks the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Unlock', value='- Unlocks the given channel ', inline=True)
        #self.base_embed.add_field(name=f'/channel Rename', value='- Renames the given channel ', inline=True)
        self.base_embed.add_field(name=f'/channel Delete', value='- Deletes a channel from the server ', inline=True)
        #self.base_embed.add_field(name=f'/channel SetTopic', value='- Sets the topic of the given channel ', inline=True)
        self.base_embed.add_field(name=f'/channel Create', value='- Create a new channel default : hidden ', inline=True)
        self.base_embed.add_field(name=f'/channel Clear', value= '- Clears the given channel Chat:bangbang:', inline=True)
        
        self.base_embed.add_field(name=f'/channel SetSlowmode', value='- Sets the slowmode of the given channel ', inline=True)

        if ctx.author.guild_permissions.moderate_members: pass  #   type: ignore
        return self.base_embed
    
    def moderation_module(self, ctx:d.ApplicationContext):

        self.base_embed.title = 'Moderator Module'
        self.base_embed.color = Color.dark_purple()

        match (ctx.author.guild_permissions): #   type: ignore
            case d.Permissions(ban_members=True):   self.base_embed.add_field(name=f'/ban', value='- Bans a user from the server', inline=True)
            case d.Permissions(kick_members=True):  self.base_embed.add_field(name=f'/kick', value='- Kicks a user from the server', inline=True)
            case d.Permissions(manage_messages=True):self.base_embed.add_field(name=f'/clear', value='- Clears messages in a channel', inline=True)

    async def administration_module(self, ctx:d.ApplicationContext): 
        #   Initializing analysis commands
        #   Initializing auditlog commands
        return