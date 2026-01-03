from typing import Any

from dishka_disnake.base.singleton import SingletonClass


class _State(SingletonClass):
    def __init__(self) -> None:
        self.__dict__["_store"] = {}

    def __getattr__(self, item) -> Any:
        return self._store.get(item, None)

    def __setattr__(self, key, value) -> None:
        self._store[key] = value


state = _State()
