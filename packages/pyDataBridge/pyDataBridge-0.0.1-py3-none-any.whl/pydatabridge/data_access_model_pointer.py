"""Data access module."""

from dataclasses import dataclass

from .data_access_model import DataAccessModel


@dataclass
class DataAccessModelPointer(DataAccessModel):
    """Defines a related entity."""

    collection_name: str
