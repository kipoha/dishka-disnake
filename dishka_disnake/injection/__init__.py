import inspect

from typing import Callable, TypeVar, ParamSpec, Coroutine, Any, get_origin

from functools import wraps

from dishka import AsyncContainer
from dishka.exceptions import NoFactoryError

from dishka_disnake.state_management import state


__all__ = ["inject", "inject_loose"]

P = ParamSpec("P")
R = TypeVar("R")


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
        container: AsyncContainer | None = state.container
        sig = inspect.signature(func)


        if container is None:
            raise RuntimeError("Container is not initialized, setup dishka first")

        async with container() as c:
            params = sig.parameters.items()
            for name, param in params:
                if name in kwargs or param.annotation is inspect._empty:
                    continue

                param_type = param.annotation

                if get_origin(param_type) is not None:
                    continue

                try:
                    kwargs[name] = await c.get(param_type)
                except NoFactoryError:
                    pass

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
