from typing import Any


def sigterm_handler(_signo: Any, _stack_frame: Any) -> None:
    raise KeyboardInterrupt()
