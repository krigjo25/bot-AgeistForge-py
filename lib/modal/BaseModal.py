#   The modal system works

import os
from typing import Optional, Any, List

from discord.ui import InputText, Modal
from discord import utils, InputTextStyle, Interaction,  ChannelType

from lib.utils.embed import EmbedFactory
from lib.utils.moderation import ModerationUtils

from lib.apis.github_api import GithubAPI
from lib.utils.exceptions import ResourceNotFoundError, DuplicationError, ExceptionHandler

from lib.utils.logger_config import ModalWatcher
logger = ModalWatcher(name="Modal")
logger.file_handler()

class ModalBase(Modal):
    """
        Base class for modals to inherit from.
        Contains common functionality for all modals.
    """

    def __init__(self, *args, **kwargs, ):              #   type: ignore
        super().__init__(*args, **kwargs)               #   type: ignore
        self.base_embed = EmbedFactory

    def create_input(self, label: str, required: bool, style:InputTextStyle = InputTextStyle.short, placeholder: Optional[str] = None):
        """
        Helper method to create an InputText item.
        """
        
        if not placeholder:
        
            match (label.lower()):
                case "url":
                    placeholder = "E.G https://example.com | Provides A read more link for the title"
                
                case _:
                    placeholder = f"Please provide a detailed {label}"


        return self.add_item(InputText(label=label, placeholder=placeholder, style=style, required=required))

    async def callback(self, interaction:Interaction):

        data = {}
        for  i in self.children:
            data[i.label] = i.value.lower() if isinstance(i.value, str) else i.value

        await self.handle_modal(interaction, data)                   #   type: ignore

        await interaction.response.send_message("Modal command executed", ephemeral=True)   #   type: ignore

    async def handle_modal(self, interaction:Interaction, data:dict[str, Any]) -> None:
        match self.title.lower():
            case "bug-report":  await self.report_issue(interaction, data)                    
            case "member-report":  await self.forum_modal(interaction, data)
            case "server-support":  await self.forum_modal(interaction, data)
            case "discord-support":  await self.forum_modal(interaction, data)
            case "announcement":    await self.post_announcement_modal(interaction, data)
            case "custom-channel": await self.channel_modal(interaction, data)
            case _ : 
                logger.error(f"Modal title : '{self.title}' not recognized.\n")
                raise ValueError(f"Modal title : '{self.title}' not recognized.\n")

    async def forum_modal(self, interaction:Interaction, data:dict[Any, Any]) -> None:
        """
        Placeholder for forum modal handling.
        """
        variable = self.title.lower().split('-') if isinstance(list, self.title) else None

        ch = utils.get(interaction.guild.channels, name= variable[1], type = ChannelType.forum) #   type: ignore
        threads = utils.get(ch.threads, name = data.get("title")) if ch else None               #   type: ignore

        try:
            if not ch: raise ResourceNotFoundError(f"Couldn't find the {interaction.guild} forum channel.")
            if threads: raise DuplicationError(f"A thread with the title '{data.get('title')}' already exists in {ch.name}.\n ( {threads.jump_url} )")
        
        except (ResourceNotFoundError, DuplicationError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)

        except Exception as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)
        
        else:
            responsebility = f"{interaction.user.name} has requested assistance from @RoleMention."                                     #   type: ignore
            form = f""" **Name** :\n{interaction.user.name}\n **What is the issue? :**\n{data.get("Message")}\n\n{responsebility}"""    #   type: ignore

            await ch.create_thread( name = data.get("title"),                                       #   type: ignore
                                    content = form,                                                 #   type: ignore
                                    auto_archive_duration = 60*24,
                                    applied_tags= [utils.get(ch.available_tags, name =variable[0])])    #   type: ignore

    async def post_announcement_modal(self, interaction:Interaction, data:dict[str, str]) -> None:
        ch = utils.get(interaction.guild.channels, type = ChannelType.news )                #   type: ignore

        try:
            if not ch: raise ResourceNotFoundError(f"Couldn't find the {interaction.guild} news channel.")

        except (ResourceNotFoundError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)    
        
        else:
            response =  self.base_embed.info(data, team = interaction.user.top_role)         #   type: ignore
            await ch.send(embed=response)                                                    #   type: ignore
    
    async def report_issue(self, interaction:Interaction, data:dict[str, Any]) -> None:
        """
        Placeholder for bug report handling.
        """
        
        api = GithubAPI(KEY=os.getenv('GithubIssueToken'))  #   type: ignore
        repo_found = False
        
        issue = {
            "title": data.get('title'),
            "assignees": data.get('assignees', ["krigjo25"]),
            "labels": data.get('labels', ['unconfirmed-bug']),
            "body": data.get('message', 'No description provided.'),}

        issue = {k: v for k, v in issue.items() if v is not None}  #   Filter out None values

        try:
            response = api._make_request_(f"{api.API_URL}/user/repos", head=api.head)  #   type: ignore

            for i in response:
                if str(data['app']).lower() in str(i['name']).lower():

                    data['app'] = i['name']
                    data['owner'] = i['owner']['login']

                    repo_found = True

                    break

            if not repo_found:
                raise ResourceNotFoundError(f"Couldn't find the repository for {data.get('app')}. Please check the app name and try again.")

            await api.post_issue(issue, f"repos/{data.get('owner')}/{data.get('app')}/issues")  #   type: ignore
        
        except (ResourceNotFoundError, Exception) as e:
            print(f"Error: {e}")

    async def channel_modal(self, interaction:Interaction, data:dict[str, Any]) -> None:
        mod_utils = ModerationUtils()

        topic = data.get('Channel Topic', "No Topic Provided")
        ch = utils.get(interaction.guild.channels, name= data['Channel Name'])                                          #   type: ignore
        perm = str(data.get('Permissions', interaction.guild.default_role.permissions)).split(',')                      #   type: ignore

        # How can i check if the cateogry is None?
        category = next((i for i in interaction.guild.categories if str(i).lower() == data.get('Category', str(interaction.channel.category.name).lower())), None)  #   type: ignore
        print(f"Category: {category}, current category: {interaction.channel.category}")                                                                                  #   type: ignore
        try:
            if category:
                if ch in category.channels and ch.type == str(data['Channel Type']).lower():                                  #   type: ignore
                    raise DuplicationError(f"A channel with the name '{data.get('Channel Name')}' and Same Channel Type '{data.get('Channel Type')}' already exists in {interaction.guild.name}.")
                
        except DuplicationError as e: await mod_utils.create_error_entry(interaction, e)
        #else: await self.create_channel_modal(interaction, data, perm, category, topic) 

    @staticmethod
    async def create_channel_modal( interaction:Interaction, data:dict[str, Any], perm : List[str], topic:str, category:str) -> None:
        mod_utils = ModerationUtils()
        try:
            print(perm)
            await mod_utils.create_channel(name = data['Channel Name'], 
                                        interaction = interaction, 
                                        channel_type = str(data['Channel Type']).lower(), 
                                        category = interaction.channel.category,  #   type: ignore
                                        topic = topic,
                                        nsfw= False,
                                        perms = interaction.channel.category) #   #   type: ignore
        except ExceptionHandler as e:
            print(e)
            await mod_utils.create_error_entry(interaction, e)
            
        #   TODO: Checking if the channel already exists
        #   TODO: Add a check for the channel type
        #   TODO: Add a check for the category name if provided
        #   TODO: Add a check for the permissions if provided
        #   TODO: Add a check for the Channel topic if provided
        #   TODO: Catch any exceptions that may occur

        #   TODO: If everything goes well, create the channel and send a message to the user

        
        #   TODO: Create a channel with the provided data