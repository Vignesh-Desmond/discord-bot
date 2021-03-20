#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import asyncio
import random
import discord
from discord.ext import commands, tasks
from pymongo import MongoClient

# from dotenv import load_dotenv
# load_dotenv()

mongo_key = os.getenv("MONGOKEY")

client = MongoClient(
    f"mongodb+srv://desmond:{mongo_key}@cluster0.s3hok.mongodb.net/gifdb?retryWrites=true&w=majority"
)
db = client.gifdb
collection = db.gifs

TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix="$")


def get_unique_tags():
    mydoc = collection.find()
    all_tags = []
    for x in mydoc:
        l = list(x.values())[2].strip("][").split(", ")
        for tag in l:
            all_tags.append(tag)
    unique_tags = set(all_tags)
    return unique_tags


status_list = [
    "thala",
    "thalapathy",
    "anil",
    "aamai",
    "sasikumar",
    "samuthirakani",
    "captain kanth",
    "thalaiva",
    "prasanth",
    "mayilvaganam",
    "osthe",
    "simbu",
    "STR",
    "mahesh babu",
    "vedhanayagam",
    "yuvanshankarraja",
    "TNEB",
    "borotta suri",
    "surakarthikeyan",
]


@tasks.loop(seconds=300.0)
async def status_task():
    set_status = "with " + random.choice(status_list)
    await client.change_presence(activity=discord.Game(name=set_status))


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.wait_until_ready()
    status_task.start()


@client.event
async def on_message(message):
    if "bot" in message.content and message.channel.id != 798516544597786655:
        text = message.content.lower().replace("bot", "")
        unique_tags = get_unique_tags()
        found_tags = {x for x in unique_tags if x in text}
        # fmt: off
        search_index = ""
        for i in found_tags:
            search_index += f'"{i}"' + ' '
        print(search_index)
        result_gifs = list(collection.find({"$text": {"$search": search_index}}))
        # fmt: on
        print(result_gifs)
        selected_gif = None
        if result_gifs:
            selected_gif = random.choice(result_gifs)["gifs"]
        if selected_gif:
            await message.channel.send(selected_gif)
        else:
            illa = text.rstrip()
            await message.channel.send(f"{illa} ku lam gif illa kelambu")
    await client.process_commands(message)


@client.command()
async def checkgif(ctx, gif):
    if gif in collection.distinct("gifs"):
        tagquery = collection.find({"gifs": gif})
        for tagdict in tagquery:
            l = list(tagdict["tags"].strip("][").split(", "))
        await ctx.send(l[1:-1])
    else:
        await ctx.send("mandamayiru dhan iruku nee keta gif ila")


@client.command()
async def addgif(ctx, gif, tags):
    if gif in collection.distinct("gifs"):
        await ctx.send("Adhellam already iruku add panna mudiyadhu")
    else:
        gifdict = {"gifs": gif, "tags": tags}
        x = collection.insert_one(gifdict)
        print("Added gif {} with tags {}, UID: {}".format(gif, tags, x.inserted_id))
        await ctx.send("Add panten")


client.run(TOKEN)