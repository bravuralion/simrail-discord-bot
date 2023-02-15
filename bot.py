import discord
import aiohttp
import json
import asyncio
from collections import defaultdict
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Define server sets to check
server_sets = {
    'de': ['de1', 'de2', 'de3', 'de4', 'de5'],
    'en': ['en1', 'en2', 'en3', 'en4', 'en5', 'en6', 'en7', 'en8'],
    'pl': ['pl1', 'pl2', 'pl3', 'pl4', 'pl5', 'pl8']
}

# Time interval between checks (in seconds)
update_interval = 30

# Function to get data from server API
async def get_data(server):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://panel.simrail.eu:8084/stations-open?serverCode={server}') as resp:
            text = await resp.text()
            return json.loads(text)

# Function to check which stations are open and send a message to the specified channel
async def check_stations(server_list, servers, last_updated, channel):
    messages = defaultdict(list)

    for server in server_list:
        data = await get_data(server)
        for station in data['data']:
            if not station['DispatchedBy']:
                messages[station['Name']].append(servers[server])
    # If there are no messages, return the last update time
    if not messages:
        return last_updated
    
    # Format the messages
    output = ""
    for station, servers in sorted(messages.items()):
        if len(servers) == 1:
            output += f"**{station}** is open on server {servers[0]}\n"
        else:
            server_list = ", ".join(servers[:-1]) + " and " + servers[-1]
            output += f"**{station}** is open on servers {server_list}\n"

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Stations currently open (last updated at {last_updated}):\n" + output
    message += "This bot was developed and provided by http://simrail.community"
    # Send the message to the specified channel
    try:
        async for msg in channel.history(limit=1):
            if msg.author == client.user:
                await msg.edit(content=message)
                return last_updated
        await channel.send(message)
    except discord.errors.Forbidden:
        pass
    return last_updated

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(message):
    global channel_id
    # If the message starts with !set_channel, set the channel to send messages to
    if message.content.startswith('!set_channel'):
        channel = message.channel_mentions[0]
        channel_id = channel.id
        await message.channel.send(f"Channel set to {channel.mention}")
        await message.channel.purge(limit=3)
    # If the message starts with !stations, set the servers to check
    elif message.content.startswith('!stations'):
        if not channel_id:
            await message.channel.send("Channel not set. Use !set_channel <channel_mention> first.")
            return
        server_list = message.content.split()[1:]
        if not server_list:
            return
        invalid_servers = set(server_list) - set(server_sets.keys())
        if invalid_servers:
            invalid_server_list = ", ".join(invalid_servers)
            await message.channel.send(f"Invalid server(s): {invalid_server_list}")
            return
        channel = client.get_channel(channel_id)
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await message.channel.purge(limit=3)
        while True:
            last_updated = await check_stations([server for set in server_list for server in server_sets[set]], {server: server_name for set in server_list for server, server_name in zip(server_sets[set], server_sets[set])}, last_updated, channel)
            await asyncio.sleep(update_interval)

client.run('bot_secret_in_here')
