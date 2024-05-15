"""Application module."""

import logging
from typing import Sequence, Iterable
from dependency_injector.wiring import inject, Provide

from .command_queue_invoker import CommandQueueInvoker
from .data_access_adapter import DataAccessAdapter
from .sync_command import SyncCommand
from .sync_strategy import SyncStrategy
from .services import Services, DependencySorter


@inject
class App:
    """Application controller."""

    def __init__(
        self,
        logger_provider = Provide[Services.LoggerProvider.provider],
        dependency_sorter: DependencySorter = Provide[Services.StrategiesDependencySorter],
        **kwargs
    ):
        """Creates the application instance."""
        self._logger: logging.Logger = logger_provider(self.__class__.__name__)
        self._strategies_dependency_sorter = dependency_sorter

        self._adapters = []
        self._strategies = []

        self._is_dry_run: bool = kwargs.get('dry_run', False)

        self._command_invoker: CommandQueueInvoker = CommandQueueInvoker()

    def __new__(cls, **kwargs):
        """Ensures singleton pattern for the application."""
        return cls.get_instance()

    def run(self) -> int:
        """Runs the application."""
        self._populate_command_queue()

        self._logger.info('Running commands.')

        if self._is_dry_run:
            self._logger.warning('dry_run mode ON.')

        try:
            self._command_invoker.execute_commands()
        except Exception as exception: # pylint: disable=broad-exception-caught
            self._handle_exception(exception)
            return 1

        return 0

    def get_is_dry_run(self) -> bool:
        """Whether the execution is dry run.
        :returns: bool

        """
        return self._is_dry_run

    def set_adapters(self, adapters: Sequence[DataAccessAdapter]) -> None:
        """Sets adapters for the app running.

        :adapters: Sequence[DataAccessAdapter]
        :returns: void

        """
        self._adapters = adapters

    def set_strategies(self, strategies: Iterable[SyncStrategy]) -> None:
        """Sets strategies for the app running.

        :strategies: Iterable[SyncStrategy]
        :returns: void

        """
        self._strategies = strategies

    def _populate_command_queue(self) -> None:
        """Iterates over the strategies and creates the respective commnads.

        We assume master to be the first adapter found. Prefixing the name of
        the master with underscore (`_`) ensures its module to be loaded first.

        :returns: void

        """
        if len(self._adapters) < 2:
            self._logger.warning('Nothing to do. Not enough adapters.')
            return
        if not self._strategies:
            self._logger.warning('Nothing to do. There are not strategies.')
            return

        self._logger.debug('Populating sync command queue.')

        strategies = self._strategies_dependency_sorter.sort(self._strategies)

        for strategy in strategies:
            if self._is_dry_run and not strategy.supports_dry_run:
                self._logger.warning('Dry-run not supported by %s', type(strategy).__name__)
                continue

            strategy.set_dry_run_mode_is_on(self._is_dry_run)
            command = SyncCommand(strategy, self._adapters)

            self._command_invoker.add(command)

    def _handle_exception(self, exception) -> None:
        """Handles an exception.

        :exception: Exception
        :returns: void

        """
        self._logger.exception(exception)

    @classmethod
    def get_instance(cls) -> "App":
        """Gets the singleton instance of the application."""

        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)

        return cls._instance
