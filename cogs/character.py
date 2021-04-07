import discord, json, DiscordUtils, traceback
from discord.ext import commands

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('data/characters.json', 'r') as charFile:
            self.chars = dict((k.lower(), v) for k, v in json.load(charFile).items())
        with open('data/emoji.json', 'r') as emojiFile:
            self.emojis = json.load(emojiFile)
        with open('data/ougi.json', 'r') as ougiFile:
            self.ougis = dict((k.lower(), v) for k, v in json.load(ougiFile).items())
        with open('data/skill.json', 'r') as skillFile:
            self.skills = dict((k.lower(), v) for k, v in json.load(skillFile).items())
        with open('data/supportskill.json', 'r') as supportSkillFile:
            self.supportSkills = dict((k.lower(), v) for k, v in json.load(supportSkillFile).items())

    @commands.Cog.listener()
    async def on_ready(self):
        print('Character module is ready.')

    @commands.command()
    async def char(self, ctx, name : str, version=None):
        name = name.lower()
        if version:
            version = version.upper()
        if name in self.chars:
            char = self.chars[name]
            charVersion = None
            if not version or version not in char:
                version = 'BASE'
                charVersion = char['BASE']
            else:
                charVersion = char[version]
            
            name = name.title()
            version = version.title()

            title = f'{self.emojis["Rarity"][charVersion["rarity"]]} **{name} ({version})**'

            title += f'\n{self.emojis["Element"][charVersion["element"]]} **{charVersion["element"]}** {self.emojis["Type"][charVersion["type"]]} **{charVersion["type"]}**\n'
            for specialty in charVersion['specialties']:
                title += f'{self.emojis["Specialty"][specialty]} **{specialty}** '

            description = f'{self.emojis["Gender"][charVersion["gender"]]} **{charVersion["gender"]}** {self.emojis["Race"][charVersion["race"]]} **{charVersion["race"]}**'
            description += f'\n{self.emojis["Stat"]["Hp"]} *{charVersion["hp"]}* \n{self.emojis["Stat"]["Atk"]} *{charVersion["atk"]}*'

            profile = f'{charVersion["profile"]}'
            misc = f'JP Name: {charVersion["jpname"]} \nVA: {charVersion["va"]}'

            embedList = []

            mainEmbed = discord.Embed()
            mainEmbed.title = title
            mainEmbed.description = description
            mainEmbed.add_field(name='Profile', value=profile, inline=False)
            mainEmbed.add_field(name='Misc.', value=misc, inline=False)
            mainEmbed.set_thumbnail(url=charVersion['thumbnail'])
            mainEmbed.set_image(url=charVersion['image'])
            embedList.append(mainEmbed)


            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")

            await paginator.run(embedList)
        else:
            await ctx.send('Character not found!')
    
    @char.error
    async def char_error(self, ctx, error):
        print(traceback.format_exc())
        await ctx.send(f'Something went wrong.\nError: {error}')

def setup(client):
    client.add_cog(Character(client))