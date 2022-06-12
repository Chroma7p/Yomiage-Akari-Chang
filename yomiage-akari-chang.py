from discord.ext import commands
from apitoken import APITOKEN

from PyVoice import PyVoice

akari=PyVoice()
akari.Talk("起動完了")



#botのオブジェクトを作成(コマンドのトリガーを!に)
bot=commands.Bot(command_prefix='!')

#コマンドを設定API
@bot.command()
#"!hello"と送信された時
async def hello(ctx):
    akari.Talk("はろー")
    await ctx.send("hello!")#送信された場所に"hello!"と送り返す

#イベントを検知
@bot.event
#botの起動が完了したとき
async def on_ready():
    print("Hello!")#コマンドラインにHello!と出力

@bot.event
async def on_message(message):#引数は上記のctxみたいなもの、これはMessageクラス
    akari.Talk(message.content)


#起動
bot.run(APITOKEN)