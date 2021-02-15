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
import os
from dotenv import load_dotenv


load_dotenv()
client = discord.Client()
TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["ID"])
screenshot_count = 0


def take_screenshot():
    left = 513
    top = 349
    right = 1617
    bottom = 1079
    ss_image = ImageGrab.grab().convert("RGB")
    im = ss_image.crop((left, top, right, bottom))
    na = np.array(im)
    lavenderY, lavenderX = np.where(np.all(na == [222, 242, 248], axis=2))
    top, bottom = lavenderY[0], lavenderY[-1]
    left, right = lavenderX[0], lavenderX[-1]
    ROI = na[top:bottom, left:right]
    cropped_image = Image.fromarray(ROI)
    return cropped_image


def pytesseract_ocr(image):
    # If only question is needed
    # na = np.array(image)
    # whitesmokeY, _ = np.where(np.all(na == [237, 244, 246], axis=2))
    # # if whitesmokeY.size == 0:
    # #     greyY, _ = np.where(np.all(na == [233, 236, 239], axis=2))
    # #     topgrey = greyY[0]
    # #     ROI = na[: topgrey - 40, :]
    # # else:
    # topwhitesmoke = whitesmokeY[0]
    # ROI = na[: topwhitesmoke - 40, :]
    # final = Image.fromarray(ROI)
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
    channel = client.get_channel(CHANNEL_ID)
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
                description=ocr_text,
                timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
            )
            embed.set_image(url="attachment://image.png")
            await channel.send(file=file, embed=embed)
            await asyncio.sleep(1)
            await channel.send("** **")
        print("Screenshot sent")
        await asyncio.sleep(1)


if __name__ == "__main__":
    client.run(TOKEN)
