"""Utils module."""
from typing import Iterable

class DependencySorter: # pylint: disable=too-few-public-methods
    """Sorts elements of a list based on internal depenencies.

    :entity_attr: str The attribute, of the entity, holding the actual name.
    :depends_attr: str The name of the attribute defining the dependency.
    """
    def __init__(self, entity_attr: str, depends_attr: str):
        self.entity_attr = entity_attr
        self.depends_attr = depends_attr

    def sort(self, objects: Iterable) -> Iterable:
        """Sorts elements in the `objects` list.

        :objet: TODO
        :returns: TODO
        """
        graph, all_nodes, node_lookup = self._build_graph(objects)
        visited: set[str] = set()
        stack: list[str] = []

        for node in all_nodes:
            if node not in visited:
                self._topological_sort_util(node, visited, stack, graph)

        return [node_lookup[node] for node in reversed(stack)]

    def _build_graph(self, objects: Iterable) -> tuple[dict, set[str], dict]:
        graph = {}
        all_nodes = set()
        node_lookup = {}

        for obj in objects:
            entity = getattr(obj, self.entity_attr)
            depends_on = getattr(obj, self.depends_attr, None)

            all_nodes.add(entity)
            node_lookup[entity] = obj

            if depends_on:
                graph.setdefault(depends_on, []).append(entity)

        return graph, all_nodes, node_lookup

    def _topological_sort_util(
        self,
        node: str,
        visited: Iterable[str],
        stack: Iterable[str],
        graph: dict
    ) -> None:
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                self._topological_sort_util(neighbor, visited, stack, graph)

        stack.append(node)
