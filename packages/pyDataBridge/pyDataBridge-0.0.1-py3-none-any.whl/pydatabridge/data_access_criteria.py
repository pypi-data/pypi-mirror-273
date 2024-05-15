"""Data access module."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DataAccessCriteria:
    """Defines a criteria to filter data.

    SUBJECT FOR FUTURE REWORK.

    The implementation is very simple and is designed for actual filters
    required by the sistem. Some rework needs to be done to improve criteria
    handling.

    NOTE_0: Review the design and reimplementation before adding new filters.
    NOTE_1: Not designed for complex filters.
    """

    modified_or_created_since: Optional[datetime] = None

    @staticmethod
    def create_criteria_modified_or_created(since: datetime) -> "DataAccessCriteria":
        """Creates a criteria with a modified-since filter.

        :since: datetime
        :returns: DataAccessCriteria

        """
        return DataAccessCriteria(modified_or_created_since = since)
