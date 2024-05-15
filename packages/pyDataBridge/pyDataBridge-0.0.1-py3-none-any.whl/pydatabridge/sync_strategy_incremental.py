"""Sync strategy module."""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .services import SyncTimeManager

from .data_access_adapter import DataAccessAdapter
from .sync_strategy import SyncStrategy


class SyncStrategyIncremental(SyncStrategy, ABC):
    """Incremental sync strategy."""

    @property
    def supports_dry_run(self) -> bool:
        return True

    def __init__(self, logger: logging.Logger, sync_time_manager: SyncTimeManager):
        super().__init__()

        self._logger = logger
        self._sync_time_manager: SyncTimeManager = sync_time_manager

        self._last_sync_time = self._sync_time_manager.get_last_for(self.entity_name)

        self._adapters: Iterable[DataAccessAdapter] = None
        self._new_last_sync_time = None

    def synchronize(self, adapters: Iterable[DataAccessAdapter]) -> None:
        self._logger.info('Performing synchronization of `%s` entity.', self.entity_name)

        if not adapters or len(adapters) < 2:
            self._logger.error('Not enough adapters to perform synchronizaton')
            return

        self._adapters = adapters

        self._prepare()
        self._new_last_sync_time = datetime.now()

        self._synchronize()
        self._save_new_last_sync_time()

    def _save_new_last_sync_time(self) -> None:
        if self._dry_run_mode_is_on:
            return

        self._sync_time_manager.log_for(self.entity_name, self._new_last_sync_time)

    @abstractmethod
    def _prepare(self):
        """Prepare a snapshot for the information to be synced.

        The last_sync_time will be set after preparation, this way we avoid
        ignoring changes performed while synchronization process is running."""

    @abstractmethod
    def _synchronize(self):
        """Persists spnapshotted data on the adapters."""
