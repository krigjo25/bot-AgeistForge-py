#   Python Repositories

#   Discord Repositories
from discord.ext import  commands
from discord import SlashCommandGroup, ApplicationContext

import lib.modal.channel as Channel

class CommunityModule(commands.Cog):
    """
    Community Module for managing community-related commands and interactions.
    This class inherits from commands.Cog and implements various community-related commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    community_group = SlashCommandGroup( name = 'community', description = 'Community related commands' )
    @community_group.command(name='Support', description='Requuest support from the community')
    async def member_support(self, ctx:ApplicationContext):
        """
        Command to display information about the community.
        """
        channel = Channel().create_modal(ctx, self.member_support.__name__)