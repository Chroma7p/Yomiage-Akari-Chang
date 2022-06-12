from discord.ext import commands
from apitoken import APITOKEN
from PyVoice import PyVoice

akari=PyVoice()
bot=commands.Bot()

@bot.event
async def on_ready():
    akari.Talk("起動完了")

@bot.event
async def on_message(message):
    content=f"{message.author.display_name}\n{message.content}"
    akari.Talk(content)

bot.run(APITOKEN)