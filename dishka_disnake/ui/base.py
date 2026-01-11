from typing import Any, Generic, TypeVar

from dishka_disnake.injector.wrap import wrap_injector


T = TypeVar("T")


class WrappedDishkaComponent(Generic[T]):
    async def callback(self, interaction: T, *args: Any, **kwargs: Any) -> None: ...

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)

        cb = cls.__dict__.get("callback")
        if cb is not None:
            cls.callback = wrap_injector(cb)
