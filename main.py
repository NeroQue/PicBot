import discord
import aiohttp
import random  # Import the random module
from config import DANBOORU_API_KEY, BOT_TOKEN


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.content.startswith('!danbooru'):
        args = message.content[len('!danbooru '):].strip().split()

        if not args:
            await message.channel.send('Please provide a name.')
            return

        name = args[0]
        series = args[1] if len(args) > 1 else name  # Default to name if series is not provided

        # Conditionally construct the search URL based on whether a series is provided
        if series == name:
            search_url = f'https://danbooru.donmai.us/posts.json?api_key={DANBOORU_API_KEY}&limit=100&tags={name}&login={login}]'
        else:
            search_url = f'https://danbooru.donmai.us/posts.json?api_key={DANBOORU_API_KEY}&limit=100&tags={name}_({series})&login={login}'

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        if len(data) == 1:
                            post = data[0]
                        else:
                            # Randomly select a result from the search
                            post = random.choice(data)

                        image_url = post['file_url']
                        await message.channel.send(image_url)
                    else:
                        await message.channel.send('No results found.')
                else:
                    await message.channel.send('Error: Unable to fetch data from Danbooru.')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(BOT_TOKEN)
