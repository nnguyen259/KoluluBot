import discord, os, io, json
from discord.ext import commands
from urllib.request import urlopen

class CharHelper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dataPath = os.getenv("data")
        self.font = urlopen('https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Medium.ttf')
        self.loadData()

    def loadData(self):
        try:
            data = urlopen(f'{self.dataPath}/characters.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'characters.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.chars = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/emoji.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'emoji.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.emojis = json.load(data)

        try:
            data = urlopen(f'{self.dataPath}/ougi.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'ougi.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.ougis = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/skill.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'skill.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.skills = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/supportskill.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'supportskill.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.supportSkills = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/emp.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'emp.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.emps = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/empdata.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'empdata.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.empData = json.load(data)

        try:
            data = urlopen(f'{self.dataPath}/empdomaindata.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'empdomaindata.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.empDomainData = json.load(data)

        try:
            data = urlopen(f'{self.dataPath}/altname.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'altname.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.altNames = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/alias.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'alias.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.aliases = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/version.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'version.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.versions = dict((k.lower(), v) for k, v in json.load(data).items())

    def getInfo(self, name, version):
        charVersion = self.chars[name][version]
        
        title = f'{self.emojis["Rarity"][charVersion["rarity"].upper()]} '
        for series in charVersion['series']:
            title += f'{self.emojis["Series"][series]} '
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

        embed = discord.Embed()
        embed.title = title
        embed.description = description
        embed.add_field(name='Basic Info.', value=information, inline=False)
        embed.add_field(name='Profile', value=profile, inline=False)
        embed.set_thumbnail(url=charVersion['thumbnail'])
        embed.set_image(url=charVersion['image'])

        return embed

    def getOugi(self, name, version):
        charVersion = self.ougis[name][version]

        ougiEmbed = discord.Embed()
        for ougiList in charVersion:
            value=''
            for ougiText in ougiList["text"]:
                value+= ougiText +"\n"
            ougiEmbed.add_field(name=f'**{ougiList["name"]}**:', value=value, inline=False)

            if "data" in ougiList:
                data = ougiList["data"]
                for details in data:
                    ougiEmbed.add_field(name=details['title'], value="\n".join(details['text']), inline=details['inLine'])

            if ougiList["duration"]:
                duration = ''
                for ougiDuration in ougiList["duration"]:
                    for ougiDurationText in ougiList["duration"][ougiDuration]:
                            duration+= f'{ougiDurationText} and '
                    duration = duration[:-4]
                    duration += f': {ougiDuration}.\n'
                    duration = duration.replace('^s', ' seconds')
                    duration = duration.replace('^i', '')
                    if ougiDuration == '1^t':
                        duration = duration.replace('^t', ' turn')
                    else:
                        duration = duration.replace('^t', ' turns')
                ougiEmbed.add_field(name='Durations', value=f'{duration}\n', inline=False)

        ougiEmbed.title="Charge Attack"
        ougiEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/828230361321963530/830390392565923900/download.png')
        ougiEmbed.set_image(url=self.chars[name][version]['image'])

        return ougiEmbed
    
    def getSkill(self, name, version):
        charVersion = self.skills[name][version]

        embedList = []
        for skillList in charVersion:
            if len(skillList) == 0: continue

            for skill in skillList:
                skillEmbed = discord.Embed(title=f'{skill["name"]}')
                skillEmbed.add_field(name=f'Cooldown: {skill["cooldown"]}', value='\n'.join(skill['text']), inline=False)
                skillEmbed.set_thumbnail(url=f'{skill["icon"][-1]}')
                skillEmbed.set_image(url=self.chars[name][version]['image'])

                if "data" in skill:
                    data = skill["data"]
                    for details in data:
                        skillEmbed.add_field(name=details['title'], value="\n".join(details['text']), inline=details['inLine'])

                if skill['duration']:
                    duration = ''
                    for skillDuration in skill['duration']:
                        for skillDurationText in skill["duration"][skillDuration]:
                                duration+= f'{skillDurationText} and '
                        duration = duration[:-4]
                        duration += f': {skillDuration}.\n'
                        duration = duration.replace('^s', ' seconds')
                        duration = duration.replace('^i', '')
                        if skillDuration == '1^t':
                            duration = duration.replace('^t', ' turn')
                        else:
                            duration = duration.replace('^t', ' turns')
                    skillEmbed.add_field(name='Durations', value=f'{duration}\n', inline=False)

            embedList.append(skillEmbed)
        return embedList
    
    def getSupport(self, name, version):
        charVersion = self.supportSkills[name][version]

        embedList = []
        for supportList in charVersion:
            supportEmbed = discord.Embed()
            supportEmbed.title = f'{supportList["name"]}:'
            supportEmbed.description = "\n".join(supportList['text'])
            supportEmbed.set_thumbnail(url=f'{supportList["thumbnail"]}')
            supportEmbed.set_image(url=self.chars[name][version]['image'])

            if "data" in supportList:
                data = supportList["data"]
                for details in data:
                    supportEmbed.add_field(name=details['title'], value="\n".join(details['text']), inline=details['inLine'])

            if supportList["duration"]:
                duration = ''
                for supportDuration in supportList["duration"]:
                    for supportDurationText in supportList["duration"][supportDuration]:
                            duration+= f'{supportDurationText} and '
                    duration = duration[:-4]
                    duration += f': {supportDuration}.\n'
                    duration = duration.replace('^s', ' seconds')
                    duration = duration.replace('^i', '')
                    if supportDuration == '1^t':
                        duration = duration.replace('^t', ' turn')
                    else:
                        duration = duration.replace('^t', ' turns')
                supportEmbed.add_field(name='Durations', value=f'{duration}\n', inline=False)
            embedList.append(supportEmbed)
        return embedList

    def getEmp(self, name, version):
        from PIL import Image, ImageDraw, ImageFont
        import urllib.request, os

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
                                font = ImageFont.truetype(self.font, 50)
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
        embed.set_footer(text=f'Data obtained from GBF Wiki', icon_url='https://cdn.discordapp.com/attachments/828230402875457546/839701583515222026/321247751830634496.png')

        return embed, file

def setup(client):
    client.add_cog(CharHelper(client))