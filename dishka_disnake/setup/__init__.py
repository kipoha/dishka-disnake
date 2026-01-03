from dishka import AsyncContainer

from dishka_disnake.state_management import state


def setup_dishka(container: AsyncContainer) -> None:
    state.container = container
