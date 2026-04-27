import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os # ضفنا المكتبة دي عشان نسحب التوكن المخفي

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_ID = 1429957936762978368

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            vc = discord.utils.get(bot.voice_clients, guild=channel.guild)
            if not vc:
                await channel.connect()
                print(f'Connected to voice channel: {channel.name}')
            else:
                print('Already connected to a voice channel.')
        except Exception as e:
            print(f'Error connecting to voice: {e}')

keep_alive()

# هنا بنسحب التوكن بشكل آمن من إعدادات Render
TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
