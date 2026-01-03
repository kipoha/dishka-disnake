from dishka import AsyncContainer

from dishka_disnake.state_management import state

from src.core import logger


def setup_dishka(container: AsyncContainer) -> None:
    logger.debug("Setting up dishka...")
    state.container = container
