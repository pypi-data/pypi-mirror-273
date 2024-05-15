"""Data access module."""

from dataclasses import dataclass


@dataclass()
class DataAccessModel:
    """DataAccessModel base class."""

    id: str
