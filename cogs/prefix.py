import os
import discord, sqlite3
from discord.ext import commands
from contextlib import closing

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.command_prefix = self.loadPrefix
        self.defaultPrefix = os.getenv("prefix")

    def loadPrefix(self, client, message):
        try:
            guildId = message.guild.id
        except Exception:
            return self.defaultPrefix
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            try:
                statement = 'SELECT prefix FROM prefixes WHERE server_id = ?'
                cursor = db.cursor()
                cursor.execute(statement, (guildId,))
                results = cursor.fetchall()
                results = list(zip(*results))[0]
                results = sorted(results, key=len, reverse=True)
                results.insert(0, self.defaultPrefix)
            except:
                results = []
                results.insert(0, self.defaultPrefix)
            return results

    @commands.group()
    @commands.guild_only()
    async def prefix(self, ctx):
        """Manage and view prefixes

        The default prefix for KoluluBot is !gbf. This prefix will always work.

        Any additional prefix works on a per server basis (each server has its own prefix list). Multiple prefixes can be active on a server at any given time.

        When adding or removing prefix, the prefix has to be enclosed within a pair of quotation mark ("). The prefix is also allowed up to ONE trailing whitespace added to the end.
        """        
        if ctx.invoked_subcommand is None:
            await ctx.send('Prefix command not found!')

    @prefix.command()
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(administrator=True), commands.has_guild_permissions(manage_guild=True),
                        commands.has_guild_permissions(manage_channels=True), commands.has_guild_permissions(manage_roles=True),
                        commands.has_guild_permissions(manage_permissions=True))
    async def add(self, ctx, *, prefixName):
        """Add a new prefix to the server

        prefixName: The name of the prefix

        Prefix name must not contain the space character.
        """        
        if not (prefixName.startswith("\"") and prefixName.endswith("\"")):
            await ctx.send(f'Invalid prefix. Please put the prefix between quotation marks.')
            return
        prefixName=prefixName[1:-1]
        if (prefixName.startswith("<") and prefixName.endswith(">") and len(prefixName)>2):
            await ctx.send(f'Invalid prefix name `{prefixName}`.')
            return
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
        """View a list of prefixes for the server"""        
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
                results.insert(0, self.defaultPrefix)
            except:
                results = []
                results.insert(0, self.defaultPrefix)
            await ctx.send(f'List of current prefixes: `{"`, `".join(results)}`')

    @prefix.command()
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(administrator=True), commands.has_guild_permissions(manage_guild=True),
                        commands.has_guild_permissions(manage_channels=True), commands.has_guild_permissions(manage_roles=True),
                        commands.has_guild_permissions(manage_permissions=True))
    async def remove(self, ctx, *, prefixName):
        """Remove a prefix for the server

        prefixName: The prefix to be removed.
        """        
        if not (prefixName.startswith("\"") and prefixName.endswith("\"")):
            await ctx.send(f'Invalid prefix. Please put the prefix between quotation marks.')
            return
        prefixName=prefixName[1:-1]
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
