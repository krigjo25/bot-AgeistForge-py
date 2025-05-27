#   Discord Repositories
import discord as d
from discord.colour import Colour


from discord.ext.commands import Cog


class ChannelPermissions(Cog):

    """
        Copyright (C) 2023  Kristoffer Gjøsund

        Permissions of the Discord Channels

        >   Creation Date   : 18.02-23
        >   Last update     :

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
    """
    def __init__(self):

        self.embed = d.Embed(color=Colour.dark_purple())

        return

    async def SelectPermissions(self, ctx:d.ApplicationContext, arg, role = None):

        if role == None: role = ctx.guild.default_role
        match str(arg).lower().replace(" ",""):
            case "member": return self.Member()
            case "none": return self.hidden(role)

    def hidden(self, role): return {role :d.PermissionOverwrite(view_channel = False,)}

    def Member(self):

        perm = d.PermissionOverwrite(
                                                # Text-Channels
                                                send_messages=True,
                                                add_reactions = True,
                                                external_emojis = True,
                                                change_nickname = True,
                                                manage_messages = False,
                                                manage_webhooks = False,
                                                manage_channels = False,
                                                mention_everyone = False,
                                                read_message_history=True,
                                                create_instant_invite = False)

        return perm
"""perm = d.PermissionOverwrite(#   Voice
                                                speak = True,
                                                connect = True,
                                                request_to_speak = True,
                                                send_tts_messages = True,
                                                use_voice_activation = True,

                                                #   Stream
                                                stream = True,

                                                # Text-Channels
                                                send_messages=True,
                                                add_reactions = True,
                                                external_emojis = True,
                                                read_message_history=True,
                                                mention_everyone = False,

                                                #   Manage Permissions
                                                ban_members = False,
                                                kick_members = False,
                                                manage_guild = False, 
                                                manage_roles = False,
                                                manage_emojis = False,
                                                manage_messages = False,
                                                manage_channels = False,
                                                manage_nicknames = False,
                                                change_nickname = False,
                                                moderate_members = False,
                                                manage_webhooks = False,

                                                #   Voice permissions 
                                                move_members = False,
                                                mute_members = False,
                                                deafen_members = False,
                                                priority_speaker = False,  
                        
                                                #   Server Settings permissions
                                                view_audit_log = False,
                                                view_guild_insights = False,
                                                create_instant_invite = False)"""