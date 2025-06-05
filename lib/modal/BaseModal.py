
#   Python responsories


#   Discord responsory
from discord import utils, InputTextStyle, Interaction,  ChannelType, ApplicationContext
from discord.ui import InputText, Modal

from typing import Optional

from lib.utils.embed import EmbedFactory as EF
from lib.utils.exception_handler import NotFoundError

class ModalBase(Modal):
    """
        Base class for modals to inherit from.
        Contains common functionality for all modals.
    """
    def __init__(self, *args, **kwargs):                                                    #   type: ignore
        super().__init__(*args, **kwargs)                                                   #   type: ignore
        self.base_embed = EF()                                                              #   type: ignore

    
    
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

        match self.title.lower():                                                          #   type: ignore
            case "announcement":    await self.announcement_modal(interaction, data)       #   type: ignore
            case "member-support":  await self.forum_modal(interaction, data)     #   type: ignore

        await interaction.response.send_message("Modal command executed", ephemeral=True)   #   type: ignore

    async def forum_modal(self, interaction:Interaction, data:dict[str, str]) -> None:
        """
        Placeholder for forum modal handling.
        """

        ch = utils.get(interaction.guild.channels, type = ChannelType.forum )                #   type: ignore
        try:
            if not ch: raise NotFoundError(f"Couldn't find the {interaction.guild} forum channel.")
        
        except (NotFoundError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)
        
        else:
            print(data, ch)
            # Build the forum post
            
            await ch.create_thread( name = data.get("title"),                                             #   type: ignore
                                content = data.get("Message"),                                      #   type: ignore
                                auto_archive_duration = 60*24,)
                                #applied_tags= [utils.get(ch.available_tags, name = "discord")])  #   type: ignore
            #   
            pass

    async def announcement_modal(self, interaction:Interaction, data:dict[str, str]) -> None:
        ch = utils.get(interaction.guild.channels, type = ChannelType.news )                #   type: ignore

        try:
            if not ch: raise NotFoundError(f"Couldn't find the {interaction.guild} news channel.")

        except (NotFoundError) as e:
            e = self.base_embed.error(e)
            await interaction.response.send_message(embed=e, ephemeral=True)    
        
        else:
            response =  self.base_embed.info(data, team = interaction.user.top_role)         #   type: ignore
            await ch.send(embed=response)                                                    #   type: ignore
            