#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from asyncio import sleep
from discord.utils import get
from youtube_dl import YoutubeDL
import requests
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(command_prefix="!")
TOKEN = os.environ["TOKEN"]


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


def search(query):
    with YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
        try:
            requests.get(query)
        except:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        else:
            info = ydl.extract_info(query, download=False)
    return (info, info["formats"][0]["url"])


@bot.command(name="play")
async def play(ctx, *, query=None):
    if query:
        FFMPEG_OPTS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        _, source = search(query)
        voice = get(bot.voice_clients, guild=ctx.guild)

        channel = ctx.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        if not voice.is_playing():
            voice.play(
                discord.FFmpegPCMAudio(source, **FFMPEG_OPTS),
                after=lambda e: print("done", e),
            )
            voice.is_playing()
            await ctx.send(f"Song playing now.")
        else:
            await ctx.send(f"Song running.")
    else:
        await ctx.send("No URL Provided.")


bot.run(TOKEN)