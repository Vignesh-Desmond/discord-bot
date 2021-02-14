#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, tasks
import asyncio
from PIL import Image, ImageEnhance, ImageFilter, ImageGrab
from io import BytesIO
import keyboard
from datetime import datetime
import pytz
import numpy as np
import pytesseract

client = discord.Client()
TOKEN = ""
screenshot_count = 0


def take_screenshot():
    left = 503
    top = 390
    right = 1617
    bottom = 1079
    image = ImageGrab.grab().convert("RGB")
    im = image.crop((left, top, right, bottom))
    na = np.array(im)
    yellowY, yellowX = np.where(np.all(na == [222, 242, 248], axis=2))
    top, bottom = yellowY[0], yellowY[-1]
    left, right = yellowX[0], yellowX[-1]
    ROI = na[top:bottom, left:right]
    return Image.fromarray(ROI)


def pytesseract_ocr(image):
    text = pytesseract.image_to_string(image, config="--psm 6 --oem 3")
    return text


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    screenshot_takeNsend.start()


@tasks.loop(seconds=0.2)
async def screenshot_takeNsend():
    channel = client.get_channel()
    if keyboard.is_pressed("ctrl + b"):
        global screenshot_count
        screenshot_count += 1
        with BytesIO() as image_binary:

            screenshot_image = take_screenshot()
            screenshot_image.save(image_binary, "PNG")
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="image.png")

            ocr_text = pytesseract_ocr(screenshot_image)
            embed = discord.Embed(
                title=f"Screenshot {screenshot_count}",
                colour=discord.Colour(0xD8C538),
                description=pytesseract_ocr(screenshot_image),
                timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
            )
            embed.set_image(url="attachment://image.png")

            # await channel.send(file=file)
            await channel.send(file=file, embed=embed)
        print("Screenshot sent")
        await asyncio.sleep(1)


if __name__ == "__main__":
    client.run(TOKEN)
