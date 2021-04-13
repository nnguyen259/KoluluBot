import logging
import os
from logging.handlers import TimedRotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(filename='logs/discord.log', encoding='utf-8', when='W0', interval=1)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)

load_dotenv()

bot = commands.Bot(os.getenv('prefix'))
modules = ['character']

@bot.event
async def on_ready():
    for module in modules:
        bot.load_extension(f'cogs.{module}')
    print('Bot is ready.')

@bot.command(hidden=True)
async def load(ctx, module):
    bot.load_extension(f'cogs.{module}')
    await ctx.send(f'Module {module} loaded.')

@bot.command(hidden=True)
async def unload(ctx, module):
    bot.unload_extension(f'cogs.{module}')
    await ctx.send(f'Module {module} unloaded.')

@bot.command(hidden=True)
async def reload(ctx, module):
    bot.unload_extension(f'cogs.{module}')
    bot.load_extension(f'cogs.{module}')
    await ctx.send(f'Module {module} reloaded.')

bot.run(os.getenv('DISCORD_TOKEN'))
