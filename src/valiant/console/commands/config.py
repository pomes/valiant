from .command import Command


class ConfigCommand(Command):
    """
    Lists the configuration settings.

    config
    """

    def handle(self):
        self.line(f"""<info>cache-dir</info> = {self.valiant.cache_dir}""")
