from typing import Self


class SingletonClass:
    _instance: Self | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
