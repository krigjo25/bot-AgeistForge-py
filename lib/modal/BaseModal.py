
import os

from discord.ui import InputText, Modal
from discord import utils, InputTextStyle, Interaction,  ChannelType

from typing import Optional, Any

from lib.apis.github_api import GithubAPI
from lib.utils.embed import EmbedFactory as EF
from lib.utils.exceptions import ResourceNotFoundError,DuplicationError


class ModalBase(Modal):
    """
        Base class for modals to inherit from.
        Contains common functionality for all modals.
    """
    def __init__(self, *args, **kwargs, ):              #   type: ignore
        super().__init__(*args, **kwargs)               #   type: ignore
        self.base_embed = EF()                          #   type: ignore

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
        print(f"Model title: {self.title}, data: {data}")  #   type: ignore
        match self.title.lower():                                                           #   type: ignore
            case "bug-report":  await self.report_issue(interaction, data)                    #   type: ignore
            case "member-report":  await self.forum_modal(interaction, data)                #   type: ignore
            case "server-support":  await self.forum_modal(interaction, data)               #   type: ignore
            case "discord-support":  await self.forum_modal(interaction, data)              #   type: ignore
            case "announcement":    await self.post_announcement_modal(interaction, data)   #   type: ignore

        await interaction.response.send_message("Modal command executed", ephemeral=True)   #   type: ignore

    async def forum_modal(self, interaction:Interaction, data:dict[Any, Any]) -> None:
        """
        Placeholder for forum modal handling.
        """
        #   TODO : Implement dynamic role mention based on the SELECTION
        
        variable = self.title.lower().split('-') if self.title else None

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
            responsebility = f"{interaction.user.display_name} has requested assistance from @RoleMention."                                     #   type: ignore
            form = f""" **Name** :\n{interaction.user.display_name}\n **What is the issue? :**\n{data.get("Message")}\n\n{responsebility}"""    #   type: ignore

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
        #  TODO: Fetch all repositories
        api = GithubAPI(KEY=os.getenv('GithubIssueToken'))  #   type: ignore
        repo = []
        data['owner'] = "krigjo25"
        print(data)
        try:
            response = api.get(f"{api.API_URL}/user/repos", head=api.head)  #   type: ignore
            for i in response:
                repo.append(i['name'].lower().split('-')[1] if '-' in i['name'] else i['name'])
            
            if data['app'].lower() not in repo:
                raise ResourceNotFoundError(f"Repository '{data['app']}' not found. Please ensure the repository exists and is accessible.")

            await api.post_issue(data, f"repos/{data.get('owner')}/bot-AgeistForge-py/issues")  #   type: ignore
        
        except (ResourceNotFoundError, Exception) as e:
            #   TODO: Catch reponse Exception
            #   TODO: Catch repository not found error
            
            pass
