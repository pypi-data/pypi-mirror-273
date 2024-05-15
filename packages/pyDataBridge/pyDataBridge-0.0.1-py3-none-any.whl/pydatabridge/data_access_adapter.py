"""Data access module."""

import logging
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Union

from .data_access_model import DataAccessModel
from .data_access_criteria import DataAccessCriteria

class DataAccessAdapter(ABC):
    """Defines the interface for data access adapters.

    We use `Iterables` of data for simplicity since we cannot asume how the data
    would be handled by the adapter since it could be batched or by item.

    To implement a new adapter you have to extend this class and implement CRUD
    methods for any supported entity. I.e, let's assume we create a new adapter
    that supports access for reading `products` , reading and writing `clients`
    and creating and deleting `orders`, then we have to define next methods:

    * `_read_products  ( self, criteria: DataAccessCriteria    )  -> Iterable[DataAccessModel]`
    * `_read_clients   ( self, criteria: DataAccessCriteria    )  -> Iterable[DataAccessModel]`
    * `_create_clients ( self, data: Iterable[DataAccessModel] )  -> Iterable[DataAccessModel]`
    * `_update_clients ( self, data: Iterable[DataAccessModel] )  -> Iterable[DataAccessModel]`
    * `_create_orders  ( self, data: Iterable[DataAccessModel] )  -> Iterable[DataAccessModel]`
    * `_delete_orders  ( self, criteria: DataAccessCriteria    )  -> Iterable[DataAccessModel]`

    NOTE: Entities required depends on syncrhonization strategies.

    Not implemented actions on a particular entity being call will fall into an
    empty list and a warning on the log, this way we avoid the whole system
    failling.

    Every single method must return an iterable containing the data being
    accessed, both for reading or writing/deleting.
    """

    @property
    @abstractmethod
    def provider_name(self):
        """Name that identifies the adapter.
        :returns: str

        """

    def __init__(
        self,
        configuration,
        logger_provider,
    ):

        self._configuration = configuration["adapters"][self.provider_name]
        self._logger: logging.Logger = logger_provider(
            f"{self.__class__.__name__}",
        )
        self.initialize()

    @abstractmethod
    def initialize(self):
        """ Initializes the adapter after construction.

        This method could be used to create database connection, configure API
        connections, etc.

        `initialize()` is called after `__init__()`.
        """

    @abstractmethod
    def check_status(self) -> bool:
        """Health check method.

        :return: bool Whether the adapter is ready and set-up.
        """

    def read(
        self,
        collection_name: str,
        criteria: Optional[DataAccessCriteria] = None
    ) -> Iterable[DataAccessModel]:
        """Reads data from collection based on the given criteria.

        :collection_name: str Collection to extrat data from.
        :criteria: DataAccessCriteria Criteria to filter data.
        :returns: Iterable[DataAccessModel] The result data.

        """
        return self._perform('read', on=collection_name, _with=criteria)

    def create(
        self,
        collection_name: str,
        data: Iterable[DataAccessModel]
    ) -> Iterable[DataAccessModel]:
        """Stores the new data for the given collection.

        :collection_name: str Collection to create data in.
        :data: Itarable[DataAccessModel] Data to be created.
        :returns: Iterable[DataAccessModel] The created data.

        """
        return self._perform('create', on=collection_name, _with=data)

    def update(
        self,
        collection_name: str,
        data: Iterable[DataAccessModel]
    ) -> Iterable[DataAccessModel]:
        """Updates already existing data in the collection.

        :collection_name: str Collection to update data in.
        :data: Itarable[DataAccessModel] Data to be updated.
        :returns: Iterable[DataAccessModel] The updated data.

        """
        return self._perform('update', on=collection_name, _with=data)

    def delete(
        self,
        collection_name: str,
        criteria: Optional[DataAccessCriteria] = None
    ) -> Iterable[DataAccessModel]:
        """Deletes given data based on the criteria.

        NOTE: Deletion is not garanteed to be physical.

        :collection_name: str Collection to delete data from.
        :criteria: DataAccessCriteria Criteria to filter data to be deleted.
        :returns: Iterable[DataAccessModel] The deleted data.

        """
        return self._perform('delete', on=collection_name, _with=criteria)

    def save(
        self,
        collection_name: str,
        data: Iterable[DataAccessModel]
    ) -> Iterable[DataAccessModel]:
        """Helper method to simplify data saving.

        Based on the existance of the data uses create or update.

        :collection_name: str Collection to extrat data from.
        :collection_name: TODO
        :data: TODO
        :returns: TODO

        """

        to_be_created = []
        to_be_updated = []
        saved = []

        for item in data:
            if self._is_new(collection_name, item):
                to_be_created.append(item)
            else:
                to_be_updated.append(item)

        if to_be_created:
            saved += self.create(collection_name, to_be_created)

        if to_be_updated:
            saved += self.update(collection_name, to_be_updated)

        return saved

    def _is_new(
        self,
        collection_name: str,
        data_item: DataAccessModel
    ) -> bool:
        """Chechs whether the element exists.

        This method can be reimplemented to change the verification strategy.

        :collection_name: str Collection to check data existance against.
        :data_item: DataAccessModel The item to be checked.
        :returns: bool Whether the element exists or not.

        """
        return collection_name and data_item.id is None

    def _perform(
        self,
        action: str,
        on: str,
        _with: Union[DataAccessCriteria, Iterable[DataAccessModel]]
    ) -> Iterable[DataAccessModel]:
        try:
            method = getattr(self, f'_{action}_' + on)
            return method(_with)
        except AttributeError as _e:
            if type(self).__name__ not in str(_e):
                raise _e

            self._warn_not_implemented(action, on)
            return []

    def _warn_not_implemented(self, method_name, entity_name = '') -> None:
        self._logger.warning(
            '`%s(%s)` is not implemented in %s adapter!',
            method_name,
            entity_name,
            self.provider_name
        )
