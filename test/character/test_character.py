from cogs.character import Character
from discord.ext import commands

class TestCharacter():
    testClass = Character(commands.Bot)

    def test_get_char_version(self):
        name, version, uncap = self.testClass.getCharVersion(None, 'abby', 'PROMO')
        assert self.testClass.chars[name][version] == self.testClass.chars['abby']['PROMO']

    def test_get_char_no_version(self):
        name, version, uncap = self.testClass.getCharVersion(None, 'abby')
        assert self.testClass.chars[name][version] == self.testClass.chars['abby']['BASE']

    def test_get_char_alias(self):
        ...

    def test_get_char_version_alias(self):
        ...