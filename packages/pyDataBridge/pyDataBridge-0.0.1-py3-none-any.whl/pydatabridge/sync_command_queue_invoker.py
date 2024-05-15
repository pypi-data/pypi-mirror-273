"""Synchronization module."""

from .command_queue_invoker import CommandQueueInvoker

class SyncCommandQueueInvoker(CommandQueueInvoker):
    """Commands queue invoker for syncrhonization commands."""
