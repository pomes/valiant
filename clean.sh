#!/bin/bash

rm -rf .nox
rm -rf .pytest_cache
rm -rf build
rm -rf .mypy_cache
rm -rf .pytype

find -name "__pycache__" -type d -exec rm -r {} \;
find -name ".pytest_cache" -type d -exec rm -r {} \;
find -name "*.egg-info" -type d -exec rm -r {} \;
find -name ".coverage" -type f -delete
find -name ".py,cover" -type f -delete
