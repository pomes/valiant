# Configuration

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

You'll also notice that wherever you run the `valiant` command you'll see a file named
`valiant-0.1.0-requests-cache.sqlite` has been created. This is a cache for web
requests and helps both speed up Valiant as well as reduce load on repository servers.
Track any update to this in [Issue #4](https://github.com/pomes/valiant/issues/4).
