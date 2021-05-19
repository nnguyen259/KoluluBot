import os, io
import discord, json, DiscordUtils
from discord.ext import commands
from discord.ext.commands.context import Context
from urllib.request import urlopen

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dataPath = os.getenv("data")
        self.font = urlopen('https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Medium.ttf')
        self.icon_url = 'https://cdn.discordapp.com/attachments/828230402875457546/839701583515222026/321247751830634496.png'
        self.helper = client.get_cog('CharHelper')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.reload()

    @commands.group(aliases=['c', 'character'])
    async def char(self, ctx : Context):
        if ctx.invoked_subcommand is None:
            offset = 0
            args = ctx.message.content.split(' ')[1:]
            name = args[0]
            if name in ['c', 'char', 'character']:
                name = args[1]
                offset = 1
            version = args[1 + offset] if len(args) > 1 + offset else None
            uncap = args[2 + offset] if len(args) > 2 + offset else None
            await self.info(ctx, name, version, uncap)

    @char.command()
    async def reload(self, ctx):
        self.helper.loadData()
        await ctx.send('Data reloaded')

    @char.command()
    async def info(self, ctx, name : str, version=None, uncap='6'):
        name, version, uncap, noVersion = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        msg = self.getUncapMessage(name, version, uncap)
        mainEmbed = self.helper.getInfo(name, version)
        embedList = []
        embedList.append(mainEmbed)
        embedList.append(self.helper.getOugi(name, version))
        embedList.extend(self.helper.getSkill(name, version))
        embedList.extend(self.helper.getSupport(name, version))
        #TODO: Look into ImgurAPI for this
        # embedList.append(await self.emp(ctx, name, version, uncap, noShow=True))

        for embed in embedList:
            index = embedList.index(embed)
            footerText = f'({index+1}/{len(embedList)})\nData obtained from GBF Wiki'
            if msg:
                footerText += f'\n{msg}'
            embed.set_footer(text=footerText, icon_url=self.icon_url)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=False)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    @char.command()
    async def ougi(self, ctx, name :str, version=None, uncap='6'):
        name, version, uncap, noVersion = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        msg = self.getUncapMessage(name, version, uncap)

        ougiEmbed = self.helper.getOugi(name, version)

        footerText = f'Data obtained from GBF Wiki'
        if msg:
            footerText += f'\n{msg}'
        ougiEmbed.set_footer(text=footerText, icon_url=self.icon_url)
        await ctx.send(embed=ougiEmbed)

    @char.command()
    async def skill(self, ctx, name, version=None, uncap='6'):
        name, version, uncap, noVersion = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        msg = self.getUncapMessage(name, version, uncap)

        embedList = self.helper.getSkill(name, version)

        for embed in embedList:
            index = embedList.index(embed)
            footerText = f'({index+1}/{len(embedList)})\nData obtained from GBF Wiki'
            if msg:
                footerText += f'\n{msg}'
            embed.set_footer(text=footerText, icon_url=self.icon_url)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=False)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    @char.command()
    async def support(self, ctx, name :str, version=None, uncap='6', noShow=False):
        name, version, uncap, noVersion = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        msg = self.getUncapMessage(name, version, uncap)

        embedList = self.helper.getSupport(name, version)

        for embed in embedList:
            index = embedList.index(embed)
            footerText = f'({index+1}/{len(embedList)})\nData obtained from GBF Wiki'
            if msg:
                footerText += f'\n{msg}'
            embed.set_footer(text=footerText, icon_url=self.icon_url)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=False)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    @char.command()
    async def emp(self, ctx, name : str, version=None, uncap='6', noShow=False):
        

        name, version, uncap, noVersion = self.getCharVersion(ctx, name, version, uncap)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        msg = self.getUncapMessage(name, version, uncap)
        
        embed, file = self.helper.getEmp(name, version)
        footerText = f'Data obtained from GBF Wiki'
        if msg:
            footerText += f'\n{msg}'
        embed.set_footer(text=footerText, icon_url=self.icon_url)

        await ctx.send(file=file, embed=embed)

    @char.command(hidden=True)
    async def refresh(self, ctx):
        import shutil
        shutil.rmtree('cache/emp/char', ignore_errors=True)
        await ctx.send('Removed charcter emp caches.')

    @char.command()
    async def art(self, ctx, name, version=None):
        name, version, _, noVersion = self.getCharVersion(ctx, name, version, None)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        charVersion = self.chars[name][version]
        charId = charVersion['id']
        maxVersion = 2
        if charVersion['max_evo'] == '5':
            maxVersion = 3
        elif charVersion['max_evo'] == '6':
            maxVersion = 4
        embedList = []

        for i in range(maxVersion):
            embed = discord.Embed()
            embed.set_image(url=f'http://game-a.granbluefantasy.jp/assets_en/img/sp/assets/npc/zoom/{charId}_0{i+1}.png')
            embedList.append(embed)

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=60, remove_reactions=True, auto_footer=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")

        await paginator.run(embedList)

    @char.group()
    async def search(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('No search term specified.')

    @char.group()
    @commands.guild_only()
    async def alias(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Alias command not found!')

    @alias.command()
    async def add(self, ctx, alias, name, version=None):
        import sqlite3
        from contextlib import closing

        name, versionTemp, _, _ = self.getCharVersion(ctx, name, version)
        if not name:
            await ctx.send('Character not found!')
            return
        alias = alias.lower()
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            cursor = db.cursor()
            char = self.helper.chars[name]
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

    @alias.command()
    async def remove(self, ctx, alias):
        import sqlite3
        from contextlib import closing

        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            cursor = db.cursor()
            statement = 'DELETE FROM alt_names WHERE server_id=? and alt_name=?'
            statement2 = 'DELETE FROM aliases WHERE server_id=? and alias_name=?'

            input = (ctx.guild.id, alias.lower())
            cursor.execute(statement, input)
            cursor.execute(statement2, input)
            db.commit()
        await ctx.send(f'Alias **{alias}** deleted.')

    @alias.command()
    async def list(self, ctx, name, version=None):
        import sqlite3
        from contextlib import closing

        name, version, _, noVersion = self.getCharVersion(ctx, name, version, None)
        if not name:
            await ctx.send('Character not found!')
            return
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)

        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            if version == 'BASE':
                statement = 'SELECT alt_name FROM alt_names WHERE server_id=? AND char_name=?'
                input = (ctx.guild.id, name)
            else:
                statement = 'SELECT alias_name FROM aliases WHERE server_id=? AND char_name=? AND char_version=?'
                input = (ctx.guild.id, name, version.lower())

            cursor = db.cursor()
            cursor.execute(statement, input)
            results = cursor.fetchall()
            if len(results) == 0:
                await ctx.send(f'No alias found for character **{name.title()} ({version.title()})**')
            else:
                results = sorted(list(zip(*results))[0])
                msg = f'Aliases for **{name.title()} ({version.title()})**:\n'
                msg += '\n'.join(results)
                await ctx.send(msg)

    def getCharVersion(self, ctx, name, version, uncap='6'):
        uncaps = {'4', '5', '6', 'MLB', 'FLB', 'ULB'}
        noVersion = False

        name = name.lower()
        if not uncap or uncap not in uncaps:
            uncap = '6'
        if version:
            version = version.upper()
            if version in uncaps:
                noVersion = True
                if version in {'4', 'MLB'}:
                    uncap = '4'
                elif version in {'5', 'FLB'}:
                    uncap = '5'
                else:
                    uncap = '6'
                version = 'BASE'

        if uncap.upper() == 'MLB':
            uncap = '4'
        elif uncap.upper() == 'FLB':
            uncap = '5'
        elif uncap.upper() == 'ULB':
            uncap = '6'

        if not name in self.helper.chars:
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
                        return None, version, uncap, noVersion

        char = self.helper.chars[name]
        if not version or version not in char:
            version = 'BASE'
            noVersion = True
        if uncap == '4' and (char[version]['max_evo'] == '5' or char[version]['max_evo'] == '6'):
            if not version.endswith('_4'):
                version += '_4'
        elif uncap == '5' and char[version]['max_evo'] == '6':
            if not version.endswith('_5'):
                version += '_5'
        return name, version, uncap, noVersion

    def sendDefault(self, ctx, name):
        versions = [version.title() for version in self.helper.chars[name] if '_' not in version]
        versions = [version for version in versions if not version.startswith('Base')]
        if len(versions) == 0: return ""
        versionText = ', '.join(versions)
        charName = self.helper.chars[name]['BASE']['name']
        charName = charName.rsplit(' ')[0] if charName.endswith(')') or charName.endswith('\u2605') else charName
        return f'Using the default version for character **{charName}**.\nOther valid versions: **{versionText}**'

    def getUncapMessage(self, name, version, uncap):
        charVersion = self.helper.chars[name][version]
        charName = charVersion['name']
        charName = charName.rsplit(' ')[0] if charName.endswith(')') or charName.endswith('\u2605') else charName
        maxUncap = int(charVersion["max_evo"])
        currentUncap = int(uncap)

        if currentUncap > maxUncap:
            currentUncap = maxUncap

        if maxUncap < 5: return ''

        if maxUncap == currentUncap:
            msg = f'Showing the highest uncap for character {charName}.\nFor lower uncap add 5 or 4 to the end of the command.'
        else:
            msg = f'Showing the {currentUncap}* uncap for character {charName}.'
        return msg

def setup(client):
    client.add_cog(Character(client))
