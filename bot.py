import discord, os, json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot('?gbf ')

@bot.event
async def on_ready():
    global chars
    with open('data/characters.json', 'r') as charFile:
        chars = json.load(charFile)
    print('Bot is ready.')

@bot.command()
async def char(ctx, name, version=None):
    if name in chars:
        outChar = None
        if not version:
            outChar = chars[name]['versions'][0]
            version = chars[name]['versions'][0]['name']
        else:
            for alt in chars[name]['versions']:
                if alt['name'] == version:
                    outChar = alt
                    break
        if not outChar:
            outChar = chars[name]['versions'][0]
            version = chars[name]['versions'][0]['name']

        embed = discord.Embed()
        embed.title = name + ' (' + version + ')'
        embed.description = '**HP:** ' + str(outChar['hp']) + '\t**ATK:** ' + str(outChar['atk']) + '\n**Race:** ' + outChar['race'] + '\t**Style:** ' + outChar['style']
        embed.set_thumbnail(url=outChar['thumbnail'])
        await ctx.send(embed=embed)
    else:
        await ctx.send('Character not found!')

bot.run(os.getenv('token'))