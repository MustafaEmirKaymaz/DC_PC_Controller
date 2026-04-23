{\rtf1\ansi\ansicpg1254\cocoartf2869
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import discord\
from discord.ext import commands, tasks\
import psutil\
import platform\
import time\
\
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())\
\
status_message = None  # Tek mesaj\uc0\u305  s\'fcrekli g\'fcncellemek i\'e7in\
\
# Bot haz\uc0\u305 r\
@bot.event\
async def on_ready():\
    print(f"Bot aktif: \{bot.user\}")\
    update_status.start()  # otomatik g\'fcncelleme ba\uc0\u351 lat\
\
# Sistem verilerini \'e7eken fonksiyon (TEK YERDEN Y\'d6NET\uc0\u304 M)\
def get_system_info():\
    cpu = psutil.cpu_percent(interval=1)\
\
    ram = psutil.virtual_memory()\
    disk = psutil.disk_usage('/')\
\
    net = psutil.net_io_counters()\
\
    sistem = platform.system() + " " + platform.release()\
\
    uptime = int((time.time() - psutil.boot_time()) // 60)\
\
    return \{\
        "cpu": cpu,\
        "ram": ram.percent,\
        "disk": disk.percent,\
        "upload": round(net.bytes_sent / (1024*1024), 2),\
        "download": round(net.bytes_recv / (1024*1024), 2),\
        "sistem": sistem,\
        "uptime": uptime\
    \}\
\
# Manuel komut\
@bot.command()\
async def durum(ctx):\
    data = get_system_info()\
\
    mesaj = f"""\
\uc0\u55357 \u56741 \u65039  **CANLI S\u304 STEM DURUMU**\
\
\uc0\u55357 \u56613  CPU: %\{data['cpu']\}\
\uc0\u55357 \u56510  RAM: %\{data['ram']\}\
\uc0\u55357 \u56512  Disk: %\{data['disk']\}\
\
\uc0\u55357 \u56545  Upload: \{data['upload']\} MB\
\uc0\u55357 \u56549  Download: \{data['download']\} MB\
\
\uc0\u55358 \u56800  Sistem: \{data['sistem']\}\
\uc0\u9201 \u65039  Uptime: \{data['uptime']\} dakika\
\
\uc0\u55356 \u57299  Ping: \{round(bot.latency * 1000)\} ms\
    """\
\
    await ctx.send(mesaj)\
\
# CANLI TAK\uc0\u304 P (MESAJ ED\u304 T)\
@bot.command()\
async def takip(ctx):\
    global status_message\
    status_message = await ctx.send("\uc0\u55357 \u56545  Sistem izleme ba\u351 lat\u305 l\u305 yor...")\
\
# OTOMAT\uc0\u304 K G\'dcNCELLEME (HER 5 SN)\
@tasks.loop(seconds=5)\
async def update_status():\
    global status_message\
\
    if status_message is None:\
        return\
\
    data = get_system_info()\
\
    # UYARI S\uc0\u304 STEM\u304 \
    warning = ""\
    if data['cpu'] > 80:\
        warning += "\uc0\u9888 \u65039  CPU \'e7ok y\'fcksek!\\n"\
    if data['ram'] > 80:\
        warning += "\uc0\u9888 \u65039  RAM \'e7ok y\'fcksek!\\n"\
\
    mesaj = f"""\
\uc0\u55357 \u56741 \u65039  **CANLI TAK\u304 P**\
\
\uc0\u55357 \u56613  CPU: %\{data['cpu']\}\
\uc0\u55357 \u56510  RAM: %\{data['ram']\}\
\uc0\u55357 \u56512  Disk: %\{data['disk']\}\
\
\uc0\u55357 \u56545  Upload: \{data['upload']\} MB\
\uc0\u55357 \u56549  Download: \{data['download']\} MB\
\
\uc0\u9201 \u65039  Uptime: \{data['uptime']\} dk\
\uc0\u55356 \u57299  Ping: \{round(bot.latency * 1000)\} ms\
\
\{warning\}\
    """\
\
    try:\
        await status_message.edit(content=mesaj)\
    except:\
        status_message = None\
\
# Takibi durdur\
@bot.command()\
async def durdur(ctx):\
    global status_message\
    status_message = None\
    await ctx.send("\uc0\u10060  Takip durduruldu.")\
\
# TOKEN\
bot.run("TOKEN\uc0\u304 N\u304 _YAZ")}