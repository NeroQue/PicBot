import discord
from discord.ext import commands
import aiohttp
import random
from config import services, login

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command(name='danbooru', description='Search for an image on Danbooru')
async def danbooru(ctx, query: str):
    service_name = 'danbooru'
    base_url = services[service_name]["base_url"]
    api_key = services[service_name].get("api_key", "")

    search_url = f'{base_url}?api_key={api_key}&limit=100&tags={query}&login={login}'

    await fetch_and_send(ctx, service_name, search_url)

@bot.command(name='gelbooru', description='Search for an image on Gelbooru')
async def gelbooru(ctx, query: str):
    service_name = 'gelbooru'
    base_url = services[service_name]["base_url"]
    api_key = services[service_name].get("api_key", "")

    search_url = f'{base_url}?api_key={api_key}&tags={query}&json=0'

    await fetch_and_send(ctx, service_name, search_url)

@bot.command(name='r34', description='Search for an image on Rule34')
async def r34(ctx, query: str):
    service_name = 'r34'
    base_url = services[service_name]["base_url"]
    search_url = f'{base_url}?page=dapi&s=post&q=index&json=1&limit=1000&tags={query}'

    await fetch_and_send(ctx, service_name, search_url)

@bot.command('list', description='List all servers')
async def server_info(ctx):
    for guild in bot.guilds:
        print(guild.name) # prints all server's names


async def fetch_and_send(ctx, service_name, search_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            print(response)
            if response.status == 200:
                data = await response.json()
                if data:
                    post = data[0] if len(data) == 1 else random.choice(data)
                    image_url = post.get('file_url')
                    if image_url:
                        await ctx.send(image_url)
                    else:
                        await ctx.send('No image found.')
                else:
                    await ctx.send('No results found.')
            else:
                await ctx.send(f'Error: Unable to fetch data from {service_name}.')
