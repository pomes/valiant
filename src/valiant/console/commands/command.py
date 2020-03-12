from cleo import Command as BaseCommand


class Command(BaseCommand):

    loggers = []

    @property
    def valiant(self):
        return self.application.valiant

    def reset_valiant(self):  # type: () -> None
        self.application.reset_valiant()
