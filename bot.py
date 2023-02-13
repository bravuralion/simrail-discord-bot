import discord
import aiohttp
import json
import asyncio
from collections import defaultdict
from datetime import datetime
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SERVERS = ['de1', 'de2', 'de3', 'de4', 'de5']  # Enter your desired Servers here
CHANNEL_ID = 1074655931910074448 # Enter the Channel ID where the Bot should Post the Messages
LAST_UPDATED = None

async def get_data(server):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://panel.simrail.eu:8084/stations-open?serverCode={server}') as resp:
            text = await resp.text()
            return json.loads(text)

async def check_stations():
    global LAST_UPDATED
    channel = client.get_channel(CHANNEL_ID)
    messages = defaultdict(list)

    for server in SERVERS:
        data = await get_data(server)
        for station in data['data']:
            if not station['DispatchedBy']:
                messages[station['Name']].append(server)

    output = ""
    for station, servers in sorted(messages.items()):
        if len(servers) == 1:
            output += f"**{station}** is open on server {servers[0]}\n"
        else:
            server_list = ", ".join(servers[:-1]) + " and " + servers[-1]
            output += f"**{station}** is open on servers {server_list}\n"

    if output:
        if LAST_UPDATED is None:
            message = "Stations currently open:\n" + output
        else:
            message = f"Stations currently open (updated at {LAST_UPDATED}):\n" + output
        if channel.last_message:
            await channel.last_message.edit(content=message)
        else:
            await channel.send(message)
    else:
        await channel.send("No stations currently open.")

    LAST_UPDATED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@client.event
async def on_ready():

    print('Bot is ready')
    channel = client.get_channel(CHANNEL_ID)
    await channel.purge(limit=100)
    await check_stations()
    while True:
        await check_stations()
        await asyncio.sleep(60)

client.run('123456') # Enter the Token from your Bot
