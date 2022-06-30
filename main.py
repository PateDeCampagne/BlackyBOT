import os
import discord, random, json, requests, datetime, asyncio
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv(dotenv_path='config')

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!", intents=default_intents)

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
        await general_channel.send("<:DrinkBlacky:968960217461174323> Pensez à vous hydrater !! <:DrinkBlacky:968960217461174323>")


bot.run(os.environ["TOKEN"])

