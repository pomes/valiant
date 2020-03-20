"""The primary entrypoint into the valiant project."""
import os

from .valiant import Valiant


_ROOT = os.path.dirname(os.path.realpath(__file__))


class Factory:
    """Generate new Valiant instances."""

    from typing import Optional
    from .config import Config

    def create_valiant(self, config: Optional[Config] = None) -> Valiant:
        """Generates a valiant instance.

        TBD - this factory is rather underdone atm.

        Args:
            config: A Valiant configuration instance.

        Returns:
            A freshly built valiant
        """
        from .config.config import _load_default_config

        if not config:
            conf = _load_default_config()
        else:
            conf = config

        return Valiant(config=conf)
