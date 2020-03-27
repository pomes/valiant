#!/bin/bash

# Grabs a copy of the metadata for the requested package,version
#
# Usage:
#    ./load.sh <package> <version>

echo Grabbing $1 $2

curl -L -o $1-$2.json https://pypi.org/pypi/$1/$2/json
