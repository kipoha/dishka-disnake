from typing import Callable

from dishka_disnake import inject
from dishka_disnake.base.sign import rebuild_signature


def wrap_injector(
    func: Callable,
) -> Callable:
    wrapped = inject(func)

    wrapped.__signature__ = rebuild_signature(func)  # type: ignore

    if hasattr(wrapped, "__wrapped__"):
        del wrapped.__wrapped__  # type: ignore

    return wrapped
