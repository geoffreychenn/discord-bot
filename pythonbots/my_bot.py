import random
import discord
from yt_dlp import YoutubeDL
import os
import time
from discord.utils import get
from discord import client
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix = '?')
bot.remove_command("help")

file = open("../adjectives.txt")
adjectives = file.read().splitlines()
file.close()

file = open("../adverbs.txt")
adverbs = file.read().splitlines()
file.close()

file = open("../questions.txt")
questions = file.read().splitlines()
file.close()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
@bot.command()
async def help(ctx):
    compliment_text = "?compliment: generates a random compliment\n"
    question_text = "?question: generates a random question\n"
    spam_text = "?spam @user: spams a user with mentions in the current text channel\n"
    summon_text = "?summon: summons the bot to users voice channel\n"
    exile_text = "?exile: disconnects the bot from the users voice channel\n"
    music_text = "?play <youtube url>: plays a video from youtube in a voice channel you are in\n?pause, ?resume and ?stop are available\n"
    await ctx.channel.send("COMMAND LIST: \n" + compliment_text + question_text + spam_text + summon_text + exile_text + music_text)    
    
@bot.command()
async def summon(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    
@bot.command()
async def exile(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.send("bot isnt in a voice channel")
    else:
        await ctx.voice_client.disconnect()
    
@bot.command()
async def compliment(ctx):
    rand_adv = random.randint(0, len(adverbs) - 1)
    rand_adj = random.randint(0, len(adjectives) - 1)
    await ctx.send("You are " + adverbs[rand_adv] + " " + adjectives[rand_adj])
    
@bot.command()
async def question(ctx):
    rand_qsn = random.randint(0, len(questions) - 1)
    await ctx.send(questions[rand_qsn])

# TODO
# add queues
@bot.command()
async def play(ctx, url : str):
    try:
        for file in os.listdir("./"):
            if file.endswith(".mp3") or file.endswith(".webm") or file.endswith(".mp4"):
                os.remove(file)
    except PermissionError:
        ctx.send("wait for song to finish or stop it, queues coming soon")
        return
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await summon(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        "format" : "bestaudio/best",
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm") or file.endswith(".mp4"):
            print("Playing: " + file)
            voice.play(discord.FFmpegOpusAudio(file))

    
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
    else:
        await ctx.send("nothing is playing rn")

@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("nothing can be resumed")

@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        voice.stop()
        await ctx.send("stopped playing")

# TODO
# work out what this is
@bot.command()
async def targetQuestion(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.send("bot must be in your voice channel to use this")

@bot.command()
async def spam(ctx, target : str):
    i = 0
    while i < 5:
        await ctx.send(target)
        time.sleep(1.3)
        i = i + 1
    
@bot.event
async def on_presence_update(before, after):
    games = ["leage of legends"]
    print(before)
    print(after)
    if after.activity and after.activity.name.lower() in games:
        await after.create_dm().send(content='you are playing leage of legends', tts=True)


bot.run(TOKEN)