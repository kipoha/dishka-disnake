from dishka_disnake.injector.wrap import wrap_injector


class WrappedDishkaItem:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cb = cls.__dict__.get("callback")
        if cb is not None:
            cls.callback = wrap_injector(cb)
