from .command import Command


class SearchCommand(Command):
    """
    Searches for packages on remote repositories.

    search
        {tokens* : The tokens to search for}
    """

    def handle(self):
        pass
