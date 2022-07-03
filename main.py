import os
import discord, datetime, asyncio, random
from dotenv import load_dotenv
from discord.ext import commands
import youtube_dl


#default_intents = discord.Intents.default()
#default_intents.members = True
bot = commands.Bot(command_prefix="!")#, intents=default_intents)

#load_dotenv(dotenv_path='config')

#Initialisation du Bot
@bot.event
async def on_ready():
    test_bot_channel = bot.get_channel(992109970340458519)
    print("Le bot est prêt.")
    await test_bot_channel.send(f"<:SugarBenny:968983325458980907> {bot.user.display_name} est en ligne ! <:SugarBenny:968983325458980907>")
    await hydrate()


#Fonction de Bienvenue
@bot.event
async def on_member_join(member):
    general_channel = bot.get_channel(368505799666040834)
    #await member.send(f"<:SugarBenny:968983325458980907> Bienvenue sur le serveur : {member.display_name} ! <:SugarBenny:968983325458980907>")
    await general_channel.send(f"<:SugarBenny:968983325458980907> Bienvenue sur le serveur : {member.display_name} ! <:SugarBenny:968983325458980907>")


#Fonction pour supprimer des messages
@bot.command(name="del")
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()
    for each_message in messages:
        await each_message.delete()


@bot.event
async def hydrate():
    while True:
        general_channel = bot.get_channel(368505799666040834)
        now = datetime.datetime.now()
        then = now+datetime.timedelta(hours=3)
        then.replace(second=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        await general_channel.send("<:DrinkBlacky:968960217461174323> Pensez à vous hydrater !! <:DrinkBlacky:968960217461174323>", delete_after=9000)

@bot.command(pass_content = True)
async def play(ctx, url : str):
    if not (ctx.voice_client):
        await ctx.send('Joining..')
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("Bruh")

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("pause !")

@bot.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("pausen't !")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_client, guild=ctx.guild)
    voice.stop()
#@bot.event
#async def on_message(message):
 #   if (message.author.id == 190155770854244353):
  #      channel = message.channel
   #     await channel.send("Super cringe wow")

bot.run(os.environ["TOKEN"])

