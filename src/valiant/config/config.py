from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    def __init__(self, default_config: Optional[Dict[str, Any]] = None, **kwargs):
        if default_config:
            self._config = deepcopy(default_config)

        if "cache-dir" in self._config:
            self._cache_dir = Path(self._config["cache-dir"])
        else:
            self._cache_dir = None

    @property
    def cache_dir(self) -> Optional[Path]:
        return self._cache_dir
