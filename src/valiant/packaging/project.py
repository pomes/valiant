from dataclasses import dataclass


@dataclass
class Project:
    name: str
    description: str
    home_page: str
    repository_url: None
    documentation_url: None
    keywords: []
    license: None
    versions: None


def load_project() -> Project:
    pass
