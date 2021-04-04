import discord, json
from discord.ext import commands

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('data/characters.json', 'r') as charFile:
            self.chars = dict((k.lower(), v) for k, v in json.load(charFile).items())

    @commands.Cog.listener()
    async def on_ready(self):
        print('Character module is ready.')

    @commands.command()
    async def char(self, ctx, name : str, version=None):
        name = name.lower()
        if name in self.chars:
            outChar = None
            if not version:
                outChar = self.chars[name]['versions'][0]
                version = self.chars[name]['versions'][0]['name']
            else:
                for alt in self.chars[name]['versions']:
                    if alt['name'].lower() == version.lower():
                        outChar = alt
                        break
            if not outChar:
                outChar = self.chars[name]['versions'][0]
                version = self.chars[name]['versions'][0]['name']

            embed = discord.Embed()
            embed.title = name + ' (' + version + ')'
            embed.description = '**HP:** ' + str(outChar['hp']) + '\t**ATK:** ' + str(outChar['atk']) + '\n**Race:** ' + outChar['race'] + '\t**Style:** ' + outChar['style']
            embed.set_thumbnail(url=outChar['thumbnail'])
            await ctx.send(embed=embed)
        else:
            await ctx.send('Character not found!')

def setup(client):
    client.add_cog(Character(client))