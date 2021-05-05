from sqlite3.dbapi2 import connect
import discord, json, sqlite3
from discord.ext import commands
from contextlib import closing

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.command_prefix = self.loadPrefix

    def loadPrefix(self, client, message):
        guildId = message.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = 'SELECT prefix FROM prefixes WHERE server_id = 0 OR server_id = ?'
            cursor = db.cursor()
            cursor.execute(statement, (guildId,))
            results = cursor.fetchall()
            results = list(zip(*results))[0]
            return results

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Prefix command not found!')

    @prefix.command()
    async def add(self, ctx, prefixName):
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            try:
                statement = 'INSERT INTO prefixes VALUES (?, ?)'
                cursor = db.cursor()
                cursor.execute(statement, (guildId, prefixName))
                db.commit()
                await ctx.send(f'Prefix **{prefixName}** added')
            except Exception:
                await ctx.send('Prefix already existed')

    @prefix.command()
    async def list(self, ctx):
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = 'SELECT prefix FROM prefixes WHERE server_id = 0 or server_id = ?'
            cursor = db.cursor()
            cursor.execute(statement, (guildId,))
            results = cursor.fetchall()
            results = list(zip(*results))[0]
            await ctx.send(f'List of current prefixes: {", ".join(results)}')

    @prefix.command()
    async def remove(self, ctx, prefixName):
        guildId = ctx.guild.id
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = 'DELETE FROM prefixes WHERE server_id = ? and prefix = ?'
            cursor = db.cursor()
            cursor.execute(statement, (guildId, prefixName))
            db.commit()
        await ctx.send(f'Prefix **{prefixName}** deleted.')

def setup(client):
    client.add_cog(Prefix(client))