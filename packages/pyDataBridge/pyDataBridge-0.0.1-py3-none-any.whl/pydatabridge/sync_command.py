"""Synchronization command abstract class."""

from typing import Iterable

from .command import Command
from .data_access_adapter import DataAccessAdapter
from .sync_strategy import SyncStrategy

class SyncCommand(Command): # pylint: disable=too-few-public-methods
    """Handles syncrhonization execution."""

    def __init__(
        self,
        strategy: SyncStrategy,
        adapters: Iterable[DataAccessAdapter]
    ):
        self._strategy: SyncStrategy = strategy
        self._adapters: Iterable[DataAccessAdapter] = adapters

    def execute(self) -> None:
        """Executes the syncrhonization strategy.

        :returns: void

        """
        self._strategy.synchronize(self._adapters)
