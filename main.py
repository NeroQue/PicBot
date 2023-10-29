import discord
import aiohttp
import random
from config import BOT_TOKEN, login, services

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.content.startswith('!danbooru') or message.content.startswith('!gelbooru') or message.content.startswith('!r34'):
        command, *args = message.content.split()  # Split the message into command and arguments

        if not args:
            await message.channel.send('Please provide a search query. Usage: !service <query>')
            return

        service_name = command[1:]  # Extract the service name (e.g., danbooru, gelbooru, r34)
        search_query = " ".join(args)  # Combine the remaining arguments as the search query

        # Check if the service name is valid
        if service_name in services:
            # Extract the service-specific base URL
            service_config = services[service_name]
            base_url = service_config["base_url"]

            # Customize the search URL based on the selected service and user input
            if service_name == "r34":
                search_url = f'{base_url}?page=dapi&s=post&q=index&json=1&limit=1000&tags={search_query}'
            else:
                # For other services, you can add logic to include an API key if required.
                api_key = service_config.get("api_key", "")
                search_url = f'{base_url}?api_key={api_key}&limit=100&tags={search_query}&login={login}'

            async with aiohttp.ClientSession() as session:
                async with session.get(search_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            if len(data) == 1:
                                post = data[0]
                            else:
                                post = random.choice(data)

                            image_url = post['file_url']
                            await message.channel.send(image_url)
                        else:
                            await message.channel.send('No results found.')
                    else:
                        await message.channel.send(f'Error: Unable to fetch data from {service_name}.')
        else:
            await message.channel.send('Invalid service. Supported services: danbooru, gelbooru, r34')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(BOT_TOKEN)
