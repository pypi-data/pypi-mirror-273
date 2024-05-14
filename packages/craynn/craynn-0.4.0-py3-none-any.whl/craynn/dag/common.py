from typing import Sequence

from .meta import Node

__all__ = [
  'get_nodes',
  'get_source_nodes',
]

def get_nodes(nodes: Node | Sequence[Node]) -> tuple[Node, ...]:
  from . import evaluate
  return tuple(evaluate.propagate(lambda node, *args: node, nodes).values())

def get_source_nodes(nodes: Node | Sequence[Node]):
  return tuple(node for node in get_nodes(nodes) if len(node.incoming) == 0)