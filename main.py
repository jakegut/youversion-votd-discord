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

async def get_verse(version='kjv'):
    """
    Get Verse of the Day using the specified version abbrevision, returns a dict of relevent information to return to user
    """
    # Make a params dict to pass to API
    params = {
        "version": version,
    }
    day_of_year = int(datetime.datetime.now().strftime("%j"))
    r = requests.get("https://developers.youversionapi.com/1.0/verse_of_the_day/" + str(day_of_year), headers=headers, params=params)
    r.encoding = "utf-8" # Set encoding in case it returns None
    j = r.json()
    verse = {
        "reference": j['verse']['human_reference'],
        "content": j['verse']['text'],
        "version": version,
        "image_url": j['image']['url']
    }
    return verse

async def save_image(image):
    """
    Will save the VOTD image if it's not already in the /images folder
    """
    # Generate a filename
    num_array = re.findall(r'\d+', image)
    filename = '_'.join(num_array) + '.png'
    
    # Make a Path obeject to see if it exits
    file = Path("./images/" + filename)
    if file.is_file():
        return filename # No need to save since it's already there

    # Get the image in a way to save it
    response = requests.get(image, stream=True)
    response.raise_for_status() # Will return if it's not in the 200 range

    # Write image
    with open("./images/" + filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)
    return filename        

@bot.event
async def on_ready():
    print("Logged in as: ", bot.user.name)

@bot.command(pass_context=True)
async def votd(ctx):
    '''
    Get a verse from YouVersion's VOTD API
    '''
    verse = await get_verse()
    # Set the verse dict to variables to easily reference
    ref = verse['reference']
    text = verse['content']
    version = verse['version']
    image = verse['image_url']
    # Change image url to make a 500x500 image, and add https: to make it a valid url
    image = image.replace("{width}", "500")
    image = image.replace("{height}", "500")
    image = "https:"+image
    file_path = await save_image(image)
    # Make an embed object to have a nice reply of the VOTD
    embed = discord.Embed(title="YouVersion's Verse of the Day")
    embed.add_field(name="Reference", value=ref, inline=False)
    embed.add_field(name="Verse", value=text, inline=False)
    await bot.say(embed=embed)
    await bot.send_file(ctx.message.channel, "./images/" + file_path)


bot.run(d_token)