
#   Python responsories
import datetime

#   Discord responsory
from discord import utils, Colour, InputTextStyle, Interaction, TextChannel, Embed
from discord.ui import InputText, Modal

from typing import Optional

from lib.utils.exception_handler import NotFoundError

class ModalBase(Modal):
    """
        Base class for modals to inherit from.
        Contains common functionality for all modals.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_embed = Embed()
        self.base_embed.colour = Colour.dark_red()
    
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

    def set_embed(self, dictionary: dict, author: Optional[str] = None, team: Optional[str] = None, avatar: Optional[str] = None):
        """
        Helper method to set embed properties.
        """

        for key, value in dictionary.items():

            match str(key).lower():
                case "title":
                    self.base_embed.title = value
                
                case "url":
                    if value: self.base_embed.url = value
                                
                case "message":
                    self.base_embed.description = value

        self.base_embed.timestamp = datetime.datetime.now()
        if author: self.base_embed.set_author(name=f"{author}", icon_url=avatar or None)
        if team: self.base_embed.set_footer(text=f"Wish you a glorious day further,\nThe {team} Team", icon_url=avatar or None)

    async def send_embed(self, channel: TextChannel):
        """
        Helper method to send the embed to a specified channel.
        """

        if channel:
            await channel.send(embed=self.base_embed)
        else:
            raise ValueError("Channel cannot be None.")
    
    async def callback(self, interaction:Interaction):

        print(f"Modal {self.title} was submitted by {interaction.user.display_name}")
        data = {}
        for  i in self.children:
            data[i.label] = i.value.lower() if isinstance(i.value, str) else i.value

        match self.title.lower():

            case "announcement":
                ch = utils.get(interaction.guild.channels, name = self.children[0].value)   #   Fetch the channel

                try:
                    if not ch: raise NotFoundError("Channel does not exits")

                except (NotFoundError) as e:
                    data = {
                        "message": e.message,
                        "title": f"Exception {e.__class__.__name__} arised",
                    }
                    self.set_embed(data)

                    await interaction.response.send_message(embed=self.base_embed)
                except (Exception) as e:
                    data = {
                        "message": e,
                        "title": f"Exception {e.__class__.__name__} arised"}
                    self.set_embed(data)

                    await interaction.response.send_message(embed=self.base_embed)
                
                finally:
                    self.set_embed(data,  team = interaction.user.top_role)    
                    await interaction.response.send_message("Command executed", delete_after=0.1)
                    await ch.send(embed=self.base_embed)
