"""A centralised set of config information."""
from .__version__ import __version__


application_name = "valiant"
application_title = "Valiant"
application_version = __version__
application_vendor = "Pomes"
application_tagline = "Dependency Investigations Unit"
application_description = "Valiant helps you investigate dependencies"
application_licence = "MIT"
application_copyright_year = 2020
application_copyright_holder = "Duncan Dickinson"
application_homepage = "https://github.com/pomes/valiant"
application_config_file = f"{application_name}.toml"
application_envvar_prefix = "VALIANT_"
pyproject_config_file = "pyproject.toml"
user_config_file = "config.toml"
