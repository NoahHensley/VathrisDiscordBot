import discord
from os import getenv
from dotenv import load_dotenv
from random import *
from datetime import datetime, timedelta

load_dotenv()

TOKEN = getenv('TOKEN')

# Creating the Discord client
bot_intents = discord.Intents.default()
bot_intents.message_content = True
client = discord.Client(intents=bot_intents)


"""
There are two types of inputs: dice and ranges.
The dice always go by the format "1dN", where n is an integer greater than or equal to 1. This will
randomize an integer in between 1 and n (both ends included).

If an integer in the range 1-100 is randomized (such as with a 1d100), then the numbers 1-3 mean an "extreme
success" and the numbers 97-99 mean an "extreme failure". In addition to showing the roll, the bot will
announce when this happens.
"""


def is_integer(string):
    try:
        value = int(string)
        return value == float(string)
    except ValueError:
        return False


def check_dice_format(dice):
    try:
        if dice[0] == "1" and dice[1] == "d":
            dice = dice[2:]  # Retrieves "number" from message
            if not is_integer(dice): return False  # Checks if "number" is integer
            dice = int(dice)  # Converts dice var to integer
            if dice < 1: return False  # Tests if dice var is at least 1
            return True  # Good input
        else:
            return False
    except Exception:
        return False


def check_range_format(range_input):
    for num in range_input:
        if not is_integer(num):
            return False
    return True


@client.event
async def on_ready():
    print("The bot has logged in as " + str(client.user) + ".")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/roll"):
        print(message.author.name + " says " + message.content + " (" + str(datetime.now()) + ")")

        args = message.content.split()[1:]
        if len(args) == 1:  # Input is a dice
            dice = args[0]
            if not check_dice_format(dice):  # Stops if invalid input
                await message.channel.send("Usage: /roll 1dN, where N is an integer greater than 0.")
                return
            dice = int(dice[2:])
            roll = randint(1, dice)

            extreme_message = ""
            if dice == 100:
                if roll <= 3:
                    extreme_message = "CRITICAL SUCCESS!\n"
                if roll >= 97:
                    extreme_message = "Critical FAIL!\n"

            message_send = extreme_message + str(roll)
            await message.channel.send(message_send)
            print(message_send)

        elif len(args) == 2:  # Input is a range
            range_input = [args[0], args[1]]

            if not check_range_format(range_input):
                await message.channel.send("Usage: /roll A B, where A and B are integers.")
                return

            message_send = str(randint(int(range_input[0]), int(range_input[1])))
            await message.channel.send(message_send)
            print(message_send)

        else:
            await message.channel.send("Usage: /roll 1dN or /roll A B.")
            return

        return


client.run(TOKEN)

