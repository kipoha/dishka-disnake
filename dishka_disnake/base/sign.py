import inspect

from typing import Callable

from dishka_disnake.base.checkers import is_disnake_annotation


def rebuild_signature(func: Callable) -> inspect.Signature:
    sig = inspect.signature(func)
    params = []

    params_ = sig.parameters.items()
    for _, param in params_:
        if param.name == "self":
            params.append(param)
            continue

        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            params.append(param)
            continue

        if is_disnake_annotation(param.annotation):
            params.append(param)
            continue

    return sig.replace(parameters=params)
