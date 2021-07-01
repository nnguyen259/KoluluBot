from cogs.character.helper import CharHelper
import discord
from discord import ButtonStyle
import discord.ui as ui
from discord.ext import commands
from typing import List, Optional

class CharView(commands.Cog):
    def __init__(self, client):
        self.client = client

    class CharacterView(ui.View):
        def __init__(self, client : discord.Client):
            super().__init__()
            self.client = client
            self.embeds = []
            self.idx = 0

        async def interaction_check(self, interaction : discord.Interaction):
            return self.id == interaction.user.id

        def setWikiLink(self, key: str):
            wiki = f'https://gbf.wiki/{key}'
            self.add_item(ui.Button(label='Wiki Link', style=ButtonStyle.grey, url=wiki, row=0))

        def setUser(self, id: int):
            self.id : int = id

        def setAttachment(self, url : str):
            for embed in self.empEmbeds:
                embed.set_image(url=url)
        
        def setEmbeds(self, bioEmbeds : List[discord.Embed], 
                            ougiEmbeds : List[discord.Embed],
                            skillEmbeds : List[discord.Embed],
                            supportEmbeds : List[discord.Embed],
                            empEmbeds : List[discord.Embed],
                            artEmbeds : List[discord.Embed]):
            self.bioEmbeds = bioEmbeds
            self.ougiEmbeds = ougiEmbeds
            self.skillEmbeds = skillEmbeds
            self.supportEmbeds = supportEmbeds
            self.empEmbeds = empEmbeds
            self.artEmbeds = artEmbeds
            self.embeds = self.bioEmbeds

        @ui.button(label='First', style=ButtonStyle.primary, row=0)
        async def first(self, button: ui.Button, interaction: discord.Interaction):
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Prev', style=ButtonStyle.primary, row=0)
        async def prev(self, button: ui.Button, interaction: discord.Interaction):
            self.idx = self.idx - 1 if self.idx > 0 else 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Next', style=ButtonStyle.primary, row=0)
        async def next(self, button: ui.Button, interaction: discord.Interaction):
            self.idx = self.idx + 1 if self.idx < len(self.embeds) - 1 else len(self.embeds) - 1
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Last', style=ButtonStyle.primary, row=0)
        async def last(self, button: ui.Button, interaction: discord.Interaction):
            self.idx = len(self.embeds) - 1
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Profile', style=ButtonStyle.green, row=1)
        async def profile(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.bioEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Ougi', style=ButtonStyle.green, row=1)
        async def ougi(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.ougiEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Skill', style=ButtonStyle.green, row=1)
        async def skill(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.skillEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Support', style=ButtonStyle.green, row=1)
        async def support(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.supportEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='EMP', style=ButtonStyle.green, row=1)
        async def emp(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.empEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

        @ui.button(label='Art', style=ButtonStyle.green, row=2)
        async def art(self, button: ui.Button, interaction: discord.Interaction):
            self.embeds = self.artEmbeds
            self.idx = 0
            embed = self.embeds[self.idx]
            await interaction.message.edit(view=self, embed=embed)

def setup(client):
    client.add_cog(CharView(client))