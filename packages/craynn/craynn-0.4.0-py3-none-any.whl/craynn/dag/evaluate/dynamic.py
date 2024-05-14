from typing import TypeVar, Callable, Protocol, Sequence, overload
from ..meta import Node

__all__ = [
  'propagate',
  'reduce'
]

T = TypeVar('T')
Aux = TypeVar('Aux')

class GraphReducer(Protocol[T, Aux]):
  def __call__(self, node: Node, args: Sequence[T], aux: Aux) -> T:
    ...


def propagate(
  f: GraphReducer[T, Aux],
  nodes: Sequence[Node] | Node,
  substitutes: dict[Node, T] | None=None,
  get_incoming: Callable[[Node], tuple[Sequence[Node], Aux]] | None=None
) -> dict[Node, T]:
  """
  Similar to the ordinary `propagate` but allows to dynamically compute incoming nodes and
  pass results of `incoming(node)` to `f`. For each node of the DAG it computes:

      r(node) = f(node, [r(x) for x in incoming_nodes], intermediate_result)
      where:
        incoming_nodes, intermediate_result = get_incoming(node)

  Graph is defined as `nodes` and all their dependencies.
  This function caches results `r(node)`, thus, `f`.

  Note, that unlike `common.propagate`, operator `f` receives 3 arguments:
  - node;
  - incoming nodes (dependencies) that *need to be computed*;
  - value returned by `incoming`.

  This is useful for implementing cached dataflows, when dependencies depend on results of cache retrieval:

      def incoming(node):
        try:
          return list(), load_cache(node)
        except:
          return node.incoming, None

      def operator(node, inputs, cached):
        if cached is not None:
          return cached
        else:
          <perform computations>

  NB: if substitutes are specified not all nodes might be evaluated, also not all nodes might
    be present in the result.

  :param f: operator to propagate, a function of type `(Node, List[A], B) -> A`;
  :param nodes: a list of nodes, output nodes of the DAG `f` is to be propagated through;
  :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`, None (empty) by default;
  :param get_incoming: operator `Node -> (List[Node], B)`, returns list of incoming nodes (dependencies)
    and some intermediate results (e.g. cached results),
    if None --- defaults to `lambda node: (node.incoming, None)`;
  :return: dictionary `Node -> A`.
  """
  if get_incoming is None:
    get_incoming = lambda node: (node.incoming, None)

  known_results = dict() if substitutes is None else dict(substitutes.items())
  graph = dict()
  intermediate_result = dict()

  stack = list()
  stack.extend(nodes)

  while len(stack) > 0:
    current_node = stack.pop()

    if current_node in known_results:
      continue

    if current_node not in graph:
      graph[current_node], intermediate_result[current_node] = get_incoming(current_node)

    incoming_nodes, intermediate = graph[current_node], intermediate_result[current_node]

    unknown_dependencies = [
      nodes
      for nodes in incoming_nodes
      if nodes not in known_results
    ]

    if len(unknown_dependencies) == 0:
      args = tuple(known_results[node] for node in incoming_nodes)
      known_results[current_node] = f(current_node, args, intermediate)

    else:
      intermediate_result[current_node] = intermediate
      stack.append(current_node)
      stack.extend(unknown_dependencies)

  return known_results

@overload
def reduce(
  f: GraphReducer[T, Aux],
  nodes: Node,
  substitutes: dict[Node, T] | None=None,
  get_incoming: Callable[[Node], tuple[Sequence[Node], Aux]] | None=None
) -> T:
  ...

@overload
def reduce(
  f: GraphReducer[T, Aux],
  nodes: Sequence[Node],
  substitutes: dict[Node, T] | None=None,
  get_incoming: Callable[[Node], tuple[Sequence[Node], Aux]] | None=None
) -> T:
  ...

def reduce(f, nodes, substitutes=None, get_incoming=None):
  """
    The same as the ordinary `reduce` but for dynamic `propagate`

        r(node) = f(node, [r(x) for x in incoming(node)])

  :param f: operator to propagate, a function of type `(Node, List[A], B) -> A`;
  :param nodes: a list of nodes, output nodes of the DAG `f` is to be propagated through;
  :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`, None (empty) by default;
  :param get_incoming: operator `Node -> (List[Node], B)`, returns list of incoming nodes (dependencies)
    and some intermediate results (e.g. cached results), if None --- defaults to `lambda node: (node.incoming, None)`;
  :return: a tuple with outputs of `nodes`, or a single value if `nodes` is a single node.
  """

  if isinstance(nodes, Sequence):
    result = propagate(f, nodes, substitutes=substitutes, get_incoming=get_incoming)
    return tuple(
      result[node]
      for node in nodes
    )

  else:
    result = propagate(f, (nodes, ), substitutes=substitutes, get_incoming=get_incoming)
    return result[nodes]