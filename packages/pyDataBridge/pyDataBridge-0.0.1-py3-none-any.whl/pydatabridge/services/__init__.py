"""Services DI Container."""

import sqlite3
import logging.config
import logging
from dependency_injector import containers, providers

from .dependency_sorter import DependencySorter
from .sync_time_manager import SyncTimeManager
from .entity_adapter_id_index_manager import EntityAdapterIdIndexManager


class Services(containers.DeclarativeContainer): # pylint: disable=too-few-public-methods
    """Services DI Container."""

    Configuration = providers.Configuration(json_files=["config.json"])

    Logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
        defaults= providers.Factory(lambda config : {
            "level": "INFO" if config["environment"] == "production" else "DEBUG"
        }, Configuration)
    )

    LoggerProvider = providers.Factory(
        logging.getLogger
    )

    DBConnection = providers.Factory(
        sqlite3.Connection,
        database=Configuration.app.db_path,
    )

    SyncTimeManager = providers.Singleton(
        SyncTimeManager,
        db=DBConnection,
        logger_provider=LoggerProvider.provider
    )

    EntityAdapterIdIndexManager = providers.Singleton(
        EntityAdapterIdIndexManager,
        db=DBConnection,
        logger_provider=LoggerProvider.provider
    )

    StrategiesDependencySorter = providers.Factory(
        DependencySorter,
        entity_attr='entity_name',
        depends_attr='depends_on'
    )
