from discord.channel import TextChannel
from discord_classes import WordleBot
from wordle_classes import Game
import sys
from re import match, compile, sub

assert sys.version_info >= (3, 10)

print(f"Executing bot with Python version: {sys.version}")

with open("bot_token.txt", "r") as f:
    bot_token = f.readline()

bot = WordleBot()

active_games = {}

wordle_regex = compile("^w[ \t\r\n\f]+[A-zÀ-ú]{5}$")


@bot.event
async def on_ready():
    print(f"Ready and running as {bot.user}")


@bot.event
async def on_message(message):
    if not isinstance(message.channel, TextChannel):    # if the message was not sent through a text channel
        return
    if not match(wordle_regex, message.content):    # if the pattern does not match
        await bot.process_commands(message)
        return
    try:
        selected_game = active_games[message.author.id]

    except KeyError:                        # if the author has no active game
        await message.channel.send("It looks like you haven't started any game. Try using **w!play** first!")
        return
    guessed_word = sub("w[ \t\r\n\f]+", "", message.content)
    game_status, view, content = selected_game.guess_word(guessed_word)
    if game_status in [-1, 1]:  # game ended
        await message.channel.send(content=content)
        del active_games[message.author.id]
    else:
        await message.channel.send(view=view, content=content)


@bot.command(pass_context=True, aliases=["start", "s", "p", "new", "game"])
async def play(context, language: str = "ita", attempts: int = 6):
    player = context.message.author.id
    if player in active_games:      # starting a new game overwrites the previous one
        del active_games[player]
    active_games[player] = Game(language=language, attempts=attempts)
    content = "You started a new game. Type your first guess! (syntax: 'w YOURGUESS')"
    await context.send(content=content)


bot.run(bot_token)
