import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# 1. إعداد خادم ويب بسيط لإبقاء البوت مستيقظاً على الاستضافة
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعدادات البوت والـ Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# الـ ID الخاص بالقناة الصوتية اللي بعته
VOICE_CHANNEL_ID = 1429957936762978368

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # محاولة دخول القناة الصوتية فور تشغيل البوت
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            # التحقق إذا كان البوت متصلاً بالفعل لتجنب الأخطاء
            vc = discord.utils.get(bot.voice_clients, guild=channel.guild)
            if not vc:
                await channel.connect()
                print(f'Connected to voice channel: {channel.name}')
            else:
                print('Already connected to a voice channel.')
        except Exception as e:
            print(f'Error connecting to voice: {e}')
    else:
        print("Voice channel not found. Make sure the ID is correct and the bot has permissions.")

# 3. تشغيل خادم الويب ثم تشغيل البوت
keep_alive()

# التوكن الخاص بك
TOKEN = 'MTQ5ODIzNDU4NzAxOTQ4MTEzOQ.GOet5S.XDWaXjwd2kbLX20U22TuYccI4E9FZAoy1aX81c'
bot.run(TOKEN)