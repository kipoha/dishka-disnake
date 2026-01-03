import inspect
import builtins
from typing import Callable, get_origin, get_args

from dishka_disnake import inject


def is_builtin_type(tp: object) -> bool:
    return tp in vars(builtins).values()


def is_disnake_type(tp: object) -> bool:
    return isinstance(tp, type) and tp.__module__.startswith("disnake")


def is_disnake_annotation(annotation: object) -> bool:
    if annotation is inspect.Parameter.empty:
        return False

    origin = get_origin(annotation)
    if origin is not None:
        return is_disnake_annotation(origin) or any(
            is_disnake_annotation(arg) for arg in get_args(annotation)
        )

    return is_builtin_type(annotation) or is_disnake_type(annotation)


def rebuild_signature(func: Callable) -> inspect.Signature:
    sig = inspect.signature(func)
    params = []

    params_ = sig.parameters.items()
    params_2 = []
    for key, param in params_:
        if param.name == "self":
            params.append(param)
            params_2.append((key, param))
            continue

        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            params.append(param)
            params_2.append((key, param))
            continue

        if is_disnake_annotation(param.annotation):
            params.append(param)
            params_2.append((key, param))
            continue

    return sig.replace(parameters=params)


def wrap_callback(
    func: Callable,
) -> Callable:
    wrapped = inject(func)

    wrapped.__signature__ = rebuild_signature(func)  # type: ignore

    if hasattr(wrapped, "__wrapped__"):
        del wrapped.__wrapped__  # type: ignore

    return wrapped
