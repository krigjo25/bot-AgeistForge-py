
from discord import  Interaction, SelectOption
from discord.ui import Select, View, select

from lib.modal.member import MemberModal

class SupportSelections(View):
    @select(placeholder="Select a topic", options=[                         #   type: ignore
        SelectOption(label="Server Support", value="game-support"),
        SelectOption(label="Discord Support", value="discord-support")
    ], custom_id="support_selection")

    async def select_callback(self, select: Select, interaction:Interaction):
        selected_value = str(select.values[0]).lower()

        try:
            match(selected_value):
                case "discord-support":
                    tag = str(selected_value).split("-")

                case _:
                    raise ValueError(f"Unknown selection: {selected_value}")
        except ValueError as e:
            return
        else:
            modal = MemberModal(title=f"{selected_value}")  #   type: ignore
            await interaction.response.send_modal(modal)

class ApplicationSelections(View):
    @select(placeholder="Select an application", options=[                   #   type: ignore
        SelectOption(label="Discord-Bot", value="bug-report"),
        SelectOption(label="Game-Server", value="game-server"),
    ], custom_id="application_selection")

    async def select_callback(self, select: Select, interaction:Interaction):
        selected_value = str(select.values[0]).lower()

        modal = MemberModal(title=f"{selected_value}")  #   type: ignore
        await interaction.response.send_modal(modal)