import os
import discord, DiscordUtils
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
    @commands.guild_only()
    async def char(self, ctx : Context):
        """Information on characters

        When no subcommand is provided, the info command is used.
        When the character cannot be found, the bot will look for alternatives in this ordre:
        - Default alternative name list
        - Default alias list
        - Server specific alternative name list
        - Server specific alias list
        - Fuzzymatching name
        """        
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

    @char.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        """Reload the data for the bot

        Data is stored at https://github.com/nnguyen259/KoluluData
        """        
        self.helper.loadData()
        await ctx.send('Data reloaded')

    @char.command()
    async def info(self, ctx, name : str, version=None, uncap='6'):
        """Complete information on a character

        name: Character Name.
        version: The specific version for the character.
        uncap: The uncap level for the version.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        
        Valid inputs for uncap include: MLB, FLB, ULB, 4, 5, 6. When no uncap level is specified, the highest uncap level is used.
        """        
        name, version, uncap, noVersion, _ = self.getCharVersion(ctx, name, version, uncap)
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
        paginator.add_reaction('??????', "first")
        paginator.add_reaction('???', "back")
        paginator.add_reaction('????', "lock")
        paginator.add_reaction('???', "next")
        paginator.add_reaction('??????', "last")

        await paginator.run(embedList)

    @char.command()
    async def ougi(self, ctx, name :str, version=None, uncap='6'):
        """Information on Charge Attacks/Ougi

        name: Character Name.
        version: The specific version for the character.
        uncap: The uncap level for the version.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        
        Valid inputs for uncap include: MLB, FLB, ULB, 4, 5, 6. When no uncap level is specified, the highest uncap level is used.
        """        
        name, version, uncap, noVersion, _ = self.getCharVersion(ctx, name, version, uncap)
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
        """Information on Skills

        name: Character Name.
        version: The specific version for the character.
        uncap: The uncap level for the version.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        
        Valid inputs for uncap include: MLB, FLB, ULB, 4, 5, 6. When no uncap level is specified, the highest uncap level is used.
        """        
        name, version, uncap, noVersion, _ = self.getCharVersion(ctx, name, version, uncap)
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
        paginator.add_reaction('??????', "first")
        paginator.add_reaction('???', "back")
        paginator.add_reaction('????', "lock")
        paginator.add_reaction('???', "next")
        paginator.add_reaction('??????', "last")

        await paginator.run(embedList)

    @char.command()
    async def support(self, ctx, name :str, version=None, uncap='6'):
        """Information on Support Skills and EMP Skills

        name: Character Name.
        version: The specific version for the character.
        uncap: The uncap level for the version.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        
        Valid inputs for uncap include: MLB, FLB, ULB, 4, 5, 6. When no uncap level is specified, the highest uncap level is used.
        """        
        name, version, uncap, noVersion, _ = self.getCharVersion(ctx, name, version, uncap)
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
        paginator.add_reaction('??????', "first")
        paginator.add_reaction('???', "back")
        paginator.add_reaction('????', "lock")
        paginator.add_reaction('???', "next")
        paginator.add_reaction('??????', "last")

        await paginator.run(embedList)

    @char.command()
    async def emp(self, ctx, name : str, version=None, uncap='6'):
        """Information on the EMP Table

        name: Character Name.
        version: The specific version for the character.
        uncap: The uncap level for the version.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        
        Valid inputs for uncap include: MLB, FLB, ULB, 4, 5, 6. When no uncap level is specified, the highest uncap level is used.
        """        
        name, version, uncap, noVersion, _ = self.getCharVersion(ctx, name, version, uncap)
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
    @commands.is_owner()
    async def refresh(self, ctx):
        import shutil
        shutil.rmtree('cache/emp/char', ignore_errors=True)
        await ctx.send('Removed charcter emp caches.')

    @char.command()
    async def art(self, ctx, name, version=None):
        """Display the artworks for the character

        name: Character Name.
        version: The specific version for the character.

        When no version is specified or the specified version is invalid, the bot defaults to the first release version of the highest rarity. This does not always match up with the naming used by GBF Wiki.
        """        
        name, version, _, noVersion, _ = self.getCharVersion(ctx, name, version, None)
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
        charVersion = self.helper.chars[name][version]
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
        paginator.add_reaction('??????', "first")
        paginator.add_reaction('???', "back")
        paginator.add_reaction('????', "lock")
        paginator.add_reaction('???', "next")
        paginator.add_reaction('??????', "last")

        await paginator.run(embedList)

    @char.group(hidden=True)
    async def search(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('No search term specified.')

    @char.group()
    @commands.guild_only()
    async def alias(self, ctx):
        """Manage and view aliases

        Aliases work on a per server basis (i.e Each server keeps its own list of aliases).

        There are 2 types of aliases: Alternate Name and Version Alias.
        Alternate Name can be used in place of the character's actual name (i.e Six instead of Seox)
        Version Alias replaces both the name and the version of a character (i.e SKolulu for Summer Kolulu)

        Both versions of aliases will work in place a name and/or version is used, including when adding a new alias.
        """        
        if ctx.invoked_subcommand is None:
            await ctx.send('Alias command not found!')

    @alias.command()
    async def add(self, ctx, alias, name, version=None):
        """Add a new alias

        alias: The name of the alias to be added
        name: The character to have the alias applied to
        version: The version of the character to have the alias applied to

        Version is an optional argument. If no version is specified, an Alternate Name is created, otherwise a new Version Alias is created.

        An error is raised if an invalid version is provided.
        """        
        import sqlite3
        from contextlib import closing

        name, versionTemp, _, _, redirect = self.getCharVersion(ctx, name, version)
        alias = alias.lower()
        if alias in self.helper.chars:
            await ctx.send('Cannot use character name as alias!')
            return
        if alias in self.helper.altNames or alias in self.helper.aliases:
            await ctx.send('Alias already existed!')
            return
        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            cursor = db.cursor()
            char = self.helper.chars[name]
            if redirect:
                version = versionTemp
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
        """Remove an alias

        alias: The name of the alias to be removed

        If the alias belongs to the default set provided by the bot, it is considered protected and cannot be removed.
        """     
        import sqlite3
        from contextlib import closing

        alias = alias.lower()

        if alias in self.helper.chars:
            await ctx.send('Character name is not an alias.')
            return

        if alias in self.helper.altNames or alias in self.helper.aliases:
            await ctx.send('Cannot delete alias. Alias belongs to a protected set.')
            return

        connection = sqlite3.connect('db/kolulu.db')
        with closing(connection) as db:
            cursor = db.cursor()
            statement = 'DELETE FROM alt_names WHERE server_id=? and alt_name=?'
            statement2 = 'DELETE FROM aliases WHERE server_id=? and alias_name=?'

            input = (ctx.guild.id, alias)
            cursor.execute(statement, input)
            cursor.execute(statement2, input)
            db.commit()
        await ctx.send(f'Alias **{alias}** deleted.')

    @alias.command()
    async def list(self, ctx, name, version=None):
        """List alias(es) for the character

        name: The character to have their aliases listed
        version: The version of the character

        Version is an optional argument. If no version is provided or the provided version is invalid, all the Alternate Names for the character will be listed. Otherwise, all the Version Aliases for the character version will be listed.
        """        
        import sqlite3
        from contextlib import closing

        name, version, _, noVersion, _ = self.getCharVersion(ctx, name, version, None)
        if noVersion:
            msg = self.sendDefault(ctx, name)
            if msg:
                await ctx.send(msg)
            
            defaultAliases = [k.lower() for k in self.helper.altNames if self.helper.altNames[k].lower() == name]
        else:
            defaultAliases = [k.lower() for k, v in self.helper.aliases.items() if v['character'].lower() == name and v['version'] == version]
        
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
            
            if len(results) + len(defaultAliases) == 0:
                await ctx.send(f'No alias found for character **{name.title()} ({version.title()})**')
            else:
                if len(results):
                    results = sorted(list(zip(*results))[0])
                defaultAliases.extend(results)
                msg = f'Aliases for **{name.title()} ({version.title()})**:\n'
                msg += '\n'.join(defaultAliases)
                await ctx.send(msg)

    def getCharVersion(self, ctx, name, version, uncap='6'):
        uncaps = {'4', '5', '6', 'MLB', 'FLB', 'ULB'}
        noVersion = False
        redirect = False

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
            # Check default alt names
            if name in self.helper.altNames:
                name = self.helper.altNames[name].lower()
            # Check default aliases
            elif name in self.helper.aliases:
                version = self.helper.aliases[name]['version']
                name = self.helper.aliases[name]['character'].lower()
            # Get from db otherwise
            else:
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
                            from fuzzywuzzy import process, fuzz
                            names = process.extractBests(name, self.helper.chars.keys(), scorer=fuzz.partial_ratio)
                            names = [name for name, score in names if score == names[0][1]]
                            tempNames = [n for n in names if n[0] == name[0]]
                            if len(tempNames):
                                names = tempNames
                            name = names[0]

        char = self.helper.chars[name]
        if not version:
            version = 'BASE'
            noVersion = True
        if version not in char:
            if version in self.helper.versions[name]:
                tempData = self.helper.versions[name][version]
                if 'character' in tempData:
                    name = tempData['character'].lower()
                version = tempData['version']
                char = self.helper.chars[name]
                redirect = True
            else:
                version = 'BASE'
                noVersion = True
        if uncap == '4' and (char[version]['max_evo'] == '5' or char[version]['max_evo'] == '6'):
            if not version.endswith('_4'):
                version += '_4'
        elif uncap == '5' and char[version]['max_evo'] == '6':
            if not version.endswith('_5'):
                version += '_5'
        return name, version, uncap, noVersion, redirect

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
