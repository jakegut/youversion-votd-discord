import requests
import discord
from discord.ext import commands
import os
import json
import re
from pathlib import Path
from environs import Env

prefix = "!"

env = Env()
env.read_env()  # read .env file, if it exists

bot = commands.Bot(command_prefix=prefix)

yv_token = env('YOUVERSION_DEV_TOKEN')
d_token = env('DISCORD_BOT_TOKEN')


headers = {
    "X-YouVersion-Developer-Token" : yv_token,
    "accept": "application/json",
    "Content-Type": "application/json",
    "referer": "jakerg.me",
    "user-agent": "YouVersion VOTD Discord Bot"
}

async def get_verse(version='kjv'):
    params = {
        "version": version
    }
    r = requests.get("https://developers.youversionapi.com/1.0/verse_of_the_day/1", headers=headers, params=params)
    r.encoding = "utf-8"
    j = r.json()
    verse = {
        "reference": j['verse']['human_reference'],
        "content": j['verse']['text'],
        "version": version,
        "image_url": j['image']['url']
    }
    return verse

async def save_image(image):
    num_array = re.findall(r'\d+', image)
    filename = '_'.join(num_array) + '.png'
    file = Path("./images/" + filename)
    if file.is_file():
        return filename

    response = requests.get(image, stream=True)
    response.raise_for_status()

    with open("./images/" + filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)
    return filename        

@bot.event
async def on

@bot.command(pass_context=True)
async def votd(ctx):
    '''
    Get a verse from YouVersion's VOTD API
    '''
    verse = await get_verse()
    ref = verse['reference']
    text = verse['content']
    version = verse['version']
    image = verse['image_url']
    image = image.replace("{width}", "500")
    image = image.replace("{height}", "500")
    image = "https:"+image
    file_path = await save_image(image)
    embed = discord.Embed(title="YouVersion's Verse of the Day")
    embed.add_field(name="Reference", value=ref, inline=False)
    embed.add_field(name="Verse", value=text, inline=False)
    await bot.say(embed=embed)
    await bot.send_file(ctx.message.channel, "./images/" + file_path)


bot.run(d_token)