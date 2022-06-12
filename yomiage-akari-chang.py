from discord.ext import commands
from apitoken import APITOKEN
from PyVoice import PyVoice
import json

with open("akari_preset.json","r",encoding="utf-8")as f:
    akari_preset=json.load(f)

akari=PyVoice()
bot=commands.Bot("!")
preset_list=akari.GetPresetList()

@bot.event
async def on_ready():
    akari.SetPresetJSON(json.dumps(akari_preset))
    akari.Talk("起動完了")

@bot.event
async def on_message(message):
    if message.content[0]!="!":
        content=f"{message.author.display_name} {message.content}"
        akari.Talk(content)
    await bot.process_commands(message)

@bot.command()
async def change_voice(ctx):
    if akari.GetCurrentPresetName()==preset_list[0]:
        akari.SetPresetName(preset_list[1])
    else:
        akari.SetPresetName(preset_list[0])
    await ctx.send(f"ボイスを{akari.GetCurrentPresetName()}に変更しました")


bot.run(APITOKEN)