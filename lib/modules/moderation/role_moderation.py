#   Python Repositories
import datetime

#   Discord Repositories
import discord as d
from discord import utils, Colour
from discord.embeds import Embed
from discord.ext import  commands

class RoleModeration(commands.Cog):

    """
        Commands for Moderators with manage_role
    """

    def __init__(self, bot):

        self.bot = bot
        self.embed = Embed()
        self.now = datetime.datetime.now()

        return

    #   Slash command group
    role = d.SlashCommandGroup(name = "role", description = "Role mananger", default_member_permissions = d.Permissions(manage_roles = True))

    @role.before_invoke # type: ignore
    async def check_channel(self, ctx: d.ApplicationContext):

        channel = []
        ch = ["auditlog", "report", "support"]

        try :
            for i in ch:
                if utils.get(ctx.guild.text_channels, name = i): return 


        except TypeError as e: print(e)
        else:

            #   Creating a channel
            perms = {ctx.guild.default_role:d.PermissionOverwrite(view_channel=False)}

            for i in ch:

                #   Prepare and send embeded message
                self.embed.color = Colour.dark_red()
                self.embed.title = f'Auto Generated Channel'



                match i:

                    case "auditlog": 
                        self.embed.description = "Created to have easy accsess to bot commands used by admin / moderator"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                    case "report": 
                        self.embed.description = "Member report channel"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                    case "support": 
                        self.embed.description = "Member support channel"
                        i = await ctx.guild.create_text_channel(i, overwrites=perms)

                self.embed.timestamp = datetime.datetime.now()
                await i.send(embed=self.embed)

    @role.command(name= "create", description = "Create a new Role") # type: ignore
    async def create(ctx:d.ApplicationContext): pass

    @role.command(name = "delete", describe = "Delete a role")  # type: ignore
    async def delete(self, ctx:d.ApplicationContext, role:d.Option(str, "Server role", required = True) ):

        """
            Delete a server role
            #
            #   Checking if there is any channels called 'moderationlog'
            #   Ask the user for comfirmation before removing the role

        """

        await self.check_channel(ctx)# Calling the function manually
        #   Fetch role and channel
        role = utils.get(ctx.guild.roles, name= role)#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try:
            if not role : raise Exception(f"Could not find \"**{role}**\" in the server")
            elif not ch : raise Exception("The channel \"**auditlog**\" were not created")

        except Exception as e:

            self.embed.title = "An Exception Occured"
            self.embed.description = f'{e}, Try again...'
            await ctx.send(embed = self.embed)

            del role, ch#   Clear some memory
            return

        else:   #   Confirming the deletion
            modal = Role(title = "Role Deletion")
            ctx.send_modal(modal)

        del role, ch, modal

        return
 
    @role.command(name = "remove", description = "Remove a member from a role") # type: ignore
    async def remove(self, ctx:d.ApplicationContext, member:d.Member, role:d.Option(str, "Server role", required = True), *, reason:d.Option(str, "Reason to remove the member from the role", required = True)):

        """
            Removing the member from the selected role

            #   Fetch the role & audit channel
            #   Checking if there is any channels called 'auditlog'
            #   When the command is invoked, ask the user for a confirmation
            #   Confirmation to remove the user from the role

        """

        await self.check_channel(ctx)# Calling the function manually
        role = utils.get(ctx.guild.roles, name=f'{role}')#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try: 
            if not role : raise Exception(f"Role \"{role}\" Not found")
            if not ch: raise Exception(f"The auditlog channel were not created")

        except Exception as e: 

            self.embed.color = Colour.dark_red()
            self.embed.title = 'An Exception Occured'
            self.embed.description = f"{e}, try again."
            await ctx.send(embed = self.embed)
            return

        else:

            #  Prepare, remove & send
            modal = Role(title = "Remove member")
            ctx.send_modal(modal)

        return

    @role.command( name = "set", description = "Set a member's new role")   # type: ignore
    async def add(self, ctx:d.ApplicationContext, member:d.Member, role:d.Option(str, "Server role", required = True)):

        """
            Add a member to given role

            #   Fetch role and channel and check if they actually exists
            #   Except exception if not exists
            #   add member to role
        """
        await self.check_channel(ctx)# Calling the function manually
        role = utils.get(ctx.guild.roles, name=f'{role}')#  Fetch role
        ch = utils.get(ctx.guild.channels, name='auditlog')#    Fetch channel

        try :
            if not role: raise Exception("Role does not exist")
            elif not ch: raise Exception("The channeld \"**auditlog**\" were not created")

        except Exception as e:

            self.embed.title = "An Exception Occured"
            self.embed.description = f"{e}, try again"
            await ctx.send(embed = self.embed)

            del role, ch, member
            return
        else:

            #  Prepare, remove, send & Clean up
            self.embed.color = Colour.dark_red()
            self.embed.title = f'{member} has been added to {role} by {ctx.author}'

            await member.add_roles(role)
            await ch.send(embed = self.embed)

        return

    @role.command(name = "modify", description = "Modify role permissions") # type: ignore
    async def modify(self, ctx:d.ApplicationContext, role:d.Option(str, "Server role", required = True), *, reason = None):  return

    @role.after_invoke  # type: ignore
    async def clear_memory(self, ctx: d.ApplicationContext):

        #   Clear some Memory
        self.embed.clear_fields()
        self.embed.remove_image()
        self.embed.remove_author()
        self.embed.remove_footer()
        self.embed.remove_thumbnail()
        self.embed.color = Colour.dark_purple()
        self.embed.description = ""

        return
