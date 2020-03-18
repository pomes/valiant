"""Package exceptions."""


class RepositoryException(Exception):  # noqa: D101 # pragma: no cover

    pass


class PackageNotFoundException(RepositoryException):  # noqa: D101 # pragma: no cover

    pass


class ValidationError(RepositoryException):  # noqa: D101 # pragma: no cover

    pass
