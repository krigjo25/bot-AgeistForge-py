# Python Responsories
from random import randrange, shuffle

class Dictionaries():
    def __init__(self):
        pass

    #   Emojies
    def BotPoll (x):

        dictionary = {   
                    1:'1️⃣',
                    2:'2️⃣',
                    3:'3️⃣',
                    4:'4️⃣',
                    5:'5️⃣',
            }

        return dictionary.get(x)

    def EmojiDictionary ():

        #   Creating a dictionary for emojies
        dictionary = {
                    1: ':astonished',
                    2:':alien:',
                    3:':blush:',
                    4:':boom:',
                    5:':cold_sweat:',
                    6:':confounded:',
                    7:':no_mouth:',
                    8:':scream:',
                    9:':joy:',
                    10:':grin:',
                    11:':grinning:',
                    12:':grimacing:',
                    13:':smiley:',
                    14:':sparkles:',
                    15:':smile:',
                    16:':laughing:',
                    17:'smirk:',
                    18:':two_hearts:',
                    19:':+1:',
                    20:':muscle:',
                    21:':question:',
                    22:':see_no_evil:',
                    23:':fire:',
                }

        #   Randomize the dictionary
        x = len(dictionary)
        x = randrange(1,x)

        return dictionary.get(x)

    def RoleColours(color):

        #   Creating a dictionary for Colours
        dictionary = {
                    'red':0x93020D,
                    'darkred':0x8A2425,
                    'blue':0x003366,
                    'darkblue':0x03001C,
                    'purple':0x36084F,
                    'darkpurple':0x3E0035,


                }

        return dictionary.get(color)

class CommandDictionary():
    def __init__(self) -> None:
        pass

    def ErrorDictionary (self, ctx, errorModule, *cmd):

        cmd = str(ctx.command)
        errorModule = str(errorModule)

        if errorModule == 'CommandNotFound':

            dictionary = {
                            1:'meep morp zeep :(\n',
                            2:f'Sir, an error has emerged \"{cmd}\" were not found in bot command dictionary',
                            2:'Sir, have you drunken to much?',
                            3:'Sir, you\'ve started the "Self destruction protocol", press "enter" to continue, press "esc" to stop.',
                            4:'Sir, im sorry, could you please repeat the command?',
                            5:'Sir The command has not been impleted in my software',
                            6:f'Sir where did you find the "{cmd}" ',
                            7:f'I have some good news, sir. Im a good boy, i didnt execute {cmd}',
                            8:f'We all do mistakes, sometimes.. There is no user with {ctx.author} name',
                            9: '0101010001101000011001010010000001100011011011110110110101101101011000010110111001100100001000000110010001101111011001010111001100100000011011100110111101110100001000000110010101111000011010010111001101110100',
                            10:'Given command does not exists'
}

        elif errorModule == 'MemberNotFound':

            dictionary = {
                            1:'meep, morp, zeep :(\n',
                            2:'Sir, imagne the member where found\n',
                            3:'Sir, if the error continues, check your spelling \n',
                            4:'I regret to inform you, sir. the selected member does not exist, should i make one? \n',
                            5:'010110010110111101110101001000000100010001101111001000000110111001101111011101000010000001101000011000010111011001100101001000000111010001101000011001010010000001110010011001010111000101110101011010010111001001100101011001000010000001110010011011110110110001100101\n',
                            6:'I\'m the bot version for the 99th emoji !',
                            7:f'Just sent out an APB of {ctx.author}',
                            8:'We all do mistakes, this time the user doesn\'t exist',
}

        elif errorModule == 'CheckFailure':

            dictionary = {
                            1:'meep, morp, zeep :(\n',
                            2:'Sir, imagne the member where found\n',
                            3:'Sir, if the error continues, check your spelling \n',
                            4:'I regret to inform you, sir. the selected member does not exist, should i make one? \n',
                            5:'010110010110111101110101001000000100010001101111001000000110111001101111011101000010000001101000011000010111011001100101001000000111010001101000011001010010000001110010011001010111000101110101011010010111001001100101011001000010000001110010011011110110110001100101\n',
                            6:'I\'m the bot version for the 99th emoji !',
                            7:f'Just sent out an APB of {ctx.author}',
                            8:'We all do mistakes, this time the user doesn\'t exist',
}

        elif errorModule == 'MissingRequiredArgument':

            dictionary = {
                            1:'meep, morp, meep :(\n',
                            2:'Sir, i just executed the command with-out any arguments...',
                            3:'Sir, should i just fake it?\n',
                            4:'More infomation would do my job easier..',
                            5:'Still missing some leads..',
                            6:'We all do mistakes. You\'re missing some requred arguments ',
}

        elif errorModule == 'TimeoutError':

            dictionary = {
                            1:'meep, morp, zeep :(\n',
                            2:'Sir, the BOENG 437 just left the airport',
                            3:'Sir, do you need more time?',
                            4:f'The game is over, {ctx.author.mention} just ran out of time.',
                            5:'Try again',
                            6:'Decided to cancel the game.',
                            7:'Never got a response in time',
}

        else:
            print(errorModule)
            dictionary = {
                            1:'the content of the command which where sent is raising "DivisionByZero" a detailed report is sent.',
}

        #   Randomize the dictionary
        x = len(dictionary)
        x = randrange(1,x)

        return dictionary.get(x)