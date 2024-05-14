from typing import Sequence, Protocol, TypeVar, Callable, overload

from ..meta import Node

__all__ = [
  'propagate',
  'reduce',
  'filter',
  'find',
]

T = TypeVar('T')

class GraphReducer(Protocol[T]):
  def __call__(self, node: Node, args: Sequence[T]) -> T: ...

def propagate(
  f: GraphReducer[T],
  nodes: Node | Sequence[Node],
  substitutes: dict[Node, T] | None=None,
  get_incoming: Callable[[Node], Sequence[Node]] | None=None
) -> dict[Node, T]:
  """
  For each node of the DAG computes:

      r(node) = f(node, [r(x) for x in get_incoming(node)])

  `dag` is defined as `nodes` and all their dependencies.
  This function caches results `r(node)`, thus, `f`.

  NB: if substitutes are specified not all nodes might be evaluated, also not all nodes might
    be present in the result.

  :param f: operator to propagate, a function of type `(Node, List[A]) -> A`;
  :param nodes: a list of nodes, output nodes of the dag `f` is to be propagated through;
  :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`, None (empty) by default;
  :param get_incoming: overrides graph connectivity, if None (the default), uses `node.incoming`;
  :return: dictionary `Node -> A`.
  """
  if get_incoming is None:
    get_incoming = lambda node: node.incoming

  if substitutes is not None:
    known_results = substitutes.copy()
  else:
    known_results = dict()

  stack: list[Node] = [*nodes] if isinstance(nodes, Sequence) else [nodes]

  while len(stack) > 0:
    current = stack.pop()

    if current in known_results:
      continue

    incoming = get_incoming(current)

    unknown_dependencies = [
      nodes
      for nodes in incoming
      if nodes not in known_results
    ]

    if len(unknown_dependencies) == 0:
      known_results[current] = f(current, [known_results[node] for node in incoming])

    else:
      stack.append(current)
      stack.extend(unknown_dependencies)

  return known_results

@overload
def reduce(
  f: GraphReducer[T], nodes: Sequence[Node], substitutes: dict[Node, T] | None=None,
  get_incoming: Callable[[Node], Sequence[Node]] | None=None
) -> tuple[T, ...]:
  ...

@overload
def reduce(
  f: GraphReducer[T], nodes: Node, substitutes: dict[Node, T] | None = None,
  get_incoming: Callable[[Node], Sequence[Node]] | None = None
) -> T:
  ...

def reduce(f, nodes, substitutes=None, get_incoming=None):
  """
    The same as `propagate` but returns results only for `nodes`:

        r(node) = f(node, [r(x) for x in incoming(node)])

    :param f: operator to propagate, a function of type `(Node, List[A]) -> A`;
    :param nodes: a list of nodes or a node --- output nodes of the dag `f` is to be propagated through;
    :param substitutes: a dictionary `Node -> A`, overrides results of r(node),
      None is the same as an emtpy dictionary;
    :param get_incoming: overrides graph connectivity, if None (the default), uses `node.incoming`;
    :return: tuple of results (if `nodes` is a collection of nodes), or
      just result for the `nodes` (in case `nodes` is a single node)
    """
  if isinstance(nodes, Sequence):
    result = propagate(f, nodes, substitutes=substitutes, get_incoming=get_incoming)
    return tuple(result[node] for node in nodes)

  else:
    result = propagate(f, (nodes, ), substitutes=substitutes, get_incoming=get_incoming)
    return result[nodes]

def filter(
  predicate: Callable[[Node], bool],
  nodes: Node | Sequence[Node],
  get_incoming: Callable[[Node], Sequence[Node]] | None=None
) -> tuple[Node, ...]:
  results: list[Node] = []
  stack: list[Node] = [*nodes] if isinstance(nodes, Sequence) else [nodes]
  visited: set[Node] = set()

  if get_incoming is None:
    get_incoming = lambda node: node.incoming

  while len(stack) > 0:
    current = stack.pop()
    if current in visited:
      continue

    if predicate(current):
      results.append(current)

    stack.extend(get_incoming(current))

  return tuple(results)

def find(
  predicate: Callable[[Node], bool],
  nodes: Node | Sequence[Node],
  get_incoming: Callable[[Node], Sequence[Node]] | None=None
) -> None | Node:
  stack: list[Node] = [*nodes] if isinstance(nodes, Sequence) else [nodes]
  visited: set[Node] = set()

  if get_incoming is None:
    get_incoming = lambda node: node.incoming

  while len(stack) > 0:
    current = stack.pop()
    if current in visited:
      continue

    if predicate(current):
      return current

    stack.extend(get_incoming(current))

  return None