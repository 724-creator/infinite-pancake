import discord
from discord.ext import commands

# Basic setup with necessary permissions
intents = discord.Intents.default()
intents.message_content = True  # Allows bot to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run('YOUR_BOT_TOKEN')
