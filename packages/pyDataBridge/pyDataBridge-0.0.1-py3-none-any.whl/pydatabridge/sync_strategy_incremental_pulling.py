"""Sync strategy."""

from .sync_strategy_incremental_pushing import SyncStrategyIncrementalPushing


class SyncStrategyIncrementalPulling(SyncStrategyIncrementalPushing):
    """Sync strategy incremental pulling"""
    def _prepare_adapters(self) -> None:
        self._source_adapters = self._adapters[1:]
        self._dest_adapters = [self._adapters[0]]
