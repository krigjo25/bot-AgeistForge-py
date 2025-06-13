
#   Python Repositories

from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
load_dotenv()

#   Discord Repositories

from discord import utils, Member, Interaction, PermissionOverwrite, ApplicationContext, Role, SlashCommand

from lib.utils.embed import EmbedFactory
from lib.utils.logger_config import UtilsWatcher
from lib.utils.exceptions import ResourceNotFoundError, ExceptionHandler, SelfReferenceError, AuthorizationError, TypeErrorHandler

logger = UtilsWatcher(name="Moderation Utils")  #   type: ignore
logger.file_handler()

class ModerationUtils(object):

    """
        Utility class for moderation actions.
        This class provides methods for creating log entries, checking member validity, and sending messages to members about moderation actions.
        It also includes methods for creating channels and categories in the server.
        
        Attributes:
            - base_embed: An instance of the EmbedFactory class for creating embeds.
    """
    
    def __init__(self):
        self.base_embed = EmbedFactory

    @staticmethod
    def fetch_member_exception(interaction:Interaction, member:Member) -> None:
        """
            This method checks if the member is valid for moderation actions.
            It raises exceptions if the member is not found, if the member is the same as the user, or if the member has a higher role than the user.
            Parameters:
                - interaction: The interaction object from the command.
                - member: The member to be moderated.

            Raises:
                - ResourceNotFoundError: If the member is not found.
                - SelfReferenceError: If the member is the same as the user.
                - AuthorizationError: If the member has a higher role than the user.

            Returns:
                None
        """
        
        if not member: 
            raise ResourceNotFoundError(f"Member not found")

        if member == interaction.user: 
            raise SelfReferenceError(" You cannot moderate yourself")

        if member.top_role >= interaction.user.top_role : 
            raise AuthorizationError("You cannot moderate this member, because they have a higher role than you")                                                         # type: ignore
    
    async def create_log_entry(self, interaction:Interaction | ApplicationContext, reason:Optional[str] = None, member:Optional[Member] = None, function_name:Optional[str] = None, n: Optional[int] = 0):
        """
            Create a log entry in the auditlog channel
            This method is used to log actions taken by moderators on members.
            It sends a message to the auditlog channel with the details of the action taken.
            During the exception handling, it creates the auditlog channel.

            Parameters:
                - interaction: The interaction object from the command.
                - member: The member who was moderated (optional).
                - action: The action taken on the member (e.g., "ban", "sush", "lift").
                - reason: The reason for the action taken.

            Exceptions:
                - ResourceNotFoundError: If the auditlog channel does not exist.
                - Creates a new auditlog channel if it does not exist.
            Returns:
                None

            """
        author = None
        channel = utils.get(interaction.guild.channels, name='auditlog')                                                        #   type: ignore


        if isinstance(interaction, ApplicationContext):
            author = interaction.author
            ch = utils.get(interaction.guild.channels, id=interaction.channel_id)
        
        else:
            author = interaction.user.name
            ch = interaction.channel

        try:
            if not channel: raise ResourceNotFoundError("Channel \"**auditlog**\" does not exists")

        except ResourceNotFoundError:
            permissions: Dict[str, PermissionOverwrite] = {}
            permissions['Forum-moderators'] = PermissionOverwrite(view_channel=True)
            permissions['Admins'] = PermissionOverwrite(view_channel=True, send_messages=False)
            permissions['Moderators'] = PermissionOverwrite(view_channel=True, send_messages=False)
            permissions[interaction.guild.default_role] = PermissionOverwrite(view_channel=False, send_messages=True)           #   type: ignore
            self.create_channel(name = "auditlog", interaction=interaction, channel_type = Channel.Text, perms = permissions)   #   type: ignore
        
        finally:
            dictionary:Dict[str, Any] = {}

            if member:
                dictionary["title"] = f"**{member.name}** has been {function_name} by {author}"
                dictionary["message"] = f"*{reason}*.\n\n User has been notified by a direct message."    
            
            if ch:
                match(function_name):
                    case _: 
                        function_name = f"{function_name}d"

                dictionary['title'] = f"**{author}** has {function_name} {f"{n} line(s) in" if n else ""}, {ch.mention if ch.name != "Unkown" else ch.name} channel."
            embed = self.base_embed.warning(dictionary)

            await channel.send(embed=embed)     #   type: ignore

    @staticmethod
    async def create_error_entry(ctx:ApplicationContext | Interaction, e:ExceptionHandler) -> None:
        """
            This method is used to log errors that occur during command execution.

            
            Parameters:
                - ctx: The context of the command or interaction.
                - e: The exception that occurred.
            
            Returns:
                a Contextual error message to the user.
        """
        logger.error(f"An {e.__class__.__name__} Occured: {e.message}")
        await ctx.respond(f"An {e.__class__.__name__} Occured: {e.message}\nPlease report if you think this is a mistake '**/community bug-report**'\n**Errors are Saved in the bot, but not supervised.**", ephemeral=True)  #   type: ignore

    @staticmethod
    async def send_member_message(ctx:ApplicationContext, member:Member, action:str, reason:Optional[str] = None, time:Optional[int] = None):
        """
            This method sends a direct message to the member about the action taken against them.
            Parameters:
                - ctx: The context of the command or interaction.
                - member: The member who was moderated.
                - action: The action taken on the member (e.g., "ban", "sush", "lift").
                - reason: The reason for the action taken (optional).
                - time: The duration of the action (optional, in seconds).
            
            Returns:
                None

            Raises:
                - Exception: If the member cannot be sent a direct message.
            This method constructs a message based on the action taken and sends it to the member.
        """

        member_message= ""
        server = f"**{ctx.guild.name if ctx.guild else "the server"}**"

        match(action):  #   type: ignore

            case "ban":
                member_message = f"You have been banned from {server} as a consequence of :\n*{reason}*.\n\n"

            case "sush":
                member_message = f"You will not be able to use {server}'s channels for {time}s as a consequence of :\n*{reason}*.\n\n"

            case "lift":
                member_message = "Your sush has been lifted.\n\n"

            case _:
                member_message = f"You have been {action}ed by an moderator, as a consequence of :\n*{reason}*.\n\n"

        if ctx.guild.rules_channel : 
            member_message += f"Please read the guidelines in **{ctx.guild.rules_channel.mention}** for more information.\n"
    
        await member.send(f"Greetings, **{member.name}**.\nYou recieve this notification, because you're a member of {server}.\n\n{member_message}Thank you for your patient and understanding\n Sincerely Moderation team")  #   type: ignore

    async def create_channel(self, name:str, interaction:Interaction, channel_type:str, topic:str, perm:Dict[Role | Member, PermissionOverwrite], nsfw:bool = False, category:Optional[str] = None) -> None:
        
        """
            Create a channel in the server.
            This method uses the pycord API to create the channel and handles any exceptions that may occur during the process.
            It supports various channel types such as Text, Voice, Forum, and Stage.
            Parameters:
                - name: The name of the channel to be created.
                - interaction: The interaction object from the command.
                - channel_type: The type of channel to be created (e.g., "Text", "Voice", "Forum", "Stage").
                - category: The category under which the channel will be created (optional).
                - topic: The topic of the channel (optional).
                - perms: A dictionary of permission overwrites for the channel (optional).
            Raises:
                - TypeError: If the channel type is not recognized or implemented yet.
            Returns:
                None
        """
        try:
            match (channel_type.lower()):
                
                case "text":
                    print(category)
                    await interaction.guild.create_text_channel(
                        nsfw = nsfw,
                        name = name,
                        topic = topic,
                        overwrites = perm,
                        reason = f"Channel '{name}' created by {interaction.user.name}",                            #   type: ignore
                        category = category,    #   type: ignore
                    )

                case "voice":
                    await interaction.guild.create_voice_channel(
                        name = name,
                        overwrites = perm,
                        reason = f"Channel '{name}' created by {interaction.user.name}",                            #   type: ignore
                        category = utils.get(interaction.guild.categories, name=category)
                    )
                
                case "forum":
                    await interaction.guild.create_forum_channel(
                        nsfw = nsfw,
                        name = name,
                        topic = topic,
                        overwrites = perm,
                        reason = f"Channel '{name}' created by {interaction.user.name}",                            #   type: ignore
                        category = utils.get(interaction.guild.categories, name=category),    #   type: ignore
                    )
                
                case "stage":
                    await interaction.guild.create_stage_channel(
                        topic = topic,
                        overwrites = perm,
                        reason = f"Channel '{name}' created by {interaction.user.name}",                            #   type: ignore
                        category = utils.get(interaction.guild.categories, name=category))    #   type: ignore

                case _:
                    raise TypeErrorHandler(f"Channel type '{channel_type}' is not recognized or implemnted yet. Please use one of the following: Text, Voice, Forum, Stage, News.")

        except TypeErrorHandler as e:
            raise e
        else:
            await self.create_log_entry(interaction, function_name=f"create {channel_type.lower()} channel", reason=f"Channel '{name}' created by {interaction.user.name}", member=interaction.user)  # type: ignore
        
    @staticmethod
    async def create_category(ctx:ApplicationContext, category:str, reason:str) -> None:
        """
            #   Create a category for the auditlog channel
        """
        try:
            if utils.get(ctx.guild.categories, name = category):
                raise ExceptionHandler("Category already exists")
            
            if not category: raise ExceptionHandler("Category name can not be empty")
            elif len(category) > 100: raise ExceptionHandler("Category name can not be longer than 100 characters")

        except ExceptionHandler as e:
            embed = EmbedFactory.exception(e)

            ctx.respond(embed = embed)

        else:
            await ctx.guild.create_category(name = category, reason = reason)

    async def create_thread(self, name:str, interaction:Interaction, channel:Optional[str] = None, perms:Optional[Dict[str, PermissionOverwrite]] = None) -> None:
        """
            Create a thread in the server.
            This method uses the pycord API to create the thread and handles any exceptions that may occur during the process.
            Parameters:
                - name: The name of the thread to be created.
                - interaction: The interaction object from the command.
                - channel: The channel in which the thread will be created (optional).
                - perms: A dictionary of permission overwrites for the thread (optional).
            Returns:
                None
        """
        raise NotImplementedError("This method is not implemented yet, please use the Channel class to create a thread")
    async def handle_permissions(self, perm:str)-> PermissionOverwrite:
        pass

    @staticmethod
    def fetch_function_name(name:SlashCommand) -> str:
        """
            Fetch the name of the function from the given string.
            This method is used to extract the function name from a string.
            Parameters:
                - function_name: The string containing the function name.
            Returns:
                The extracted function name or None if not found.
        """
        func = getattr(name, "__name__", name)
        func = str(func).split(" ")

        return func[1]