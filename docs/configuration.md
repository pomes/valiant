# Configuration

## Version 0.1.0
It's still very early days and Valiant isn't configurable. You can check the
settings with:

    valiant config

This will display the current configuration:

    cache_dir: /home/fred/.cache/valiant/0.1.0
    config_dir: /home/fred/.config/valiant/0.1.0
    default_repository_name: pypi
    repositories: pypi
    reports: basic,spdx,safety

If you check the `config_dir` you'll see that Valiant is putting its logs in there.

### Notes

You'll also notice that wherever you run the `valiant` command you'll see a file named
`valiant-0.1.0-requests-cache.sqlite` has been created. This is a cache for web
requests and helps both speed up Valiant as well as reduce load on repository servers.
Track any update to this in [Issue #4](https://github.com/pomes/valiant/issues/4).

## Version 0.2.0

Configuration has been improved under version 0.2.0 - and will benefit from
real-world testing.

This version will allow you to load configuration from multiple sources, including
from a config file passed via the command line.

Valiant configuration uses the [TOML](https://github.com/toml-lang/toml) format.

The easiest way to start a custom configuration is to run the following:

    valiant config --out toml

This will provide a base config file that you can start editing. The example config
below is a useful start:

```toml
[tool.valiant]
configuration_dir = "/etc/valiant"
cache_dir = "/tmp/valiant/cache"
log_dir = "/tmp/valiant/log"
default_reports = [ "basic" ]

[tool.valiant.requests_cache]
file = "$cache_dir/valiant-0.2.0-requests-cache"
backend = "sqlite"
expire_after = 86400
```

I can save the config into a file named `test.toml` and use the following command:

    poetry run valiant config --config test.toml -o toml

### Placeholders

You'll note the `$cache_dir` placeholder in the `file` setting for `requests-cache`.
A very limited set of placeholders are available for the following settings:

- `[tool.valiant.requests_cache]` - `file`: The location of the requests cache. Note
    that you don't include the file extension here.

The following placeholders will work and are based on the associated config setting:

- `configuration_dir`
- `cache_dir`
- `log_dir`

### Configuring logs

Who doesn't love configuring logs?

Valiant makes use of [`structlog`](http://www.structlog.org/en/stable/) to provide
logging. If you need a custom logging setup, you first set up a
[logging configuration file](https://docs.python.org/3/library/logging.config.html#logging-config-fileformat)
- the one below just spits out to the command line (stdout):

```ini
[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(message)s
datefmt=
```

Then, in your Valiant config file, set the `logging_configuration_file` entry
to the location of your logging config file:

```toml
[tool.valiant]
logging_configuration_file = "/etc/valiant/logging.conf"
```

### The loading process

Configuration can be loaded from a number of places.

_Before we start_ please note that the `configuration_dir` setting
doesn't indicate a location for Valiant to look for its own configuration.
Instead, it could be used by plugins. If you need to specify a Valiant
configuration file, please use the `--config` option in the command line.

To start with, run the `config` command as follows:

    poetry run valiant config -v

You'll see something along the following lines:

```bash
configuration_dir: /home/fred/.config/valiant/0.2.0
cache_dir: /home/fred/.cache/valiant/0.2.0
log_dir: /home/fred/.cache/valiant/0.2.0/log
default_repository: pypi
repositories: pypi
reports :  {'basic', 'spdx', 'safety'}
metadata:
  {'build_results': {'dictionary': 'Read',
                   '/etc/xdg/xdg-cinnamon/valiant/0.2.0/config.toml': 'Not_Read',
                   '/home/fred/.config/valiant/0.2.0/config.toml': 'Not_Read',
                   '/home/fred/my_project/pyproject.toml': 'Read'}}
```

The `metadata` section illustrates how Valiant is loading its configuration:

1. First of all, a default config is read (noted as `dictionary`)
2. Then a site-level `config.toml` is checked - in this example, `Not_Read` highlights
    that no file was found.
3. Then the user-level `config.toml` file is read, if it exists
4. Finally, if the current directory has a
    [`pyproject.toml`](https://www.python.org/dev/peps/pep-0518/) file then it will
    be read
5. (not shown) If I passed in a configuration file using the `--config` option this will
    be read last

_Note:_ The [AppDirs package](https://pypi.org/project/appdirs/) is used to determine
appropriate directory locations - check out their doco for the rationale behind the
selected directories.

Importantly, each step can replace settings made in an earlier step. This means that,
ultimately, the file passed in with the `--config` option will gazump earlier settings.
