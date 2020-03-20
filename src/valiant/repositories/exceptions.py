"""Package exceptions."""


class RepositoryException(Exception):  # noqa: D101

    pass


class PackageNotFoundException(RepositoryException):  # noqa: D101

    pass


class ValidationError(RepositoryException):  # noqa: D101

    pass
