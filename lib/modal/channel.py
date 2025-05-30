

#   Discord responsory
import discord as d
from discord import utils
from discord.ui import InputText, Modal

class Channel(Modal):

    """
        Channel modals

        #   Author : krigjo25
        #   Date :   21.02-23
        #   Last update: 22.02-23

        #   Server announcements
        #   Create multiply channels
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embed = d.Embed()
        self.kwargs = [kwargs]

        for i in self.kwargs:

            match i["title"]:
                case "Channel Announcement": self.announcement()
                case "Channel Creation": self.channel()

        return

    def announcement(self):

        self.add_item(InputText(label = "channel name", placeholder = "eg. announcement", style= d.InputTextStyle.short))
        self.add_item(InputText(label = "title", placeholder = "eg. announcement", style = d.InputTextStyle.short))
        self.add_item(InputText(label = "url", placeholder = "url", style = d.InputTextStyle.short, required = False,))
        self.add_item(InputText(label = "What would you like to announce?", placeholder = "Some text you would like to announce", style = d.InputTextStyle.long))

        return

    async def callback(self, interaction:d.Interaction):

        match self.title:
            case "Channel Announcement":

                modal = [{
                            "channel_name":self.children[0].value.lower(),
                            "announcement_title":self.children[1].value.capitalize(),
                            "announcement_url":self.children[2].value.lower(),
                            "announcement_message":self.children[3].value}]

                ch = utils.get(interaction.guild.channels, name = self.children[0].value)   #   Fetch the channel

                try:
                    if not ch: raise Exception("Channel does not exits")

                except Exception as e:

                    self.embed.title = "An Exception Occured"
                    self.embed.description = e

                    await interaction.response.send_message(embed=self.embed)
                    return

                else:
                    for i in modal:

                        self.embed.title = i["announcement_title"]
                        self.embed.set_author(name = f"by {interaction.user.name}")
                        if i["announcement_url"] != None: self.embed.url = i["announcement_url"]
                        self.embed.description = i["announcement_message"]
                    await ch.send(embed = self.embed)
                    await interaction.response.send_message("Message responded", delete_after=0.1)

                    return

        del interaction, modal#   Clearing some memory
        self.embed.clear_fields()
        self.embed.description = ""
        self.embed.remove_author()
        return
