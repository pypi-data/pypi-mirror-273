"""Core module."""
from typing import Iterable

from .command import Command


class CommandQueueInvoker():
    """A commands queue invoker."""
    def __init__(self):
        self._queue: Iterable[Command] = []

    def add(self, command: Command) -> None:
        """Adds a new command to the queue.

        :command: Command
        :returns: None

        """
        self._queue.append(command)

    def execute_commands(self) -> None:
        """Executes the commands in the queue.

        :returns: None

        """
        for command in self._queue:
            command.execute()
