"""Core module."""

from abc import ABC, abstractmethod


class Command(ABC): # pylint: disable=too-few-public-methods
    """Represents an executable command abstraction."""

    @abstractmethod
    def execute(self) -> None:
        """Executes the command.
        :returns: None

        """
