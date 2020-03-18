"""Example test data."""

import json


BASIC_PKG = json.loads(
    """{
    "info": {
        "author": "",
        "author_email": "",
        "bugtrack_url": "http://bugs.example.com",
        "classifiers": [],
        "description": "Basic description",
        "description_content_type": "",
        "docs_url": "http://docs.example.com",
        "download_url": "",
        "downloads": {
        "last_day": -1,
        "last_month": -1,
        "last_week": -1
        },
        "home_page": "http://project.example.com",
        "keywords": "",
        "license": "",
        "maintainer": "",
        "maintainer_email": "",
        "name": "Demo",
        "package_url": "",
        "platform": "",
        "project_url": "",
        "project_urls": {
        "Code": "",
        "Documentation": "",
        "Homepage": "",
        "Issue tracker": ""
        },
        "release_url": "",
        "requires_dist": [],
        "requires_python": "",
        "summary": "A short summary.",
        "version": "0"
    },
    "last_serial": 1,
    "releases": {},
    "urls": []
}"""
)

BASIC_PKG_2 = json.loads(
    """{
    "info": {
        "author": "",
        "author_email": "",
        "bugtrack_url": "http://bugs.example.com",
        "classifiers": [],
        "description": "Basic description",
        "description_content_type": "",
        "docs_url": "http://docs.example.com",
        "download_url": "",
        "downloads": {
        "last_day": -1,
        "last_month": -1,
        "last_week": -1
        },
        "home_page": "",
        "keywords": "",
        "license": "",
        "maintainer": "",
        "maintainer_email": "",
        "name": "Demo 2",
        "package_url": "",
        "platform": "",
        "project_url": "",
        "project_urls": {
        "Code": "",
        "Documentation": "",
        "Homepage": "http://project.example.com",
        "Issue tracker": ""
        },
        "release_url": "",
        "requires_dist": [],
        "requires_python": "",
        "summary": "A short summary.",
        "version": "0"
    },
    "last_serial": 1,
    "releases": {},
    "urls": []
}"""
)
