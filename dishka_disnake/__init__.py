"""
Disnake mini library with Dishka integration

Example:
```py
from dishka_disnake.commands import slash_command

@slash_command()
async def foo(inter: AppCmdInter, *, usecase: UserUsecase):
    await usecase.do_something()
```
"""

__version__ = "0.1.0"
__author__ = "kipoha"


from dishka_disnake.injection import inject, inject_loose
from dishka_disnake.setup import setup_dishka

__all__ = [
    "inject",
    "inject_loose",
    "setup_dishka",
]
