from ingryd.logging import init
init()

from ._app import create_app  # noqa: E402


__all__ = [
    'create_app',
]
