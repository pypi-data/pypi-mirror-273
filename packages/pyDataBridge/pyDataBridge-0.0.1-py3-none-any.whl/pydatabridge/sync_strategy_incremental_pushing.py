"""Sync strategy."""

import logging
from copy import copy
from dataclasses import fields
from typing import Iterable, Any, Callable, Optional

from .services import SyncTimeManager, EntityAdapterIdIndexManager

from .sync_strategy_incremental import SyncStrategyIncremental
from .data_access_adapter import DataAccessAdapter
from .data_access_model import DataAccessModel
from .data_access_model_pointer import DataAccessModelPointer
from .data_access_criteria import DataAccessCriteria


class SyncStrategyIncrementalPushing(SyncStrategyIncremental):
    """Incremental pushing syncrhonization strategy.

    Performs syncrhonization relying on data provided by source data adapter
    which will be taken from the first adapter available.
    """
    def __init__(
        self,
        logger: logging.Logger,
        sync_time_manager: SyncTimeManager,
        id_index_manager: EntityAdapterIdIndexManager,
    ):
        """TODO: to be defined. """
        super().__init__(logger, sync_time_manager)

        self._id_index_manager: EntityAdapterIdIndexManager = id_index_manager

        self._data: Optional[Iterable[DataAccessModel]] = None

        self._source_adapters: Optional[Iterable[DataAccessAdapter]] = None
        self._dest_adapters: Optional[Iterable[DataAccessAdapter]] = None

    def _prepare(self) -> None:
        self._prepare_adapters()
        self._prepare_data()

    def _prepare_adapters(self) -> None:
        # NOTE: We could add support for mutiple soures programatically by
        # having a configuration that states which are sources and which are
        # destinies. By now we assume the first adapter is the source the rest
        # are dest adapters.
        self._source_adapters = [self._adapters[0]]
        self._dest_adapters = self._adapters[1:]

    def _prepare_data(self) -> None:
        self._data = []

        criteria = self._create_criteria_for_last_increment()

        for adapter in self._source_adapters:
            self._logger.info('Loading data from %s', adapter.provider_name)

            if self._check_status_of(adapter) is False:
                continue

            data = adapter.read(self.entity_name, criteria)
            self._data += self._map_to_local_entities(data, _from=adapter)
            self._logger.info('Loading data from %s - DONE', adapter.provider_name)

        self._logger.debug('Number of %s loaded: %d', self.entity_name, len(self._data))

    def _create_criteria_for_last_increment(self) -> DataAccessCriteria:
        # FIXME: Use dependency injection here
        return DataAccessCriteria.create_criteria_modified_or_created(since=self._last_sync_time)

    def _map_to_local_entities(
        self,
        entities: Iterable[DataAccessModel],
        _from: DataAccessAdapter
    ) -> Iterable[DataAccessAdapter]:
        return [self._map_to_local_entity(entity, _from) for entity in entities]

    def _map_to_local_entity(self, base_entity: DataAccessModel, _from: DataAccessAdapter):
        entity = copy(base_entity)
        adapter = _from

        _id = self._id_index_manager.get_local_id_for(entity, of=self.entity_name, _from=adapter)

        if _id is None and entity.id is not None:
            _id = self._create_local_id_for(entity, _from=adapter)

        entity.id = _id

        return self._map_attributes_of(entity, adapter, self._id_index_manager.get_local_id_for)

    def _synchronize(self) -> None:
        if not self._data:
            self._logger.info('There is nothing to be synced.')
            return

        if self._dry_run_mode_is_on:
            self._logger.info(
                'There are %d %s to be synced, disable dry-run to perform syncrhonization',
                len(self._data),
                self.entity_name
            )
            return

        self._save_data_into_dest_adapters()

    def _save_data_into_dest_adapters(self) -> None:
        for adapter in self._dest_adapters:
            self._logger.info('Saving data into %s', adapter.provider_name)

            if self._check_status_of(adapter) is False:
                continue

            self._save_data_into_dest_adapter(adapter)
            self._logger.info('Saving data into %s - DONE', adapter.provider_name)

    def _save_data_into_dest_adapter(self, adapter: DataAccessAdapter) -> None:
        data = self._generate_data_for(adapter)

        adapter_data = adapter.save(self.entity_name, data)

        self._create_adapter_local_ids_for(adapter_data, _from=adapter)

    def _generate_data_for(self, adapter):
        return [
            self._map_to_adapter_entity(item, adapter)\
            for item \
            in self._data
        ]

    # NOTE: Looks similar to `_map_to_local_entity` but have different intents.
    def _map_to_adapter_entity(
        self,
        base_entity: DataAccessModel,
        adapter: DataAccessAdapter
    ) -> DataAccessModel:
        entity = copy(base_entity)

        adapter_id = self._id_index_manager.get_adapter_id_for(
            entity,
            of=self.entity_name,
            _from=adapter
        )

        # Control properties
        entity.local_id = entity.id
        entity.is_new_on_adapter = adapter_id is None

        entity.id = adapter_id

        return self._map_attributes_of(entity, adapter, self._id_index_manager.get_adapter_id_for)

    def _create_adapter_local_ids_for(
        self,
        data: Iterable[DataAccessModel],
        _from: DataAccessAdapter
    ):
        for entity in data:
            if entity.is_new_on_adapter is not True:
                continue

            self._create_local_id_for(entity, _from)

    def _create_local_id_for(
        self,
        entity: DataAccessModel,
        _from: DataAccessAdapter
    ):
        if self._dry_run_mode_is_on:
            return None

        try:
            return self._id_index_manager.save_id_for(
                entity,
                self.entity_name,
                _from,
                entity.local_id if hasattr(entity, 'local_id') else None
            )
        except Exception as e: # pylint: disable=broad-exception-caught
            self._logger.exception(e)

        return None

    def _map_attributes_of(
        self,
        entity: DataAccessModel,
        adapter: DataAccessAdapter,
        id_provider: Callable
    ) -> DataAccessModel:
        for field in fields(entity):
            attr = getattr(entity, field.name)
            setattr(entity, field.name, self._map_attribute(attr, adapter, id_provider))

        return entity

    def _map_attribute(self, attr: Any, adapter: DataAccessAdapter, id_provider: Callable) -> Any:
        if isinstance(attr, DataAccessModelPointer):
            return self._map_to_pointer(attr, adapter, id_provider)

        if isinstance(attr, list):
            if isinstance(attr[0], DataAccessModelPointer):
                return [self._map_to_pointer(p, adapter, id_provider) for p in attr]

            if isinstance(attr[0], DataAccessModel):
                return [self._map_attributes_of(e, adapter, id_provider) for e in attr]

        return attr

    def _map_to_pointer(
        self,
        base_pointer: DataAccessModelPointer,
        adapter: DataAccessAdapter,
        id_provider: Callable
    ) -> DataAccessModelPointer:
        pointer = copy(base_pointer)

        pointer.id = id_provider(pointer, of=pointer.collection_name, _from=adapter)

        return pointer

    def _check_status_of(self, adapter: DataAccessAdapter) -> bool:
        adapter_status = adapter.check_status()

        if adapter_status is True:
            self._logger.info('Adapter status is OK: %s', adapter.provider_name)
        else:
            self._logger.warning('Adapter status is NOT OK: %s', adapter.provider_name)

        return adapter_status
