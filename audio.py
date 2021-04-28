#!/usr/bin/env python
# -*- coding: utf-8 -*-
# added opus

import discord
import random
from discord.ext import commands
from asyncio import sleep
from dotenv import load_dotenv
import os

PATH_LIST = ["./audio.mp3", "./audio2.mp3"] # AUDIO PATHS HERE
PATH = random.choice(PATH_LIST)

load_dotenv()

bot = commands.Bot(command_prefix="!")
TOKEN = os.environ["TOKEN"]

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.command(name="lol")
async def mp3player(ctx):
    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                executable="/usr/bin/ffmpeg",
                source=PATH,
            )
        )
        # Sleep while audio is playing.
        while vc.is_playing():
            sleep(0.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()


@bot.event
async def on_voice_state_update(member, before, after):
    if (
        before.channel is None
        and after.channel is not None
        and (member.id == "<ID_HERE>" or member.id == "<ID_HERE>") # extend or for multiple users
    ):
        voice_channel = member.voice.channel
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                executable="/usr/bin/ffmpeg",
                # executable="/app/vendor/ffmpeg/ffmpeg",
                source=PATH,
            )
        )
        while vc.is_playing():
            await sleep(0.1)
        await vc.disconnect()


bot.run(TOKEN)