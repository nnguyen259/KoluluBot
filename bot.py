from helper.help import KoluluHelpCommand
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
defaultPrefix = os.getenv("prefix")

if not os.path.exists('db/kolulu.db'):
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        try:
            for file in os.listdir('sql'):
                if file.endswith('.sql'):
                    with open(f'sql/{file}', 'r') as script:
                        db.cursor().executescript(script.read())
                    db.commit()
        except Exception:
            pass

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

checkPrefix = 'SELECT prefix FROM prefixes WHERE server_id = 0'
connection = sqlite3.connect('db/kolulu.db')
with closing(connection) as db:
    cursor = db.cursor()
    cursor.execute(checkPrefix)
    result = cursor.fetchone()
    if not result:
        statement = 'INSERT INTO prefixes VALUES(0, ?)'
        cursor.execute(statement, (defaultPrefix,))
        db.commit()

bot = commands.Bot(command_prefix=defaultPrefix, help_command=KoluluHelpCommand())
modules = ['charhelper', 'character', 'prefix', 'admin']

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
    guildId = ctx.guild.id
    with closing(connection) as db:
        statement = 'INSERT INTO errors (user_id, stacktrace, command) VALUES (?, ?, ?)'
        db.cursor().execute(statement, (ctx.author.id, msg, ctx.message.content))
        db.commit()
        statement = 'SELECT silent FROM silence WHERE server_id = ?'
        cursor = db.cursor()
        cursor.execute(statement, (guildId,))
        result = cursor.fetchone()
        if result[0]==0:
            await ctx.send(f'Error: {error}')
        db.commit()

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, module, prefix='cogs'):
    bot.load_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} loaded.')

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, module, prefix='cogs'):
    bot.unload_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} unloaded.')

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, module, prefix='cogs'):
    bot.reload_extension(f'{prefix}.{module}')
    await ctx.send(f'Module {module} reloaded.')

@bot.command()
async def feedback(ctx, *, message):
    """Send feedback to the developer

    message: The feedback message
    """
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        statement = 'INSERT INTO feedback (user_id, feedback) VALUES (?, ?)'
        db.cursor().execute(statement, (ctx.author.id, message))
        db.commit()

    await ctx.send(f'Feedback received!')
@bot.command()
@commands.has_permissions(administrator=True)
async def silent(ctx):
    guildId = ctx.guild.id
    connection = sqlite3.connect('db/kolulu.db')
    with closing(connection) as db:
        statement = 'SELECT silent FROM silence WHERE server_id = ?'
        cursor = db.cursor()
        cursor.execute(statement, (guildId,))
        result = cursor.fetchone()
        if result is None:
            statement = 'INSERT INTO silence (server_id, silent) VALUES (?, ?)'
            db.cursor().execute(statement, (guildId, 1))
            db.commit()
            await ctx.send(f'Error message turned **off**!')
        else:
            statement = 'UPDATE silence SET silent = ? WHERE server_id =?'
            cursor = db.cursor()
            cursor.execute(statement, (1-result[0], guildId))
            db.commit()
            if (1-result[0]==1):
                await ctx.send(f'Error message turned **off**!')
            else:
                await ctx.send(f'Error message turned **on**!')




bot.run(os.getenv('DISCORD_TOKEN'))
