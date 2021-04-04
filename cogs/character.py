import discord, json
from discord.ext import commands

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('data/characters.json', 'r') as charFile:
            self.chars = dict((k.lower(), v) for k, v in json.load(charFile).items())
        with open('data/emoji.json', 'r') as emojiFile:
            self.emojis = json.load(emojiFile)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Character module is ready.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'Something went wrong.\nError: {error}')

    @commands.command()
    async def char(self, ctx, name : str, version=None):
        name = name.lower()
        if name in self.chars:
            char = self.chars[name]
            charVersion = None
            if not version:
                charVersion = self.chars[name]['versions'][0]
            else:
                for alt in self.chars[name]['versions']:
                    if alt['name'].lower() == version.lower():
                        charVersion = alt
                        break
            if not charVersion:
                charVersion = self.chars[name]['versions'][0]
                        
            version = charVersion['name']
            name = name.title()

            msg = f'{self.emojis["Rarity"][charVersion["rarity"]]} **{name} ({version})**'

            title = f'{self.emojis["Element"][charVersion["element"]]} **{charVersion["element"]}** {self.emojis["Type"][charVersion["type"]]} **{charVersion["type"]}**\n'
            for specialty in charVersion['specialties']:
                title += f'{self.emojis["Specialty"][specialty]} **{specialty}** '

            description = f'{self.emojis["Gender"][char["gender"]]} **{char["gender"]}** {self.emojis["Race"][charVersion["race"]]} **{charVersion["race"]}**'
            description += f'\n{self.emojis["Stat"]["Hp"]} *{charVersion["hp"]}* \n{self.emojis["Stat"]["Atk"]} *{charVersion["atk"]}*'

            embed = discord.Embed()
            embed.title = title
            embed.description = description
            embed.set_thumbnail(url=charVersion['thumbnail'])
            await ctx.send(msg, embed=embed)
        else:
            await ctx.send('Character not found!')

def setup(client):
    client.add_cog(Character(client))