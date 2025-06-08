#   Copyright (C) 2023  Kristoffer Gjøsund

#   Discord Repositories
from discord import Intents

from lib.system.discordBot import DiscordBot
from lib.utils.error_handler import ErrorHandler
from lib.system.faq import FrequentlyAskedQuestions

#   Moderation libraries
from lib.modules.moderation.administrator import Administrator
from lib.modules.moderation.role_moderation import RoleModeration
from lib.modules.moderation.member_moderation import MemberModeration
from lib.modules.moderation.channel_moderation import ChannelModeration

class DiscordSetup():

    def __init__(self):

        self.intents = Intents()
        self.bot = DiscordBot(intents=self.initialize_intents())

        return

    def initialize_intents(self):
        #  General Interaction
        self.intents.bans = True                            #   Allows the bot to ban / unban members
        self.intents.emojis = True                          #   emoji, sticker related events
        self.intents.guilds = True                          #   Allows the bot to interect with guilds 
        self.intents.members = True                         #   Allows the bot to interact with members
        self.intents.presences = True                       #   Allows the bot to track member activity (presence_update, member.activities, status, raw status)
        
        #   Messaging and Communication
        self.intents.typing = True                          #   Allows the bot to show typing indicator inside both Guild & DM (message.content, embeds, attatchments, message components)
        self.intents.messages = True                        #   Allows the bot to send messages to both Guild & DM (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        self.intents.message_content =True                  #   Allows the bot to send embeded message (content, embeds, attachments, components)
        
        #   Direct Message and Guild Specific
        #self.intents.dm_typing = True                       #   Allows the bot to indicate a typing indicator in Direct Message (message.content, embeds, attatchments, message components)
        #self.intents.dm_messages = True                     #  Allows the bot to send messages in direct messages only (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        #self.intents.dm_reactions = True                    #  Allow the bot to react in direct messages only (reaction_add, reaction_remove, reaction_clear)
        #self.intents.guild_typing = True                    #   Allows the bot to indicate a typing indicatior inside the Guild (message.content, embeds, attatchments, message components)
        #self.intents.guild_messages = True                     #   Allows the bot to send messages inside guild only (message_edit, message_delete, cached_messages, get_message, reaction_add, reaction_remove, )
        #self.intents.guild_reactions = True                 #   Allows the bot to add reactions with-in the guild  (reaction_add, reaction_remove, reaction_clear)
        
        #   Miscellaneous Events
        #self.intents.invites = True                        #   Invite related events
        #self.intents.webhooks = True                       #   Webhook related events
        #self.intents.reactions = True                      #   Allows the bot to send reaction to both guild & DM (reaction_add, reaction_remove, reaction_clear)
        #self.intents.integrations = True                   #   integrations related events
        #self.intents.voice_states = True                   #   voice states related events 
        #self.intents.scheduled_events = True               #   scheduled event related events (create, update, delete, user_add, user_remove, get_scheduled_events)
        #self.intents.auto_moderation_execution = True      #   moderation execution related events (action_execution)
        #self.intents.auto_moderation_configuration = True  #    moderation configuration events (create, update and rule_delete)
        
        return self.intents

    def system_setup(self):
        self.bot.add_cog(ErrorHandler(self.bot))
        self.bot.add_cog(FrequentlyAskedQuestions(self.bot))

    def moderation_setup(self):
        #
        self.bot.add_cog(Administrator(self.bot))
        #self.bot.add_cog(RoleModeration(self.bot))
        self.bot.add_cog(MemberModeration(self.bot))
        self.bot.add_cog(ChannelModeration(self.bot))
