"""Services module."""

from typing import Optional, Iterable
from pypika import SQLLiteQuery, Criterion, Field # type: ignore

from ..data_access_model import DataAccessModel
from ..data_access_adapter import DataAccessAdapter

class EntityAdapterIdIndexManager():
    """Manages id mapping of entities from different adapters."""
    _table_name = 'adapter_entity_id'

    def __init__(self, db, logger_provider):
        self._db = db
        self._logger = logger_provider(self.__class__.__name__)

        self._initialize_db()

    def save_id_for(
        self,
        entity: DataAccessModel,
        of: str,
        _from: DataAccessAdapter,
        _id: int = None
    ) -> str:
        """Creates or Updates the id for the entity.

        :entity: DataAccessModel The entity whose id is being mapped.
        :of: str The collection whose entity belongs to.
        :_from: DataAccessAdapter The adapter whose id is from.
        :_id: Local id if any.

        :return: str The local id.

        """
        collection_name = of
        adapter_name = _from.provider_name

        self._logger.debug(
            'Creating entity\'s id of %s (%s) for: "%s" `%s`',
            collection_name,
            _id,
            adapter_name,
            entity
        )

        query = self._build_insert_query(collection_name, adapter_name, entity.id, _id)
        self._execute(query, and_commit=True)

        if _id is not None:
            return _id

        _id = self._get_local_id_for(entity.id, collection_name, adapter_name)

        self._logger.debug('Entity\'s id index saved with local id "%s"', _id,)

        return _id

    def get_local_id_for(
        self,
        entity: DataAccessModel,
        of: str,
        _from: DataAccessAdapter
    ) -> Optional[str]:
        """Retrieve the id for the entity.

        :entity: DataAccessModel The entity whose id is being mapped.
        :of: str The collection whose entity belongs to.
        :_from: DataAccessAdapter The adapter whose id is from.

        :return: str The local id.

        """
        collection_name = of
        adapter_name = _from.provider_name

        _id = self._get_local_id_for(entity.id, collection_name, adapter_name)
        self._logger.debug('Entity id loaded: "%s-%s" for `%s`', adapter_name, _id, entity)

        return _id

    def get_adapter_id_for(
        self,
        entity: DataAccessModel,
        of: str,
        _from: DataAccessAdapter
    ) -> Optional[str]:
        """Gets the adapter id for a particular entity.

        :entity: DataAccessModel The entity whose id is being mapped.
        :of: str The collection whose entity belongs to.
        :_from: DataAccessAdapter The adapter whose id is from.

        :returns: str The adapter entity id.

        """
        collection_name = of
        adapter_name = _from.provider_name

        query = self._build_select_adapter_id_query(collection_name, adapter_name, entity.id)
        cursor = self._execute(query)
        result = cursor.fetchone()
        _id = result[0] if result else None

        self._logger.debug('Adapter entity id loaded: "%s-%s" for `%s`', adapter_name, _id, entity)

        return _id


    def _get_local_id_for(
        self,
        entity_id: str,
        collection_name: str,
        adapter_name: str
    ) -> Optional[str]:
        query = self._build_select_local_id_query(collection_name, adapter_name, entity_id)
        cursor = self._execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    def _build_insert_query(
        self,
        collection_name: str,
        adapter_name: str,
        entity_id: str,
        _id: str = None
    ) -> SQLLiteQuery:
        return SQLLiteQuery\
            .into(self._table_name)\
            .columns(
                'collection_name',
                'entity_id',
                'adapter_name',
                'adapter_entity_id',
            ).insert(
                collection_name,
                _id,
                adapter_name,
                entity_id,
            )

    def _build_select_local_id_query(
        self,
        collection_name: str,
        adapter_name: str,
        adapter_entity_id: str
    ) -> SQLLiteQuery:
        return self._build_select_query_base(collection_name, adapter_name)\
            .select('entity_id')\
            .where(
                Field('adapter_entity_id') == adapter_entity_id,
            )

    def _build_select_adapter_id_query(
        self,
        collection_name: str,
        adapter_name: str,
        entity_id: str
    ) -> SQLLiteQuery:
        return self._build_select_query_base(collection_name, adapter_name)\
            .select('adapter_entity_id')\
            .where(
                Field('entity_id')       == entity_id,
            )

    def _build_select_query_base(self, collection_name: str, adapter_name: str) -> SQLLiteQuery:
        return SQLLiteQuery\
            .from_(self._table_name)\
            .where(
                Criterion.all([
                    Field('collection_name') == collection_name,
                    Field('adapter_name')    == adapter_name,
                ])
            )

    def _initialize_db(self):
        self._create_table()
        self._create_indexes()
        self._create_triggers()

    def _create_table(self):
        query = SQLLiteQuery\
            .create_table(self._table_name)\
            .if_not_exists()\
            .columns(
                ('collection_name',   'TEXT NOT NULL'),
                ('entity_id',         'INTEGER'),
                ('adapter_name',      'TEXT NOT NULL'),
                ('adapter_entity_id', 'TEXT NOT NULL'),
            ).primary_key(
                'collection_name',
                'adapter_name',
                'entity_id',
            )

        self._logger.debug('Initializing service table:\n\t`%s`', query)

        self._execute(query)

    def _create_indexes(self):
        query = SQLLiteQuery\
            .create_index(f'{self._table_name}_adapter_entity_id_idx')\
            .on(self._table_name)\
            .if_not_exists()\
            .columns(
                'collection_name',
                'adapter_name',
                'adapter_entity_id',
            )

        self._logger.debug('Creating service table indexes:\n\t`%s`', query)

        self._execute(query)

    def _create_triggers(self):
        trigger_name = 'set_entity_id_after_insert'
        query = f"""
        CREATE TRIGGER IF NOT EXISTS {self._table_name}_{trigger_name}
        AFTER INSERT ON {self._table_name}
        WHEN (NEW.entity_id IS NULL)
        BEGIN
            UPDATE {self._table_name}
            SET
                entity_id = (
                    SELECT IFNULL(MAX(entity_id), -1) + 1
                    FROM adapter_entity_id
                    WHERE collection_name = NEW.collection_name
                )
            WHERE
                rowid = NEW.rowid;
        END;
        """

        self._logger.debug('Creating service table triggers:\n\t`%s`', query)

        self._execute(query)

    def _execute(self, query: SQLLiteQuery, and_commit: bool = False) -> Iterable[tuple]:
        self._logger.debug('Performing query: `%s`', query)

        cursor = self._db.cursor()
        cursor.execute(str(query))

        if and_commit is True:
            cursor.connection.commit()

        return cursor
