
#   Discord Repositories
import discord as d
from discord.embeds import Embed
from discord import Color
from discord.ext.commands import Cog, slash_command, has_permissions, after_invoke, before_invoke

class FrequentlyAskedQuestions(Cog):

    """        
        Copyright (C) 2023  Kristoffer Gjøsund

        Help page for the bot

        >   Creation Date   : 19.02-23
        >   Last update     : 21.02-23

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

    """

    def __init__(self, bot):
        self.bot = bot
        self.embed = Embed(color=Color.dark_purple())

        return

    help = d.SlashCommandGroup(name = "help", description = "Bot Documentation")

    @help.command()
    async def faq(self, ctx:d.ApplicationContext, arg = None):

        match str(arg).lower():
            case "community module": embed = self.community(ctx)
            case "administrator module": embed = self.AdministratorModule(ctx)

        if arg == None:

            self.title = "Frequently Asked Questions"
            self.embed.add_field(name = "Community Module", value = " ")
            if ctx.author.guild_permissions.kick_members: self.embed.add_field(name = "Moderator Module", value = " ")
            if ctx.author.guild_permissions.manage_roles: self.embed.add_field(name = "Moderator Module", value = " ")
            if ctx.author.guild_permissions.manage_channels: self.embed.add_field(name = "Moderator Module", value = " ")
            if ctx.author.guild_permissions.moderate_members: self.embed.add_field(name = "Moderator Module", value = " ")
            if ctx.author.guild_permissions.administrator: self.embed.add_field(name = "Administrator Module", value = " ")

        ctx.send(embed = self.embed)

    def ServerMod(self, ctx:d.ApplicationContext):#   Server Moderation

        self.embed.title = 'Moderator Module'
        self.embed.color = Color.dark_purple()

        if ctx.author.guild_permissions.kick_members: pass
        if ctx.author.guild_permissions.manage_roles:pass

        if ctx.author.guild_permissions.manage_channels:

            self.embed.add_field(name=f'/channel Delete', value='- Deletes a channel from the server ', inline=True)
            self.embed.add_field(name=f'/channel Clear', value= '- Clears the given channel Chat:bangbang:', inline=True)
            self.embed.add_field(name=f'/channel Create', value='- Create a new channel default : hidden ', inline=True)

        if ctx.author.guild_permissions.moderate_members: pass
        return self.embed

    #   Server Adminsistration
    async def AdministratorModule(self, ctx:d.ApplicationContext): return