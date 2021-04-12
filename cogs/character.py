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
        with open('data/emp.json', 'r') as empFile:
            self.emps = dict((k.lower(), v) for k, v in json.load(empFile).items())
        with open('data/empdata.json', 'r') as empDataFile:
            self.empData = json.load(empDataFile)

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

            charSupport = self.supportSkills[name.lower()][version]
            charOugi = self.ougis[name.lower()][version]
            name = name.title()
            version = version.title()
            embedList = []
            #Main embed
            title = f'{self.emojis["Rarity"][charVersion["rarity"]]}'
            for series in charVersion['series']:
                title += f'{self.emojis["Series"][series]}'
            if (version != 'Base'):
                title +=f'**{charVersion["name"]} ({version})**'
            else:
                title +=f'**{charVersion["name"]}**'
            description = f'**JP**: {charVersion["jpname"]}\n'
            description += f'**VA**: {", ".join(charVersion["va"])}'

            information = f'\n{self.emojis["Element"][charVersion["element"]]} **{charVersion["element"]}** {self.emojis["Type"][charVersion["type"]]} **{charVersion["type"]}**\n'
            for specialty in charVersion['specialties']:
                information += f'{self.emojis["Specialty"][specialty]} **{specialty}**  '
            information += '\n'
            for gender in charVersion['gender']:
                information += f'{self.emojis["Gender"][gender]} **{gender}**  '
            information += '\n'
            for race in charVersion['race']:
                information += f'{self.emojis["Race"][race]} **{race}**  '
            information += f'\n{self.emojis["Stat"]["Hp"]} *{charVersion["hp"]}* {self.emojis["Stat"]["Atk"]} *{charVersion["atk"]}*'

            profile = f'{charVersion["profile"]}'

            mainEmbed = discord.Embed()
            mainEmbed.title = title
            mainEmbed.description = description
            mainEmbed.add_field(name='Basic Info.', value=information, inline=False)
            mainEmbed.add_field(name='Profile', value=profile, inline=False)
            mainEmbed.set_thumbnail(url=charVersion['thumbnail'])
            mainEmbed.set_image(url=charVersion['image'])
            embedList.append(mainEmbed)

            #Ougi embed
            ougiEmbed = discord.Embed()
            for ougiList in charOugi:
                for ougiText in ougiList["text"]:
                    ougiEmbed.add_field(name=f'**{ougiList["name"]}**:', value=f'{ougiText} \n', inline=False)
            ougiEmbed.title="Charge Attack"
            ougiEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/828230361321963530/830390392565923900/download.png')
            ougiEmbed.set_image(url=charVersion['image'])
            embedList.append(ougiEmbed)

            #Support skill embed
            for supportList in charSupport:
                supportEmbed = discord.Embed()
                supportEmbed.title =f'{supportList["name"]}:'
                for supportText in supportList["text"]:
                    supportEmbed.description= f'{supportText}'
                    supportEmbed.set_thumbnail(url=f'{supportList["thumbnail"]}')
                    supportEmbed.set_image(url=charVersion['image'])
                    embedList.append(supportEmbed)

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")

            await paginator.run(embedList)
        else:
            await ctx.send('Character not found!')

    @commands.command()
    async def emp(self, ctx, name : str, version=None):
        from PIL import Image
        import urllib.request, os

        name = name.lower()
        if version:
            version = version.upper()
        if name in self.emps:
            char = self.emps[name]
            charVersion = None
            if not version or version not in char:
                version = 'BASE'
                charVersion = char['BASE']
            else:
                charVersion = char[version]
            try:
                file = discord.File(f'cache/emp/char/{name}/{version}.png', filename='emp.png')
            except Exception:
                image = Image.new("RGBA", (104*5, 104*len(charVersion)))
                i = 0
                for row in charVersion:
                    j = 0
                    rowImage = Image.new("RGBA", (104*5, 104))
                    for emp in row:
                        id = self.empData[emp]
                        try:
                            cellImage = Image.open(f'cache/emp/image/normal/{id}.png')
                            rowImage.paste(cellImage, (104*j, 0))
                        except Exception:
                            os.makedirs('cache/emp/image/normal', exist_ok=True)
                            url = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/zenith/assets/ability/{id}.png'
                            cellImage = Image.open(urllib.request.urlopen(url))
                            cellImage.save(f'cache/emp/image/normal/{id}.png')
                            rowImage.paste(cellImage, (104*j, 0))
                        j += 1
                    image.paste(rowImage, (0, 104*i))
                    i += 1

                os.makedirs(f'cache/emp/char/{name}', exist_ok=True)
                image.save(f'cache/emp/char/{name}/{version}.png', format="PNG")
                file = discord.File(f'cache/emp/char/{name}/{version}.png', filename="emp.png")

            embed = discord.Embed()
            embed.title = '__Extended Mastery Perks__'
            embed.set_thumbnail(url=self.chars[name][version]['thumbnail'])
            embed.set_image(url="attachment://emp.png")

            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send('Character Not Found!')

    @commands.command(hidden=True)
    async def refresh(self, ctx):
        import shutil
        shutil.rmtree('cache/emp/char', ignore_errors=True)
        await ctx.send('Removed charcter emp caches.')

    @char.error
    @emp.error
    @refresh.error
    async def error(self, ctx, error):
        print(traceback.format_exc())
        await ctx.send(f'Something went wrong.\nError: {error}')

def setup(client):
    client.add_cog(Character(client))
