
from discord import  Interaction, SelectOption
from discord.ui import Select, View, select

from lib.modal.member import MemberModal

class SupportSelections(View):
    @select(placeholder="Select a topic", options=[                         #   type: ignore
        SelectOption(label="Gerneral Question", value="misc-question"),
        SelectOption(label="Server Support", value="game-support"),
        SelectOption(label="Discord Support", value="discord-support")
    ], custom_id="support_selection")

    async def select_callback(self, select: Select, interaction:Interaction):
        selected_value = str(select.values[0]).lower()
        
        tag = None

        try:
            match(selected_value):
                case "discord-support":
                    tag = str(selected_value).split("-")[0]

                case _:
                    raise ValueError(f"Unknown selection: {selected_value}")
        except ValueError as e:
            return
        else:
            print(tag)
            modal = MemberModal(title="forum-post", custom_id= tag)  #   type: ignore
            await interaction.response.send_modal(modal)