import io
import discord, DiscordUtils, sqlite3
from discord.ext import commands, tasks
from contextlib import closing

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.report.start()

    def cog_unload(self):
        self.report.cancel()

    @commands.group(hidden=True)
    @commands.is_owner()
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Admin command not found!')

    @admin.command()
    async def guildlist(self, ctx):
        guildEmbedList = []
        emojiList = ['🔟', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        i = 0
        guildEmbed = discord.Embed()

        for guild in self.client.guilds:
            if not guild.name.startswith('Kolulu'):
                i+=1
                guildEmbed.add_field(name=f'{emojiList[i%10]} {guild.name}', value='\u200b', inline=False)
                if i%10 == 0:
                    guildEmbedList.append(guildEmbed)
                    guildEmbed = discord.Embed()

        if i%10 != 0:
            guildEmbedList.append(guildEmbed)

        for embed in guildEmbedList:
            embed.title=f'Kolulu server list: {len(self.client.guilds)} total servers'
            index = guildEmbedList.index(embed)
            footerText = f'({index+1}/{len(guildEmbedList)})'
            embed.set_footer(text=footerText)

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=False)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(guildEmbedList)

    @admin.command()
    async def log(self, ctx, recent=0):
        import os
        if recent == 0:
            file = discord.File('logs/discord.log')
            await ctx.send("Most recent log file",file=file)
        else:
            files = [f.name for f in os.scandir('logs') if f.is_file()]
            try:
                file = discord.File(f'logs/{files[-recent]}')
            except Exception:
                recent = 0
                file = discord.File(f'logs/{files[0]}')
            await ctx.send(f'The no.{recent+1} recent log', file=file)

    @admin.command()
    async def feedback(self, ctx, days=0):
        output = 'name, feedback\n'
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = f"SELECT user_id, feedback FROM feedback WHERE created_at > DATE('now', '-{days} days') ORDER BY created_at DESC"
            cursor = db.cursor()
            cursor.execute(statement)
            results = cursor.fetchall()
            for result in results:
                user = await self.client.fetch_user(result[0])
                output += f'{user.name}, {result[1]}\n'
            outputFile = discord.File(io.BytesIO(output.encode('utf-8')), filename='feedback.csv')

            await ctx.send(file=outputFile)

    @admin.command()
    async def errors(self, ctx, days=0):
        output = 'id, name, command\n'
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = f"SELECT id, user_id, command FROM errors WHERE created_at > DATE('now', '-{days} days') ORDER BY created_at DESC"
            cursor = db.cursor()
            cursor.execute(statement)
            results = cursor.fetchall()
            for result in results:
                user = await self.client.fetch_user(result[1])
                output += f'{result[0]}, {user.name}, {result[2]}\n'
            outputFile = discord.File(io.BytesIO(output.encode('utf-8')), filename='errors.csv')

            await ctx.send(file=outputFile)

    @admin.command()
    async def error(self, ctx, id):
        if not id:
            await ctx.send('No id specified.')
            return
        output = f'ERROR ID={id}\n'
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            statement = f"SELECT user_id, command, stacktrace FROM errors WHERE id=?"
            cursor = db.cursor()
            cursor.execute(statement, (id,))
            result = cursor.fetchone()
            user = await self.client.fetch_user(result[0])
            output += f'USER={user.name}\n'
            output += f'COMMAND={result[1]}\n'
            output += f'STACKTRACE=\n{result[2]}'
            outputFile = discord.File(io.BytesIO(output.encode('utf-8')), filename=f'error{id}.txt')

            await ctx.send(file=outputFile)

    @tasks.loop(hours=168)
    async def report(self):
        import datetime
        guild = await self.client.fetch_guild(831807081723199519)
        role = guild.get_role(831808673092599850)
        channel = self.client.get_channel(836796622003765288)
        await channel.send(f'{role.mention}\nWeekly Report for {datetime.date.today()}')
        await self.errors(channel, days=7)
        await self.feedback(channel, days=7)

    @report.before_loop
    async def before_report(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Admin(client))
