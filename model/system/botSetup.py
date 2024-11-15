#   Discord Repositories
from discord import Intents

#   library Repositories - System module
from model.system.discordBot import DiscordBot                                         #   The Bot Client
from model.system.commandError import ErrorHandler                                     #   Error Handling Module
from model.system.faq import FrequentlyAskedQuestions                                  #   Help module

#   Moderation Utility
from lib.moderation.post_moderation import ChannelModeration, Administrator, MiscModeration, RoleModeration, MemberModeration

class DiscordSetup():

    """
        Copyright (C) 2023  Kristoffer Gjøsund

        Discord bot setup

        >   Creation Date   : 19.02-23
        >   Last update     : 21.02-23

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

        self.intents = Intents()
        self.bot = DiscordBot(intents=self.SystemConiguration())

        return

    def SystemConiguration(self):
        #   Bot intents
        self.intents.guilds = True                          #   Allows the bot to interect with guilds 
        #self.intents.dm_typing = True                       #   Allows the bot to indicate a typing indicator in Direct Message (message.content, embeds, attatchments, message components)
        #self.intents.dm_messages = True                     #  Allows the bot to send messages in direct messages only (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        #self.intents.dm_reactions = True                    #  Allow the bot to react in direct messages only (reaction_add, reaction_remove, reaction_clear)
        #self.intents.guild_typing = True                    #   Allows the bot to indicate a typing indicatior inside the Guild (message.content, embeds, attatchments, message components)
        #self.intents.guild_messages = True                 #   Allows the bot to send messages inside guild only (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        #self.intents.guild_reactions = True                 #   Allows the bot to add reactions with-in the guild  (reaction_add, reaction_remove, reaction_clear)

        self.intents.bans = True                            #   Allows the bot to ban / unban members
        self.intents.emojis = True                          #   emoji, sticker related events
        self.intents.typing = True                          #   Allows the bot to show typing indicator inside both Guild & DM (message.content, embeds, attatchments, message components)
        self.intents.members = True                         #   Allows the bot to interact with members
        self.intents.messages = True                        #   Allows the bot to send messages to both Guild & DM (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        #self.intents.reactions = True                      #   Allows the bot to send reaction to both guild & DM (reaction_add, reaction_remove, reaction_clear)
        self.intents.presences = True                       #   Allows the bot to track member activity (presence_update, member.activities, status, raw status)
        self.intents.message_content =True                  #   Allows the bot to send embeded message (content, embeds, attachments, components)
        
        #self.intents.webhooks = True                       #   Webhook related events
        #self.intents.invites = True                        #   Invite related events
        #self.intents.voice_states = True                   #   voice states related events 
        #self.intents.integrations = True                   #   integrations related events
        #self.intents.scheduled_events = True               #   scheduled event related events (create, update, delete, user_add, user_remove, get_scheduled_events)
        #self.intents.auto_moderation_execution = True      #   moderation execution related events (action_execution)
        #self.intents.auto_moderation_configuration = True  #    moderation configuration events (create, update and rule_delete)
        
        return self.intents

    def SystemSetup(self):

        #   Add Cogs
        self.bot.add_cog(ErrorHandler(self.bot))
        self.bot.add_cog(FrequentlyAskedQuestions(self.bot))

        return

    def ModerationSetup(self):

        self.bot.add_cog(Administrator(self.bot))
        self.bot.add_cog(MiscModeration(self.bot))
        self.bot.add_cog(MemberModeration(self.bot))
        self.bot.add_cog(ChannelModeration(self.bot))
        


        return
