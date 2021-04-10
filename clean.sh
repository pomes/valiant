#!/bin/bash -xe

rm -rfv .nox/
rm -rfv .pytest_cache/
rm -rfv build/
rm -rfv .mypy_cache/
rm -rfv .pytype/
rm -rfv junit/

find -name "__pycache__" -type d -exec rm -rv {} \;
find -name ".pytest_cache" -type d -exec rm -rv {} \;
find -name "*.egg-info" -type d -exec rm -rv {} \;
find -name ".coverage" -type f -delete
find -name "*.py,cover" -type f -delete
