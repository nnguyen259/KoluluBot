import discord, json, DiscordUtils
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
            charOugi = self.ougis[name][version]
            charSkill = self.skills[name][version]
            name = name.title()

            msg = f'{self.emojis["Rarity"][charVersion["rarity"]]} **{name} ({version})**'

            title = f'{self.emojis["Element"][charVersion["element"]]} **{charVersion["element"]}** {self.emojis["Type"][charVersion["type"]]} **{charVersion["type"]}**\n'
            for specialty in charVersion['specialties']:
                title += f'{self.emojis["Specialty"][specialty]} **{specialty}** '

            description = f'{self.emojis["Gender"][char["gender"]]} **{char["gender"]}** {self.emojis["Race"][charVersion["race"]]} **{charVersion["race"]}**'
            description += f'\n{self.emojis["Stat"]["Hp"]} *{charVersion["hp"]}* \n{self.emojis["Stat"]["Atk"]} *{charVersion["atk"]}*'

            ougi = ''
            for ougiText in charOugi['text']:
                ougi += ougiText + '\n'

            embedList = []

            mainEmbed = discord.Embed()
            mainEmbed.title = title
            mainEmbed.description = description
            mainEmbed.set_thumbnail(url=charVersion['thumbnail'])
            mainEmbed.set_image(url=charVersion['image'])
            mainEmbed.add_field(name=f'Charge Attack: {charOugi["name"]}', value=ougi, inline=False)
            embedList.append(mainEmbed)

            for skill in charSkill:
                skillEmbed = discord.Embed()
                skillText = ''
                for text in skill['text']:
                    skillText += text + '\n'
                skillName = f'{self.emojis["Skill"][skill["type"]]} {skill["name"]} ({skill["cooldown"]}T)'
                skillEmbed.title = skillName
                skillEmbed.description = skillText
                skillEmbed.set_image(url=charVersion['image'])
                embedList.append(skillEmbed)


            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('🔐', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")

            await paginator.run(embedList)
        else:
            await ctx.send('Character not found!')

def setup(client):
    client.add_cog(Character(client))