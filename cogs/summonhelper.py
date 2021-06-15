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

    def get(self, name):
        summon = self.summons[name]
        versions = summon['versions']
        id = summon['id']
        embedList = []

        mainEmbed = discord.Embed()
        mainEmbed.title = summon['name']
        mainEmbed.add_field(name='Profile', value=summon['profile'], inline=False)
        imageUrl = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/detail/{id}{versions[0]["id"] if versions[0]["id"] else ""}.png'
        thumbnailUrl = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/m/{id}{versions[0]["id"] if versions[0]["id"] else ""}.jpg'
        mainEmbed.set_image(url=imageUrl)
        mainEmbed.set_thumbnail(url=thumbnailUrl)
        embedList.append(mainEmbed)

        for version in versions:
            embed = discord.Embed()
            embed.title = f'{summon["name"]} ({version["name"]})'
            embed.add_field(name=f'Aura: {summon["aura"]}', value=version['aura'], inline=False)
            if version['subaura']:
                embed.add_field(name='Sub-Aura', value=version['subaura'], inline=False)
            call = ""
            for text in version['call']['desc']:
                call += f'{text}\n'
            embed.add_field(name=f'Call: {summon["call"]} ({version["call"]["cd"]})', value=call)
            image = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/detail/{id}{version["id"] if version["id"] else ""}.png'
            thumbnail = f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/summon/m/{id}{version["id"] if version["id"] else ""}.jpg'
            embed.set_image(url=image)
            embed.set_thumbnail(url=thumbnail)
            embedList.append(embed)

        return embedList

def setup(client):
    client.add_cog(SummonHelper(client))