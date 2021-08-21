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
            scriptFile = f'sql/{os.getenv("sql")}.sql'
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
modules = ['charhelper', 'character', 'prefix', 'admin', 'utility']

@bot.event
async def on_ready():
    for module in modules:
        bot.load_extension(f'cogs.{module}')
    activity = discord.Game(name="!gbf help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
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
        try:
            guildId = ctx.guild.id
            statement = 'SELECT silent FROM silence WHERE server_id = ?'
            cursor = db.cursor()
            cursor.execute(statement, (guildId,))
            result = cursor.fetchone()
            if result[0]==0:
                await ctx.send(f'Error: {error}')
            db.commit()
        except:
            await ctx.send(f'Error: {error}')

@bot.event
async def on_guild_join(guild):
        server = await bot.fetch_guild(831807081723199519)
        channel = bot.get_channel(836796622003765288)
        await channel.send(f'I joined a new server: {guild.name}')

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send(f'Hi, {message.author.display_name}! Please use `!gbf help` to get the list of commands <:NierLove:809541622257680444>')
        return
    await bot.process_commands(message)

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


bot.run(os.getenv('DISCORD_TOKEN'))
