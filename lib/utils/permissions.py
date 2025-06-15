#   Discord Repositories

from typing import Optional
import discord as d

from discord.ext import commands


class PermissionUtils(commands.Cog):

    """Utility class for handling permissions in Discord channels."""

    def handle_permissions(self,case: Optional[str] = "default", dict:Optional[dict[str, str]] = {}) -> None:
        """
        Handles the default permissions for channels.
        """
        match(case):
            case "member": self.Member(dict)
            case _ : self.default()

    @staticmethod
    def Member(dict: dict[str, str]) -> d.PermissionOverwrite:

        perm = d.PermissionOverwrite()
        
        for key, value in dict.items():
            if hasattr(perm, key):
                setattr(perm, key, value)


        return perm
    
    @staticmethod
    def default() -> d.PermissionOverwrite:

        perm = d.PermissionOverwrite(
            # Text-Channels
            view_channel=False,
            send_messages=False,
            add_reactions=False,
            external_emojis=False,
            read_message_history=False,
            mention_everyone=False,
            )

        return perm
    
        """perm = d.PermissionOverwrite(
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

        return perm perm = d.PermissionOverwrite(#   Voice
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