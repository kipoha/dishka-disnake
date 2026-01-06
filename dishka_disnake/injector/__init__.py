import inspect

from typing import (
    Callable,
    TypeVar,
    ParamSpec,
    Coroutine,
    Any,
    Annotated,
    get_origin,
    get_args,
)

from functools import wraps

from dishka import AsyncContainer, FromDishka

from dishka_disnake.state_management import State
from dishka_disnake.base.checkers import is_dependency


__all__ = ["inject", "inject_loose"]

P = ParamSpec("P")
R = TypeVar("R")


def extract_fromdishka(annotation):
    origin = get_origin(annotation)

    if origin is Annotated:
        base, *metadata = get_args(annotation)
        for meta in metadata:
            mod = getattr(meta, "__module__", "")
            if mod.startswith("dishka") or mod.startswith("dishka_disnake"):
                return base
    elif origin is FromDishka:
        return get_args(annotation)[0]

    return None


def inject(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    """
    decorator: accepts any async function (arguments not strict),
    but preserves the return type R.
    """
    if not inspect.iscoroutinefunction(func):
        raise TypeError(
            f"@inject can be applied only to async functions: {func.__name__}"
        )

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        container: AsyncContainer | None = State.container
        sig = inspect.signature(func)

        if container is None:
            raise RuntimeError("Container is not initialized, setup dishka first")

        async with container() as c:
            params = sig.parameters.items()
            for name, param in params:
                if name in kwargs or param.annotation is inspect._empty:
                    continue

                annotation = param.annotation

                dep_type = extract_fromdishka(annotation)
                if dep_type is not None:
                    kwargs[name] = await c.get(dep_type)
                    continue

                if is_dependency(annotation):
                    kwargs[name] = await c.get(annotation)
                    continue

            return await func(*args, **kwargs)

    return async_wrapper


def inject_loose(
    func: Callable[..., Coroutine[Any, Any, R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    Loose decorator: accepts any async function (arguments not strict),
    but preserves the return type R.
    Delegates to the real `inject` implementation.
    """
    return inject(func)
