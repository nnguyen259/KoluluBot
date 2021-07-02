import os
import discord, DiscordUtils
from discord.ext import commands
from urllib.request import urlopen
from cogs.summonhelper import SummonHelper

class Summon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dataPath = os.getenv("data")
        self.icon_url = 'https://cdn.discordapp.com/attachments/828230402875457546/839701583515222026/321247751830634496.png'
        self.helper : SummonHelper = client.get_cog('SummonHelper')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.reload()

    @commands.group(aliases=['s'])
    @commands.guild_only()
    async def summon(self, ctx):
        if ctx.invoked_subcommand is None:
            args = ctx.message.content.split(' ')[1:]
            name = args[0]
            if name in ['s', 'summon']:
                name = args[1]
            await self.info(ctx, name=name)
    
    @summon.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        """Reload the data for the bot

        Data is stored at https://github.com/nnguyen259/KoluluData
        """        
        self.helper.loadData()
        await ctx.send('Data reloaded')

    @summon.command()
    async def info(self, ctx, *, name):
        embedList = self.helper.get(self.getSummonName(name))
        for embed in embedList:
            index = embedList.index(embed)
            footerText = f'({index+1}/{len(embedList)})\nData obtained from GBF Wiki'
            embed.set_footer(text=footerText, icon_url=self.icon_url)

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=False)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    def getSummonName(self, name : str):
        name = name.lower()
        if name in self.helper.summons:
            return name
        
        from fuzzywuzzy import process, fuzz
        names = process.extractBests(name, self.helper.summons.keys(), scorer=fuzz.partial_ratio, limit=20)
        names = [name for name, score in names if score == names[0][1]]
        tempNames = [n for n in names if n[0] == name[0]]
        if len(tempNames):
            names = tempNames
        print(names[0])
        return names[0]        

def setup(client):
    client.add_cog(Summon(client))