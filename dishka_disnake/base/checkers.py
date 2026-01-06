import inspect
import builtins

from typing import get_origin, get_args


def is_builtin_type(tp: object) -> bool:
    return tp in vars(builtins).values()


def is_disnake_type(tp: object) -> bool:
    return isinstance(tp, type) and tp.__module__.startswith("disnake")


def is_dishka_disnake_type(tp: object) -> bool:
    return isinstance(tp, type) and tp.__module__.startswith("dishka_disnake")


def is_disnake_annotation(annotation: object) -> bool:
    if annotation is inspect.Parameter.empty:
        return False

    origin = get_origin(annotation)
    if origin is not None:
        return is_disnake_annotation(origin) or any(
            is_disnake_annotation(arg) for arg in get_args(annotation)
        )

    return (
        is_builtin_type(annotation)
        or is_disnake_type(annotation)
        or is_dishka_disnake_type(annotation)
    )


def is_dependency(annotation: object) -> bool:
    if annotation is inspect.Parameter.empty:
        return False

    origin = get_origin(annotation)
    if origin is not None:
        return any(is_dependency(arg) for arg in get_args(annotation))

    return not (
        is_builtin_type(annotation)
        or is_disnake_type(annotation)
        or is_dishka_disnake_type(annotation)
    )
