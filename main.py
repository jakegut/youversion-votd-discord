import requests
import discord
from discord.ext import commands
import os
import json
import re
import datetime
from pathlib import Path
from environs import Env

prefix = "!"

env = Env()
env.read_env()  # read .env file, if it exists

bot = commands.Bot(command_prefix=prefix)

yv_token = env('YOUVERSION_DEV_TOKEN')
d_token = env('DISCORD_BOT_TOKEN')

# Header to be used when calling the YouVersion API
headers = {
    "X-YouVersion-Developer-Token" : yv_token,
    "accept": "application/json",
    "Content-Type": "application/json",
    "referer": "jakerg.me",
    "user-agent": "YouVersion VOTD Discord Bot"
}

ver_headers = {
    "X-YouVersion-Developer-Token" : yv_token,
    "accept": "application/json",
    "accept-language": "en"
}

async def get_version_id(version):
    version = version.upper()
    r = requests.get("https://developers.youversionapi.com/1.0/versions", headers=headers)
    r.encoding = "utf-8" # Set encoding in case it returns None
    j = r.json()
    versions_array = []
    for data in j['data']:
        if(data['abbreviation'] == version):
            return data['id']
    return None   

async def get_verse(version='kjv'):
    """
    Get Verse of the Day using the specified version abbrevision, returns a dict of relevent information to return to user
    """
    # Make a params dict to pass to API
    version_id = await get_version_id(version)
    if version_id != None:
        params = {
            "version_id": await get_version_id(version),
        }
        day_of_year = int(datetime.datetime.now().strftime("%j"))
        r = requests.get("https://developers.youversionapi.com/1.0/verse_of_the_day/" + str(day_of_year), headers=headers, params=params)
        r.encoding = "utf-8" # Set encoding in case it returns None
        j = r.json()
        if 'verse' not in j:
            print(j)
        verse = {
            "reference": j['verse']['human_reference'],
            "content": j['verse']['text'],
            "version": version,
            "image_url": j['image']['url']
        }
        return verse
    else:
        return None

async def get_version():
    r = requests.get("https://developers.youversionapi.com/1.0/versions", headers=ver_headers)
    r.encoding = "utf-8" # Set encoding in case it returns None
    j = r.json()
    versions_array = []
    for data in j['data']:
        versions_array.append(data['abbreviation'])
    return versions_array      

@bot.event
async def on_ready():
    print("Logged in as: ", bot.user.name)

@bot.command(pass_context=True)
async def votd(ctx, ver="KJV"):
    '''
    Get a verse from YouVersion's VOTD API
    '''
    verse = await get_verse(ver)
    if verse != None:
        # Set the verse dict to variables to easily reference
        ref = verse['reference']
        text = verse['content']
        version = verse['version']
        image = verse['image_url']
        # Change image url to make a 500x500 image, and add https: to make it a valid url
        image = image.replace("{width}", "500")
        image = image.replace("{height}", "500")
        image = "https:"+image
        # Make an embed object to have a nice reply of the VOTD
        embed = discord.Embed(title="YouVersion's Verse of the Day")
        embed.add_field(name="Reference", value=ref, inline=False)
        embed.add_field(name="Verse", value=text, inline=False)
        await bot.say(embed=embed)
        await bot.say(image)
    else:
        await bot.say("Version: '" + ver + "' not found. Say !versions to get a list of usable versions")

@bot.command(pass_context=True)
async def versions():
    """
    Get a list of versions you can use on the API
    """
    versions_array = await get_version()
    r_string = "Available Versions:\n"
    i = 1
    for version in versions_array:
        r_string += str(i) + ": " + version + "\n"
        i += 1
    await bot.say(r_string)

bot.run(d_token)