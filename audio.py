#!/usr/bin/env python
# -*- coding: utf-8 -*-
# added opus

import discord
from discord.ext import commands
from asyncio import sleep

PATH = "ivanda.mp3"
bot = commands.Bot(command_prefix="shadow ")
DISCORD_TOKEN = "ODA5Nzg5MzgwOTUyNzE5NDAw.YCaNIQ.uWN9wOdNtBDh_kB9mLCKkdWTPwY"


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.command(name="potta")
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
        and (member.id == 569503886038138900 or member.id == 490916719792095243)
    ):
        voice_channel = member.voice.channel
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                # executable="/usr/bin/ffmpeg",
                executable="/app/vendor/ffmpeg/ffmpeg",
                source=PATH,
            )
        )
        while vc.is_playing():
            await sleep(0.1)
        await vc.disconnect()


bot.run(DISCORD_TOKEN)