<h1 align="center"> PyMod Documentations</h1>

<h2 align="center">Table of content</h2>

## [Introduction](#introduction)
> [the Maintainer](#the-maintainer)<br>
> [project information](#project-info)<br>

## [PyMod](#pymod)

> [How to use the bot](#how-to-use-the-bot)<br>
> [What makes the bot unique](#what-makes-this-bot-unique)<br>

## [Features](#features)

> [Community Module](#community-module)<br>
> [Moderation commands](#moderator-commands)<br>
> [Administrator commands](#administrator-commands)<br>

## [Credentials](#credentials)

> [Disclamers](#disclaimer)
> [Responsories](#responsories)
> [Licence](#licence)


## Introduction

###  The Maintainer

goes by the name Kristoffer, born in 94, :flag_no:.<br>
maintaining Python & SQL projects<br>
otherwise just being a human.

### Project info

> Project start :<br>
>   20.02-23
>
>   Last update :<br>
>   25.02-23
>
>   SQL Database:<br>
>   mariadb

##   Pymod

The bot is a discord moderator command assistant,<br>
Intention of the bot is to easy accsess discord moderation system.

### What makes this bot unique

The unique thing about this bot, its made of love and its not automatically gen

### How to use the bot

The bot uses Slash command, "/" (eg. **/help frequentlyaskedquestions**)

## Features

## <h2 align = "center"> Community module</h3>

Commands which is available for everyone.
> /community botinfo (optional parameter : log, todo, bug )<br>
> * if the command is executed with out or any other arguments than listed,Information about the bot will appear.
>   *   Log parameter returns the changelog information
>   *   todo parameter returns whats planned further to do.
>   *   bug parameter allows server members to send a direct message to  the developer to report a bug
>
> /community meme (optional parameter : reddit<br>
> *     if the command is executed without any arguments, a meme from a random hoster
>*  reddit argument notifies the program to send only meme from reddit.
>
> /community members (optional parameters : off, on<br>
> * list of members in the server
> * on argument retruns only server members which is online
> * off argument returns only offline members.
>
> /community roles<br>
> * List the server roles
>
> /community poll
>  -    Creates a poll
>
> /community report
>   -   Reporting a member for his / her behavior
>
> /community support
>   -   Creating a post in the support channel

## Bot Post Moderation Utility

<h2 align = "center"> Introduction</h3>

The bot has been coded to automatically generate roles and channels.

### Channels
>   log<br>
>   -   A category to store the listed text channels.
>   auditlog<br>
>   -   A channel log
>
>   member-support<br>
>   -   Generates a new post in help and support
>
>   member-report<br>
>   -   Reporting a members behavior


### <h2 align="center"> Moderation Module</h2>

Note : Most of the commands is recorded in the auditlog channel

Note : The targeted member will be notified if commands such as warn, sush, lift, kick, ban is used, the member will get a clear understanding for the left brain thought "why" it has happend

####  **Moderators with manage_channels**

Commands which requires **manage_channels**
>   /channel clear (channel name) (int)
>  -    Clear the chat limit 100 lines each time the command is used
>   -   Limited to channel duplicates, due to an deletion error.
>
>   /channel create (channel type), (name), (age_restricted), (bitrate), (category), (delay), (user_limit), (perm), *(topic), (**reason)
>   -   Channel_type, is required to contain either (text / forum / voice, stage or category). So the program knows what type of channel the user would like to create.
>   -   name, is required to type in, so the program knows what you would like to call the channel.
>   -   age_restricted has a default value of False, if you would like to restrict the channels for adults add True as value.
>   -   category, has a default value to None, if you would like to select a category for the channel, type in the name of the category.
>   -   delay has a default value of 0, if you would like slow peoples posts set it to a desired number, can not be less than 0.
>   -   user_limit, limits how many users can be at once in a VOICE channel.
>   -   perm, overwrites whom can view the channel, default to hidden.
>   -   topic, notify moderators / admins what the channel is used for
>   -   Reason to add to the auditlog
>
>   /channel delete (channel name)
>   -   Deletes a channel if it exists<br>
>
>   /channel clear (channel name)
####  **Moderators with manage_member**

Commands which requires **moderate_members**
>   /member warn (member name), (reason)<br>
>   /member sush (member name), (time), (reason)<br>
>   /member lift (member name)<br>

Commands which requires **kick_members**
> /member kick (member name), (reason)


####  **Moderators with manage_Roles**

Commands which requires **manage_roles**

>   /role delete* (roleName)
>   ~~/role create~~
>   /role modify
>   /role add


#### **List of Premade Permissions**

>   Members ()
>   -   Full Membership Permissions
>   -   Chat previligies, Stream previliges & Voice Previliges
>   -   Chat Permissions only
>   -   permissions enabled :<br>Send_messages,<br> add_reactions,<br> external_emojis,<br> read_message_history & use_slash_commands<br>

>  StreamPermissions
>  -    permissions enabled : stream
>
>   VoicePermissions
>   -   permissions enabled :<br> speak, connect,<br> request_to_speak,<br> send_tts_messages,<br> use_voice_activation

>   Moderator
>
>   Server Moderator
>   -   Manages the guilds with manage_guild, and other  permissions for moderators.
>
>   Role Moderator
>   -  Can manage roles with mange_roles permissions
>
>   Voice Moderator
>   -   They're able to move, mute, deafen members. They have priority_speaker previliges
>
>   Member Moderator
>   -    They're able to manage nicknames & moderate members
>
>   Headmoderator
>   -   Has every moderation possiblities the other moderation type + they're able to kick members


<h2 align="center"> Administrator module</h2>

>   /ban member (member) (reason)
>  -   Ban a discord user from the server
>
>   /ban list
>  -    View a list of banned server members
>
>   /ban unban* (member)
>   -   Unban a discord user from the server
>
>   /misc announce (channelName)
>  -   Opens a modal, where you can create a announcement in the given channel as the bot. The author will be the member whom invoked the commannd.

##  Credentials

### Responsories

-   pycord.py by [Pycord Development](https://github.com/Pycord-Development/pycord),
-   ~~Anti-Spam by [Skelmis](https://github.com/Skelmis/DPY-Anti-Spam/commits?author=Skelmis)~~,
-   humanfriendly by [Peter Odding](https://github.com/xolox/python-humanfriendly),
-   MariaDB by [MariaDB Community](https://github.com/mariadb-corporation/mariadb-connector-python),
-   python_dotenv by [Saurabh Kumar](https://github.com/motdotla/dotenv),

### API

no apis used in the project

### Disclaimer

The developer can only have the responsibility,<br>
for how the projects is created, how it is used,<br>
is another story. 

[Terms of Use](), [Privacy Policy notice]()<br> 

### [Licence](https://github.com/krigjo25/Discord/blob/main/licence)

### Contact information

-   Discord : krigjo25#5588<br>
-   Messenger : krigjo25<br>
-   website :