from discord.ext.commands.help import DefaultHelpCommand

class KoluluHelpCommand(DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    def get_ending_note(self):
        """:class:`str`: Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        return (
            f"Type {self.context.clean_prefix}{command_name} command for more info on a command.\n"
            f"You can also type {self.context.clean_prefix}{command_name} category for more info on a category.\n"
            f"For further support and feedback please visit the support server at \u200bdiscord.gg/yATu8Z2A6R\u200b"
        )