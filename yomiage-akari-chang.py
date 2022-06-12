from discord.ext import commands
from apitoken import APITOKEN
from PyVoice import PyVoice

akari=PyVoice()

bot=commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    akari.Talk("起動完了")

@bot.event
async def on_message(message):
    akari.Talk(message.content)

bot.run(APITOKEN)