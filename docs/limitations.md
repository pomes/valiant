# Limitations

It's new! ...and can be improved!

- Only packages in the central [PyPI](https://pypi.org/) repo can be queried
- The report providers are currently built-in. The ultimate goal is to provide a
    [Flake8-style plugin model](http://flake8.pycqa.org/en/latest/plugin-development/index.html)
- The caching database doesn't get stored in the cache directory -
    [track this issue](https://github.com/pomes/valiant/issues/4)
