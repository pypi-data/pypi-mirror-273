"""Services module."""

from datetime import datetime
from pypika import SQLLiteQuery, Field, Order


class SyncTimeManager():
    """Manages status of sync processes."""

    _table_name = 'sync_times'

    def __init__(self, db, logger_provider):
        self._db = db
        self._logger = logger_provider(self.__class__.__name__)

        self._initialize_db()

    def log_for(self, entity: str, timestamp: datetime) -> None:
        """Logs a new sync status for specified entity.

        :param entity: str - The entity for which to log the sync status
        """
        query = SQLLiteQuery\
            .into(self._table_name)\
            .columns(
                'entity',
                'timestamp'
            ).insert(
                entity,
                timestamp
            )

        cursor = self._db.cursor()
        cursor.execute(str(query))
        self._db.commit()

        self._logger.debug('New sync time created for %s: %s', entity, timestamp)

    def get_last_for(self, entity: str) -> datetime:
        """Get the timestamp of the last sync process for specified entity.

        :param entity: str - The entity for which to retrieve the last sync timestamp
        :returns: datetime - The timestamp of the last sync
        """
        query = SQLLiteQuery\
            .from_(self._table_name)\
            .select('timestamp')\
            .where(Field('entity') == entity)\
            .orderby('timestamp', order=Order.desc)\
            .limit(1)

        cursor = self._db.cursor()
        cursor.execute(str(query))

        result = cursor.fetchone()
        sync_time = datetime.fromisoformat(result[0]) if result else None

        if not sync_time:
            self._logger.debug('No sync time loaded for %s', entity)
        else:
            self._logger.debug('Sync time loaded for %s: %s', entity, sync_time)

        return sync_time

    def _initialize_db(self):
        self._create_table()
        self._create_indexes()

    def _create_table(self):
        query = SQLLiteQuery\
            .create_table(self._table_name)\
            .if_not_exists()\
            .columns(
                ('id',              'INTEGER PRIMARY KEY AUTOINCREMENT'),
                ('entity',          'TEXT NOT NULL'),
                ('timestamp',       'DATETIME DEFAULT CURRENT_TIMESTAMP'),
                ('additional_info', 'TEXT'),
            )

        self._logger.debug('Initializing service table:\n\t`%s`', query)

        cursor = self._db.cursor()
        cursor.execute(str(query))

    def _create_indexes(self):
        query = SQLLiteQuery\
            .create_index(f'{self._table_name}_entity_idx')\
            .on(self._table_name).\
            if_not_exists()\
            .columns('entity')

        self._logger.debug('Creating service table indexes:\n\t`%s`', query)

        cursor = self._db.cursor()
        cursor.execute(str(query))
