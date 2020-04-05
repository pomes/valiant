"""Package exceptions."""
from valiant.exceptions import ValiantException


class RepositoryException(ValiantException):  # noqa: D101

    pass


class PackageNotFoundException(RepositoryException):  # noqa: D101

    pass


class ValidationError(RepositoryException):  # noqa: D101

    pass
