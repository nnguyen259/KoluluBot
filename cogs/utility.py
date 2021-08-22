import os
import discord, sqlite3
from discord.ext import commands
from contextlib import closing

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def silent(self, ctx):
        """Turns on/off error messages.

        Error messages are turned on by default. Only server admins can use this command.
        """
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

    @commands.command()
    async def invite(self, ctx):
        """Sends a DM containing my invite link!
        """
        member= ctx.author
        channel= member.dm_channel
        if channel is None:
            channel= await member.create_dm()
        await channel.send("Invite link: https://discord.com/api/oauth2/authorize?client_id=827690753727397908&permissions=371776&scope=bot\nIf you need further help, please join the support server here!\nhttps://discord.gg/yATu8Z2A6R")
        await ctx.send("Invite link sent! Please check your DMs.")
        
def setup(client):
    client.add_cog(Utility(client))
