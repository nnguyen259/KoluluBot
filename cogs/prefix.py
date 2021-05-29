import os
from sqlite3.dbapi2 import connect
import discord, json, sqlite3
from discord.ext import commands
from contextlib import closing

defaultPrefix = os.getenv("prefix")

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.command_prefix = self.loadPrefix

    def loadPrefix(self, client, message):
        guildId = message.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            try:
                statement = 'SELECT prefix FROM prefixes WHERE server_id = ?'
                cursor = db.cursor()
                cursor.execute(statement, (guildId,))
                results = cursor.fetchall()
                results = list(zip(*results))[0]
                results = sorted(results, key=len, reverse=True)
                results.insert(0,defaultPrefix)
            except:
                results = []
                results.insert(0,defaultPrefix)
            return results

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Prefix command not found!')

    @prefix.command()
    async def add(self, ctx, *, prefixName):
        if not (prefixName.startswith("\"") and prefixName.endswith("\"")):
            await ctx.send(f'Invalid prefix. Please put the prefix between quotation marks.')
            return
        prefixName=prefixName[1:-1]
        prefixPartNum = len(prefixName.split(' '))
        if prefixPartNum > 2 or (prefixPartNum == 2 and not prefixName.endswith(' ')):
            await ctx.send(f'Invalid prefix name `{prefixName}`.')
            return
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            try:
                statement = 'INSERT INTO prefixes VALUES (?, ?)'
                cursor = db.cursor()
                cursor.execute(statement, (guildId, prefixName))
                db.commit()
                await ctx.send(f'Prefix `{prefixName}`  added')
            except Exception:
                await ctx.send('Prefix already existed')

    @prefix.command()
    async def list(self, ctx):
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            try:
                statement = 'SELECT prefix FROM prefixes WHERE server_id = ?'
                cursor = db.cursor()
                cursor.execute(statement, (guildId,))
                results = cursor.fetchall()
                results = list(zip(*results))[0]
                results = sorted(results, key=len, reverse=True)
                results.insert(0,defaultPrefix)
            except:
                results = []
                results.insert(0,defaultPrefix)
            await ctx.send(f'List of current prefixes: `{"`, `".join(results)}`')

    @prefix.command()
    async def remove(self, ctx, *, prefixName: str):
        if not (prefixName.startswith("\"") and prefixName.endswith("\"")):
            await ctx.send(f'Invalid prefix. Please put the prefix between quotation marks.')
            return
        prefixName=prefixName[1:len(prefixName)-1]
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = 'DELETE FROM prefixes WHERE server_id = ? and prefix = ?'
            cursor = db.cursor()
            cursor.execute(statement, (guildId, prefixName))
            db.commit()
        await ctx.send(f'Prefix `{prefixName}` deleted.')

def setup(client):
    client.add_cog(Prefix(client))
