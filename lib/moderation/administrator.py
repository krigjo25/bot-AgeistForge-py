#       Administrator
#        Copyright (C) 2023  Kristoffer Gjøsund

#        *   Creation Date   : 21.02-23
#        *   Last update     :
#        *   Version         : 0.1.0 Beta

#   Python Repositories
import datetime
from typing import Annotated
from discord.ext import  commands
from discord.embeds import Embed, Colour
from discord import utils, Option, ApplicationContext, SlashCommandGroup, Permissions, Member

from lib.utils.logger_config import AdminWatcher
from lib.utils.exception_handler import NotFoundError

logger = AdminWatcher(name="administrator-module", dir=".logs")
logger.file_handler()

class Administrator(commands.Cog):
    def __init__(self, bot:commands.Bot):

        self.bot = bot
        self.embed = Embed(color=Colour.dark_red())
        self.now = datetime.datetime.now().strftime('%a, %d.%b-%y')

    admin_group = SlashCommandGroup(name = "ban", description = "Server Administrator", default_member_permissions = Permissions(administrator = True))

    @admin_group.before_invoke #   type: ignore
    async def CheckModChannel(self, ctx:ApplicationContext):
        pass

    @admin_group.after_invoke #   type: ignore
    async def admin_command_after(self, ctx:ApplicationContext):

        
        #   Clearing embeds
        self.embed.clear_fields()
        self.embed.remove_image()
        self.embed.remove_author()
        self.embed.remove_footer()
        self.embed.description = ""
        self.embed.remove_thumbnail()
        self.embed.color = Colour.dark_purple()

    @admin_group.command()  #   type: ignore
    async def list(self, ctx:ApplicationContext):

        #   Initializing a list
        banned = []

        try:

            #   Iterating over the ctx.guild bans
           async for entry in ctx.guild.bans():

                dictionary = {  "name": entry.user.name,
                                "discriminator": entry.user.discriminator,
                                "reason": entry.reason}

                banned.append(dictionary)

        except Exception as e : 
            logger.exception(f"An error occured while fetching the list of banned members: {e}")
            print(e)
        else:

            #   Prepare the ebeded message
            self.embed.title = 'List of banned server members'
            self.embed.description =' User name & discriminator | Reason'
            self.embed.color = Colour.dark_red()

            if banned:

                for i in banned: 
                    self.embed.add_field(name= f'{i["name"]}#{i["discriminator"]}', value = f'{i["reason"]}', inline = True)


            else: self.embed.description = "Noone banned yet, Hurray :party:"

            self.embed.add_field(name= f'Total banned users {len(banned)}\n== End of List ==', value = ':-)', inline = False)
            await ctx.send(embed=self.embed)

    @admin_group.command()  #   type: ignore
    async def member(self, ctx:ApplicationContext, member:Member, *, reason:Annotated[str, Option(str, "Reason for the ban", required=True)]):

        """
            #   Ban a server member
            #   Reason required
            #   Notify the user about the ban
            #   Cheeck for a moderationlog channel
            #   Log the ban

        """

        ch = utils.get(ctx.guild.channels, name='auditlog') #   Fetch channel
        try :
            if not ch : raise NotFoundError(404,f"'**auditlog**' was not found.")
            

        except NotFoundError as e :

            self.embed.color = Colour.dark_red()
            self.embed.title =f"An Exception Occured"
            self.embed.description = f"{e.status_code} - {e.message}\n"
            await ctx.send(embed = self.embed)

        else:

            #   Log the ban
            self.embed.color = Colour.dark_red()
            self.embed.description = f"due to {reason}"
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f'{member} has been banned by {ctx.author}'
            
            await ch.send(embed=self.embed)

            #   Notify the user about the ban & ban the member
            message = f'the Administrator Team has decided to probhid you for using  **{ctx.guild.name}** \n \n Due to :\n **{reason}**'
            await member.send(message)
            await member.ban(reason=reason)

            #   Clear some memory
            del reason, message
            del member, ch

        return

    @admin_group.command()  #   type: ignore
    async def unban(self, ctx:ApplicationContext, *, member:Member):

        ch = utils.get(ctx.guild.channels, name='auditlog') #   Fetch channel

        try :
            if not ch : raise Exception("auditlog channel does not exits")

        except Exception as e:

            #   Prepare emed message
            self.embed.color = Colour.dark_red()
            self.embed.title = f"An Exception Occured"
            self.description = f"{e}, try again"
            await ctx.send(embed = self.embed)

            del ch, member
            return

        else:
            
            #   Log the unban
            self.embed.color = Colour.dark_red()
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f"{member.name} has been unbanned by {ctx.author.name}"

            await ch.send(embed=self.embed)

            #  Unban the given member
            async for entry in ctx.guild.bans():
                if entry.user.name == member.name: await ctx.guild.unban(entry.user)

            await member.send(f"Greetings, {member}, the administrator team has decided to unban you from {ctx.guild}\n You are now welcome back to the server.")

        del member, ch

        return

    @admin_group.command()  #   type: ignore
    @commands.is_owner()    #   type: ignore 
    async def shutdown_bot(self, ctx:ApplicationContext): 

        await ctx.defer(ephemeral=True)  #   type: ignore

        await ctx.send("Initiating bot restart...", ephemeral=True) #   type: ignore
        logger.critical(f"'{ctx.author}' initiated self destruct butten !")

        # This will gracefully disconnect the bot from Discord.
        # Once disconnected, the Python script will exit.
        await self.bot.close()


    @admin_group.command()  #   type: ignore
    async def server_analysis(self, ctx:ApplicationContext): 
        pass

