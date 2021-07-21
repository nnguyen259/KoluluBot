import discord, os, io, json
from discord.ext import commands
from urllib.request import urlopen

class SummonHelper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dataPath = os.getenv("data")
        self.loadData()

    def loadData(self):
        try:
            data = urlopen(f'{self.dataPath}/summons.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'summons.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.summons = dict((k.lower(), v) for k, v in json.load(data).items())

        try:
            data = urlopen(f'{self.dataPath}/emoji.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'emoji.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.emojis = json.load(data)

        try:
            data = urlopen(f'{self.dataPath}/embedcolor.json')
        except Exception:
            with open(os.path.join(self.dataPath, 'embedcolor.json'), 'r', encoding='utf-8') as dataFile:
                data = io.StringIO(dataFile.read())
        self.embedColor = json.load(data)

    def get(self, name):
        summon = self.summons[name]
        versions = summon['versions']
        id = summon['id']
        embedList = []

        mainEmbed = discord.Embed()
        titlePrefix = f'{self.emojis["Summons"][summon["series"]] if summon["series"] else ""} {self.emojis["Element"][summon["element"].title()]} {self.emojis["Rarity"]["SSR"]}'
        mainEmbed.title = f'{titlePrefix} {summon["name"]}'
        mainEmbed.description = f'JP: {summon["jpname"]}'

        if summon['profile']:
            mainEmbed.add_field(name='Profile', value=summon['profile'], inline=False)
        imageUrl = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/detail/{id}{versions[0]["id"] if versions[0]["id"] else ""}.png'
        thumbnailUrl = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/m/{id}{versions[0]["id"] if versions[0]["id"] else ""}.jpg'
        mainEmbed.set_image(url=imageUrl)
        mainEmbed.set_thumbnail(url=thumbnailUrl)
        mainEmbed.colour= int(self.embedColor[summon["element"].title()], 16)
        embedList.append(mainEmbed)

        for version in versions:
            embed = discord.Embed()
            embed.title = f'{mainEmbed.title} ({version["name"]})'
            embed.description = f'{self.emojis["Stat"]["Hp"]} *{version["hp"]}* {self.emojis["Stat"]["Atk"]} *{version["atk"]}*'
            embed.add_field(name=f'Aura: {summon["aura_name"]}', value=version['aura'], inline=False)
            embed.colour= int(self.embedColor[summon["element"].title()], 16)

            if version["duration_aura"]:
                duration = ''
                for auraDuration in version["duration_aura"]:
                    for auraDurationText in version["duration_aura"][auraDuration]:
                            duration += f'{auraDurationText} and '
                    duration = duration[:-4]
                    duration += f': {auraDuration}.\n'
                    duration = duration.replace('^s', ' seconds')
                    duration = duration.replace('^i', '')
                    if auraDuration == '1^t':
                        duration = duration.replace('^t', ' turn')
                    else:
                        duration = duration.replace('^t', ' turns')
                embed.add_field(name='Durations', value=f'{duration}\n', inline=False)

            if version['subaura']:
                embed.add_field(name='Sub-Aura', value=version['subaura'], inline=False)

            callTitle = f'Call: {version["call_name"]} ({version["call_cd"]}T'
            if version["call_cd_first"]:
                callTitle += f'/Inital: {version["call_cd_first"]}T)'
            else:
                callTitle += ')'
            if summon['call_reuse'] != 'Yes':
                callTitle += ' (Cannot Recast)'
            embed.add_field(name=callTitle, value=version["call"], inline=False)

            if summon['comboable'] != 'Yes':
                embed.add_field(name='\u200b', value='**Cannot be included in other players\' combo call.**', inline=False)

            if version["duration_call"]:
                duration = ''
                for callDuration in version["duration_call"]:
                    for callDurationText in version["duration_call"][callDuration]:
                            duration += f'{callDurationText} and '
                    duration = duration[:-4]
                    duration += f': {callDuration}.\n'
                    duration = duration.replace('^s', ' seconds')
                    duration = duration.replace('^i', '')
                    if callDuration == '1^t':
                        duration = duration.replace('^t', ' turn')
                    else:
                        duration = duration.replace('^t', ' turns')
                embed.add_field(name='Durations', value=f'{duration}\n', inline=False)

            image = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/detail/{id}{version["id"] if version["id"] else ""}.png'
            thumbnail = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/m/{id}{version["id"] if version["id"] else ""}.jpg'
            embed.set_image(url=image)
            embed.set_thumbnail(url=thumbnail)
            embedList.append(embed)

        return embedList

def setup(client):
    client.add_cog(SummonHelper(client))
