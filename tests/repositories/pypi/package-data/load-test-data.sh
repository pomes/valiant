#!/bin/bash

# Gets the latest version of the package info from PyPi
# for a set of test packages

IFS=":"

test_data=("appdirs:1.4.3" \
    "flask:0.1" \
    "gpiozero:1.5.1" \
    "opencv-python:4.2.0.32" \
    "pipenv:2018.11.26" \
    "rdflib:4.2.2" \
    "tensorflow:2.1.0" \
    "django:3.0.4" \
    "flask:1.1.1"  \
    "numpy:1.18.2" \
    "pandas:1.0.3" \
    "poetry:1.0.5" \
    "six:1.14.0" \
    "twisted:20.3.0")

for item in "${test_data[@]}"
    do
    read -ra pkg <<< $item
    curl -L -o ${pkg[0]}-${pkg[1]}.json https://pypi.org/pypi/${pkg[0]}/${pkg[1]}/json
done
