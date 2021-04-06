import discord, os
from discord.ext import commands

bot = commands.Bot('?gbf ')
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

@bot.command()
async def unload(ctx, module):
    bot.unload_extension(f'cogs.{module}')
    await ctx.send(f'Module {module} unloaded.')

@bot.command()
async def reload(ctx, module):
    bot.unload_extension(f'cogs.{module}')
    bot.load_extension(f'cogs.{module}')
    await ctx.send(f'Module {module} reloaded.')

bot.run(os.getenv('DISCORD_TOKEN'))