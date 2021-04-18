import discord, json, DiscordUtils
from discord.ext import commands
from discord.ext.commands.context import Context

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loadData()

    def loadData(self):
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
        with open('data/empdomaindata.json', 'r') as empDomainDataFile:
            self.empDomainData = json.load(empDomainDataFile)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.reload()
        print('Character module is ready.')

    @commands.group(aliases=['c', 'character'])
    async def char(self, ctx : Context):
        if ctx.invoked_subcommand is None:
            args = ctx.message.content.split(' ')[1:]
            name = args[0]
            version = args[1] if len(args) > 1 else None
            uncap = args[2] if len(args) > 2 else None
            await self.info(ctx, name, version, uncap)

    @char.command()
    async def reload(self, ctx):
        self.loadData()
        await ctx.send('Data reloaded')

    @char.command()
    async def info(self, ctx, name : str, version=None, uncap='6'):
        name, version, uncap = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        charVersion = self.chars[name][version]

        name = name.title()
        version = version.title()
        
        embedList = []

        #Main embed
        title = f'{self.emojis["Rarity"][charVersion["rarity"]]} '
        for series in charVersion['series']:
            title += f'{self.emojis["Series"][series]} '
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

        embedList.append(await self.ougi(ctx, name, version, uncap, noShow=True))
        embedList.extend(await self.support(ctx, name, version, uncap, noShow=True))

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    @char.command()
    async def ougi(self, ctx, name :str, version=None, uncap='6', noShow=False):
        name, version, uncap = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        charVersion = self.ougis[name][version]

        ougiEmbed = discord.Embed()
        for ougiList in charVersion:
            for ougiText in ougiList["text"]:
                ougiEmbed.add_field(name=f'**{ougiList["name"]}**:', value=f'{ougiText} \n', inline=False)
                if ougiList["duration"]:
                    duration = ''
                    for ougiDuration in ougiList["duration"]:
                        for ougiDurationText in ougiList["duration"][ougiDuration]:
                                duration+= f'{ougiDurationText} and '
                        duration = duration[:-4]
                        if ougiDuration != "Indefinite":
                            duration += f': {ougiDuration} turns.\n'
                        else:
                            duration += f': {ougiDuration}.\n'
                    ougiEmbed.add_field(name='\u200b', value=f'{duration}\n', inline=False)

        ougiEmbed.title="Charge Attack"
        ougiEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/828230361321963530/830390392565923900/download.png')
        ougiEmbed.set_image(url=self.chars[name][version]['image'])

        if noShow:
            return ougiEmbed
        else:
            await ctx.send(embed=ougiEmbed)

    @char.command()
    async def support(self, ctx, name :str, version=None, uncap='6', noShow=False):
        name, version, uncap = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        charVersion = self.supportSkills[name][version]

        embedList = []
        for supportList in charVersion:
            supportEmbed = discord.Embed()
            supportEmbed.title =f'{supportList["name"]}:'
            for supportText in supportList["text"]:
                supportEmbed.description= f'{supportText}'
                supportEmbed.set_thumbnail(url=f'{supportList["thumbnail"]}')
                supportEmbed.set_image(url=self.chars[name][version]['image'])
                embedList.append(supportEmbed)

        if noShow:
            return embedList
        else:
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")

            await paginator.run(embedList)

    @char.command()
    async def emp(self, ctx, name : str, version=None, uncap='6'):
        from PIL import Image, ImageDraw, ImageFont
        import urllib.request, os

        name, version, uncap = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        charVersion = self.emps[name][version]

        try:
            file = discord.File(f'cache/emp/char/{name}/{version}.png', filename='emp.png')
        except Exception:
            image = Image.new("RGBA", (104*5, 104*len(charVersion)))
            i = 0
            for row in charVersion:
                j = 0
                rowImage = Image.new("RGBA", (104*5, 104))
                for emp in row:
                    try:
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
                    except:
                        id = self.empDomainData[emp]
                        if id == 0:
                            try:
                                cellImage = Image.open(f'cache/emp/image/domain/0.png')
                                rowImage.paste(cellImage, (104*j, 0))
                            except Exception:
                                os.makedirs('cache/emp/image/domain', exist_ok=True)
                                cellImage= Image.new("RGBA", (520, 104))
                                domainText = ImageDraw.Draw(cellImage)
                                font = ImageFont.truetype("data/Ubuntu-medium.ttf", 50)
                                domainText.text((258,52), "Domain of the Evoker", anchor= "mm", font=font)
                                cellImage.save(f'cache/emp/image/domain/{id}.png')
                                rowImage.paste(cellImage, (104*j, 0))

                        else:
                            try:
                                cellImage = Image.open(f'cache/emp/image/domain/{id}.png')
                                rowImage.paste(cellImage, (104*j, 0))
                            except Exception:
                                os.makedirs('cache/emp/image/normal', exist_ok=True)
                                url = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/domain_evoker/assets/domain_icon/{id}/i_released.png'
                                cellImage = Image.open(urllib.request.urlopen(url))
                                cellImage= cellImage.crop((10, 10, 114, 114))
                                cellImage.save(f'cache/emp/image/domain/{id}.png')
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

    @char.command(hidden=True)
    async def refresh(self, ctx):
        import shutil
        shutil.rmtree('cache/emp/char', ignore_errors=True)
        await ctx.send('Removed charcter emp caches.')

    @char.group()
    async def alias(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Alias command not found!')

    @alias.command()
    async def add(self, ctx, alias, name, version=None):
        import sqlite3
        from contextlib import closing

        if version:
            version = version.upper()
        name, versionTemp, uncap = self.getCharVersion(ctx, name, version)
        if not name:
            await ctx.send('Character not found!')
            return
        alias = alias.lower()
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            cursor = db.cursor()
            char = self.chars[name]
            if versionTemp == 'BASE' and not version:
                try:
                    statement = 'INSERT INTO alt_names VALUES(?, ?, ?)'
                    cursor.execute(statement, (ctx.guild.id, alias, name))
                    db.commit()
                    await ctx.send(f'Alternate name **{alias.lower()}** added for character **{name.title()}**.')
                except Exception:
                    await ctx.send('Alternate name already existed.')
            else:
                if versionTemp != 'BASE':
                    version = versionTemp
                if version in char:
                    version = version.lower()
                    try:
                        fetchStatement = 'SELECT * FROM alt_names WHERE server_id=? AND alt_name=?'
                        cursor.execute(fetchStatement, (ctx.guild.id, alias))
                        result = cursor.fetchone()
                        if result:
                            raise Exception()

                        statement = 'INSERT INTO aliases VALUES(?, ?, ?, ?)'
                        cursor.execute(statement, (ctx.guild.id, alias, name, version))
                        db.commit()
                        await ctx.send(f'Alias **{alias}** added for character **{name.title()} ({version.title()})**.')
                    except Exception:
                        await ctx.send('Alias already existed.')
                else:
                    await ctx.send(f'Version *{version.title()}* not found for the character *{name.title()}*.')

    def getCharVersion(self, ctx, name, version='BASE', uncap='6'):
        name = name.lower()
        if not uncap:
            uncap = '6'
        if version:
            if version == '6' or version.upper() == 'ULB':
                version = 'BASE'
                uncap = '6'
            elif version == '5' or version.upper() == 'FLB':
                version = 'BASE'
                uncap = '5'
            elif version == '4' or version.upper() == 'MLB':
                version = 'BASE'
                uncap = '4'
            version = version.upper()
        else:
            uncap = '6'

        if uncap.upper() == 'MLB':
            uncap = '4'
        elif uncap.upper() == 'FLB':
            uncap = '5'
        elif uncap.upper() == 'ULB':
            uncap = '6'

        if not name in self.chars:
            import sqlite3
            from contextlib import closing
            connection = sqlite3.connect('db/kolulu.db')
            with closing(connection) as db:
                cursor = db.cursor()
                fetchAltName = 'SELECT char_name FROM alt_names WHERE server_id=? AND alt_name=?'
                cursor.execute(fetchAltName, (ctx.guild.id, name))
                result = cursor.fetchone()
                if result:
                    name = result[0]
                else:
                    fetchAlias = 'SELECT char_name, char_version FROM aliases WHERE server_id=? AND alias_name=?'
                    cursor.execute(fetchAlias, (ctx.guild.id, name))
                    result = cursor.fetchone()
                    if result:
                        name = result[0]
                        version = result[1].upper()
                    else:
                        return None, version, uncap

        char = self.chars[name]
        if not version or version not in char:
            version = 'BASE'
        if uncap == '4' and (char[version]['max_evo'] == '5' or char[version]['max_evo'] == '6'):
            if not version.endswith('_4'):
                version += '_4'
        elif uncap == '5' and char[version]['max_evo'] == '6':
            if not version.endswith('_5'):
                version += '_5'
        return name, version, uncap
    

def setup(client):
    client.add_cog(Character(client))
