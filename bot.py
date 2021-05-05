import logging
import os
import sqlite3
from contextlib import closing
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

if not os.path.exists('db/kolulu.db'):
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        for file in os.listdir('sql'):
            if file.endswith('.sql'):
                with open(f'sql/{file}', 'r') as script:
                    db.cursor().executescript(script.read())
                db.commit()

if os.getenv("sql"):
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        try:
            scriptFile = f'sql/upgrades/{os.getenv("sql")}.sql'
            with open(scriptFile) as script:
                db.cursor().executescript(script.read())
            db.commit()
        except Exception:
            pass

bot = commands.Bot("!gbf ")
modules = ['character', 'prefix']

@bot.event
async def on_ready():
    for module in modules:
        bot.load_extension(f'cogs.{module}')
    print('Bot is ready.')

@bot.event
async def on_command_error(ctx, error):
    import traceback
    msg = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    logger.error(msg)
    logger.error(f'Error caused by user {ctx.author} running the command {ctx.message.content}')

    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        statement = 'INSERT INTO errors (user_id, stacktrace, command) VALUES (?, ?, ?)'
        db.cursor().execute(statement, (ctx.author.id, msg, ctx.message.content))
        db.commit()

    await ctx.send(f'Something went wrong.\nError: {error}')

@bot.command(hidden=True)
async def load(ctx, module, prefix='cogs'):
    bot.load_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} loaded.')

@bot.command(hidden=True)
async def unload(ctx, module, prefix='cogs'):
    bot.unload_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} unloaded.')

@bot.command(hidden=True)
async def reload(ctx, module, prefix='cogs'):
    bot.reload_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} reloaded.')

@bot.command()
async def feedback(ctx, *, msg):
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        statement = 'INSERT INTO feedback (user_id, feedback) VALUES (?, ?)'
        db.cursor().execute(statement, (ctx.author.id, msg))
        db.commit()

    await ctx.send(f'Feedback received!')

bot.run(os.getenv('DISCORD_TOKEN'))
