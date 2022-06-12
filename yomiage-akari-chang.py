from discord.ext import commands
from apitoken import APITOKEN
from PyVoice import PyVoice
import json

with open("akari_preset.json","r",encoding="utf-8")as f:
    akari_preset=json.load(f)


akari=PyVoice()
bot=commands.Bot("!")



@bot.event
async def on_ready():
    akari.SetPreset(akari_preset)
    akari.Talk("起動完了")

@bot.event
async def on_message(message):
    content=f"{message.author.display_name} {message.content}"
    akari.Talk(content)

bot.run(APITOKEN)