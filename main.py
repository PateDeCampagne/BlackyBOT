import os
import discord, datetime, asyncio
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
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        await ctx.send('Wait for the current playing music to end or use the <stop> command')


    await ctx.send('Joining..')
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Bruh")

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'))

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Je suis pas connecté chakal")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_client, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('Je parle pas wsh')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_client, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Je chante déjà')

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_client, guild=ctx.guild)
    voice.stop()

bot.run(os.environ["TOKEN"])

