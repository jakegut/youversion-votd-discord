# youversion-votd-discord
A discord bot that pulls from [YouVersion's Verse of the Day API](https://developers.youversion.com/), written in Python.

## Setup
#### This guide asssumes you have a recent version of Python installed

First, you need to populate an `.env` file with the appropiate values. Rename `.env.example` to `.env`.

You need two tokens, one to access YouVersions VOTD API and one for your Discord bot. If you have not already, follow [this guide](https://yv-public-api-docs.netlify.app/) to get your VOTD API token (which will go right after `YOUVERSION_DEV_TOKEN=` in `.env.`). Next, you need your Discord bot token. To make a Discord bot and retrieve your token: follow [this guide](https://www.writebots.com/discord-bot-token/). The Discord token will go right afer `DISCORD_BOT_TOKEN=` in `.env`.

From the Discord bot guide, you will need to add the bot to your sever with the given URL.

Next, we need to install the necessary Python packages by running `pip install -r requirements.txt`.

Next, run `python main.py` to start the Discord bot!

## Bot Commands
| Command           | Description                                             |
|-------------------|---------------------------------------------------------|
| `!votd`           | Get the Verse of the Day image using the KVJ version    |
| `!votd <version>` |  Get the VOTD image through using the specified version |
| `!versions`       | Get the available versions the !votd command            |
---


### About the images folder...
The images returned from the api are stored in the images folder in a .png format 500x500 pixels wide, Discord embeds doesn't like images from proxies too much. Images are only downloaded if it's brand new. Hopefully this is a temporary fix.
