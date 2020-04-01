"""A helpful base to get started from."""
import json
import traceback

from typing import Optional

from cleo import Command as CleoCommand
from clikit.api.io.flags import VERBOSE
from valiant import Valiant


class BaseCommand(CleoCommand):
    """Common methods for most commands."""

    __valiant: Optional[Valiant] = None

    @staticmethod
    def singleton_valiant(command: "BaseCommand") -> Valiant:
        """This should only create 1 instance of Valiant.

        Also, handles the --config option.

        Args:
            command: Used to grab the cli options

        Returns:
            The hopefully single instance.

        Raises:
            ValueError: When a Valiant instance couldn't be created.
        """
        from pathlib import Path
        from valiant.config.util import (
            generate_valiant_config_from_map,
            create_valiant_builder,
        )
        from valiant.config.source import TomlSource

        if not BaseCommand.__valiant:
            config_builder = create_valiant_builder()
            if command.option("config"):
                config_builder.add_source(
                    TomlSource(Path(command.option("config")), optional=False)
                )
            conf_map = config_builder.build()

            if not conf_map:
                raise ValueError("Failed to construct the Valiant configuration.")

            conf = generate_valiant_config_from_map(conf_map)
            BaseCommand.__valiant = Valiant(conf)
        return BaseCommand.__valiant

    @property
    def valiant(self) -> Valiant:
        """Access the Valiant application object."""
        return BaseCommand.singleton_valiant(self)  # noqa: DAR201

    def output_error(self, e: Exception, format: str = None) -> None:
        """Outputs the error to the required format."""  # noqa:DAR101
        if format == "json":
            data = {"error": {"type": e.__class__.__name__, "message": str(e)}}
            if self.io.is_verbose():
                data["error"]["trace"] = traceback.format_exc()
            self.line_error(json.dumps(data))
        else:
            output = f"<error>{e.__class__.__name__}: {e}\n"
            self.line_error(output)
            if self.io.is_verbose():
                self.line_error(
                    f"<debug>{traceback.format_exc()}</debug>", verbosity=VERBOSE
                )
