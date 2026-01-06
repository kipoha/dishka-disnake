from dishka import AsyncContainer

from dishka_disnake.state_management import State


def setup_dishka(container: AsyncContainer) -> None:
    """
    Setup dishka for disnake
    """
    State.container = container
    State.sync_container = container
