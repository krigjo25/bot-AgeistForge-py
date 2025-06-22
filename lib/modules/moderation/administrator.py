#   Administrator Module

#   Python Repositories
import datetime
from typing import Annotated, List, Dict, Tuple

#   Discord Repositories
from discord import Embed
from discord.ext import  commands
from discord import utils, Option, ApplicationContext, SlashCommandGroup, Permissions, Member

#   Local Repositories
from lib.utils.moderation import ModerationUtils
from lib.utils.embed import EmbedFactory
from lib.utils.logger_config import AdminWatcher
from lib.utils.exceptions import ResourceNotFoundError

logger = AdminWatcher(name="administrator-module", dir=".logs")
logger.file_handler()

class Administrator(commands.Cog):
    def __init__(self, bot:commands.Bot):

        self.bot = bot
        self.now = datetime.datetime.now().strftime('%a, %d.%b-%y')
        self.base_embed = EmbedFactory

    admin_group = SlashCommandGroup(name = "ban", description = "Server Administrator",
                                    default_member_permissions = Permissions(administrator = True))

    @admin_group.command(name ="list")                                                                                   #   type: ignore
    async def list(self, ctx:ApplicationContext):

        banned:List[Dict[str,str]] = []


        try:
           async for entry in ctx.guild.bans():

                dictionary = {  "name": entry.user.name,
                              "discriminator": entry.user.discriminator,
                              "reason": entry.reason}
                banned.append(dictionary)

        except Exception as e :
            logger.error(f"An error occurred while fetching banned members: {e}")
            dictionary = {"title": "Error", "message": f"An error occurred while fetching banned members: {e}"}
            embed = EmbedFactory().warning(dictionary=dictionary)
            await ctx.respond(embed=embed, ephemeral=True)
            return


        else:
            dictionary: Dict[str, str] = {}
            dictionary["title"] = "List of banned server members :sto"

            if banned:

                dictionary["message"] = f"User name & discriminator | Reason.\tTotal banned users {len(banned)}"

                embed = EmbedFactory().warning(dictionary = dictionary, fields=tuple(banned))

            else: 
                dictionary["message"] = f"No one banned yet, :partying_face: Hurray :partying_face:\nTotal banned users {len(banned)}\n== End of List =="
                
                embed = EmbedFactory().all_clear(dictionary)

            await ctx.respond(embed=embed, ephemeral=True)
            

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
            if not ch : raise ResourceNotFoundError(404,f"'**auditlog**' was not found.")
            

        except ResourceNotFoundError as e :

            """self.embed.color = Colour.dark_red()
            self.embed.title =f"An Exception Occured"
            self.embed.description = f"{e.status_code} - {e.message}\n"
            await ctx.send(embed = self.embed)"""

        else:

            #   Log the ban
            """self.embed.color = Colour.dark_red()
            self.embed.description = f"due to {reason}"
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f'{member} has been banned by {ctx.author}'
            
            await ch.send(embed=self.embed)"""

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
           """ self.embed.color = Colour.dark_red()
            self.embed.title = f"An Exception Occured"
            self.description = f"{e}, try again"
            await ctx.send(embed = self.embed)"""


        else:
            
            #   Log the unban
            """self.embed.color = Colour.dark_red()
            self.embed.timestamp = datetime.datetime.now()
            self.embed.title = f"{member.name} has been unbanned by {ctx.author.name}"

            await ch.send(embed=self.embed)"""

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

        await self.bot.close()


    @admin_group.command()  #   type: ignore
    async def server_analysis(self, ctx:ApplicationContext): 
        pass

