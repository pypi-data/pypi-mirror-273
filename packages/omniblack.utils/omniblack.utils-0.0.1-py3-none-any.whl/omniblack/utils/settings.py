from os import environ, makedirs, path
from pathlib import Path
from typing import Annotated

from public import public
from pydantic import BaseModel, ValidationError
from pydantic import AnyUrl, UrlConstraints

settings_errors = {}


def get_var(var_name, *, optional=False):
    var_key = var_name.upper()

    if var_key not in environ:
        if not optional:
            settings_errors[var_key] = KeyError(f"'{var_key}' is not set.")

        return None
    else:
        return environ[var_key]


@public
def get_int(var_name, *, optional=False):
    if var_value := get_var(var_name, optional=optional):
        try:
            return int(var_value, 10)
        except ValueError as err:
            if not optional:
                settings_errors[var_name.upper()] = err
            return None


@public
def get_path(var_name, *, optional=False):
    path = get_var(var_name, optional=optional)

    if path := get_var(var_name, optional=optional):
        return Path(path)


@public
def get_dir_path(var_name, *, optional=False):
    if dir_path := get_var(var_name, optional=optional):
        makedirs(dir_path, exist_ok=True)

        if not path.isdir(dir_path):
            if not optional:
                settings_errors[var_name.upper()] = NotADirectoryError(
                    f"'{var_name}' must be a directory",
                )

            return None

        return Path(dir_path)
    else:
        return None


HttpsUrl = Annotated[
    AnyUrl,
    UrlConstraints(
        max_length=2083,
        allowed_schemes=['https'],
    ),
]


class Url(BaseModel):
    url: HttpsUrl


@public
def get_url(var_name, *, optional=False):
    if url := get_var(var_name, optional=optional):
        try:
            Url(url=url)
        except ValidationError as err:
            if not optional:
                settings_errors[var_name.upper()] = err
            return None

        return url


@public
def raise_for_settings():
    if settings_errors:
        raise BaseExceptionGroup(
            'There are configuration problems with artifact_server.',
            list(settings_errors.values()),
        )
