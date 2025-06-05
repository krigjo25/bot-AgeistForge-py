
#   Discord responsory
from discord.ui import InputText, Modal
from discord import utils, InputTextStyle, Interaction,  ChannelType

from typing import Optional

from lib.utils.embed import EmbedFactory as EF
from lib.utils.exception_handler import NotFoundError,DuplicationError

class ModalBase(Modal):
    """
        Base class for modals to inherit from.
        Contains common functionality for all modals.
    """
    def __init__(self, *args, **kwargs, ):              #   type: ignore
        super().__init__(*args, **kwargs)               #   type: ignore
        self.base_embed = EF()                          #   type: ignore
        self.custom_id = kwargs.get('custom_id', None)  #   type: ignore

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

        match self.title.lower():                                                           #   type: ignore
            case "bug-report":  await self.bug_report(interaction, data)               #   type: ignore
            case "member-report":  await self.forum_modal(interaction, data)                #   type: ignore
            case "member-support":  await self.forum_modal(interaction, data)               #   type: ignore
            case "announcement":    await self.post_announcement_modal(interaction, data)   #   type: ignore

        await interaction.response.send_message("Modal command executed", ephemeral=True)   #   type: ignore

    async def forum_modal(self, interaction:Interaction, data:dict[str, str]) -> None:
        """
        Placeholder for forum modal handling.
        """
        #   TODO : Implement dynamic role mention based on the SELECTION
        pre_defined = f"{interaction.user.display_name} has requested support by @RoleMention." #   type: ignore
        
        #   TODO : Implement dynamic channel selection based on the SELECTION
        ch = utils.get(interaction.guild.channels, name= "support", type = ChannelType.forum)   #   type: ignore
        threads = utils.get(ch.threads, name = data.get("title")) if ch else None               #   type: ignore

        try:
            if not ch: raise NotFoundError(f"Couldn't find the {interaction.guild} forum channel.")
            if threads: raise DuplicationError(f"A thread with the title '{data.get('title')}' already exists in {ch.name}.\n ( {threads.jump_url} )")
        
        except (NotFoundError, DuplicationError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)

        except Exception as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)
        
        else:
            await ch.create_thread( name = data.get("title"),                                           #   type: ignore
                                   content = data.get("Message") +"\n\n" + pre_defined,                 #   type: ignore
                                auto_archive_duration = 60*24,
                               applied_tags= [utils.get(ch.available_tags, name =self.custom_id)])      #   type: ignore

    async def post_announcement_modal(self, interaction:Interaction, data:dict[str, str]) -> None:
        ch = utils.get(interaction.guild.channels, type = ChannelType.news )                #   type: ignore

        try:
            if not ch: raise NotFoundError(f"Couldn't find the {interaction.guild} news channel.")

        except (NotFoundError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)    
        
        else:
            response =  self.base_embed.info(data, team = interaction.user.top_role)         #   type: ignore
            await ch.send(embed=response)                                                    #   type: ignore
    
    async def bug_report(self, interaction:Interaction, data:dict[str, str]) -> None:
        """
        Placeholder for bug report handling.
        """
        #   TODO : Implement bug report handling
        pass