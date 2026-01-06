from typing import Any

from disnake import MessageInteraction

from dishka_disnake.injector.wrap import wrap_injector


class WrappedDishkaItem:
    async def callback(self, interaction: MessageInteraction, *args: Any, **kwargs: Any) -> None: ...

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)

        cb = cls.__dict__.get("callback")
        if cb is not None:
            cls.callback = wrap_injector(cb)
