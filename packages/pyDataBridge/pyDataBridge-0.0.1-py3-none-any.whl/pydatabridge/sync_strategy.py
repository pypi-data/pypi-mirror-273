"""Defines the syncrhonization strategy base interface."""

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .data_access_adapter import DataAccessAdapter

class SyncStrategy(ABC):
    """Defines the interface to run a data syncrhonization process."""

    @property
    def supports_dry_run(self) -> bool:
        """Whether the strategy can be executed in dry-run mode for.

        """
        return False

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """Name of the entity managed."""

    @property
    def depends_on(self) -> Optional[str]:
        """Name of the entity this strategy depends on to be already synced.
        :returns: TODO

        """
        return None

    def __init__(self):
        self._dry_run_mode_is_on = False

    @abstractmethod
    def synchronize(self, adapters: Iterable[DataAccessAdapter]) -> None:
        """Performs the data syncrhonization process.

        Syncrhonizes the data for the given adapters. Each concrete
        implementations defines which and how data is synchronized.

        :adapters: The adapters to be synchronized.
        :returns: none

        """

    def set_dry_run_mode_is_on(self, is_enabled: bool) -> None:
        """Tells the strategy whether to run in dry run mode.

        :is_enabled: bool
        :returns: void

        """
        self._dry_run_mode_is_on = is_enabled
