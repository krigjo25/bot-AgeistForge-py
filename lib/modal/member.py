#   Python responsories
import datetime

#   Discord responsory
import discord as d
from discord import utils, Colour
from discord.ui import InputText, Modal


class Member(Modal):

    """

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embed = d.Embed()
        self.kwargs = [kwargs]

        for i in self.kwargs:

            match i['title']:
                case "Member Report": self.report()
                case "Member Support": self.support()

        return

    def report(self):

        self.add_item(InputText(label = "Member", placeholder= "Member Name"))
        self.add_item(InputText(label = "Uniform Resource Locator (URL)", style=d.InputTextStyle.long, required= True, placeholder= "https://google.com"))
        self.add_item(InputText(label = "Reason", style=d.InputTextStyle.long, required= False, placeholder= ""))
        self.embed.colour = d.Colour.dark_red()

        return

    def support(self):

        self.add_item(InputText(label = "Title Of The Document", placeholder= "eg. How To Use Commands", style=d.InputTextStyle.short))
        self.add_item(InputText(label = "Image", placeholder= "Member", style=d.InputTextStyle.short))
        self.add_item(InputText(label = "Challange", placeholder= "What do you need help with?", style=d.InputTextStyle.long))
        self.embed.colour = d.Colour.dark_red()
        return
    
    def bugreport(self): pass
    async def callback(self, interaction:d.Interaction):

        for i in self.kwargs:

            match i['title']:
                case "Member Report": ch = utils.get(interaction.guild.text_channels, name = "report")
                case "Member Support":ch = utils.get(interaction.guild.text_channels, name = "support")


        try:

            if not ch: raise Exception(f"{ch} does not exists")

        except Exception as e:
     
            ch = utils.get(interaction.guild.channels, name = "auditlog")

             #   Prepare the embed message
            self.embed.description = f" {e}"
            self.embed.title = "An Exception Occured"
            self.embed.timestamp = datetime.datetime.now() 

            await ch.send(embed= self.embed)    #   Send the modal response

        else:

            #   Prepare the embed message
            self.embed.title = self.title
            self.embed.timestamp = datetime.datetime.now() 
            self.embed.set_author(name = f"Author: {interaction.user.name}")


            #   Prepare the user mode
            for i in range(len(self.children)): self.embed.add_field(name = self.children[i].label, value = self.children[i].value, inline= False)

            await interaction.response.defer()  #   Save the modal response
            await ch.send(embed= self.embed)    #   Send the modal response

        del ch, interaction
        return
