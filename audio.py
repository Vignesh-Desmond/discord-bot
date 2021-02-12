#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from asyncio import sleep

PATH = ""
MEMBER_ID = ""
DISCORD_TOKEN = ""

bot = commands.Bot(command_prefix="sentience ")


@bot.command(name="paatu")
async def mp3player(ctx):
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
    await ctx.message.delete()


@bot.event
async def on_voice_state_update(member, before, after):
    print("\n")
    print(after)
    print("\n")
    if before.channel is None and after.channel is not None and member.id == MEMBER_ID:
        voice_channel = member.voice.channel
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(
            discord.FFmpegPCMAudio(
                executable="/usr/bin/ffmpeg",
                source=PATH,
            )
        )
        while vc.is_playing():
            await sleep(0.1)
        await vc.disconnect()


bot.run(DISCORD_TOKEN)