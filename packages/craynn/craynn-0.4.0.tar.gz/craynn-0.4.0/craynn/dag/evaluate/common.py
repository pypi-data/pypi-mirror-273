from typing import Sequence, TypeVar, TypeAlias, Any, overload

from ... import utils
from ..meta import Node

from . import static
from . import dynamic

__all__ = [
  'get_all_outputs',
  'get_output',
  'get_output_shape',
  'get_all_output_shapes',
  'get_nodes',
  'get_sources',
  'get_mode_nodes'
]

Shape: TypeAlias = tuple[int, ...]
T = TypeVar('T')

def get_all_outputs(
  nodes: Sequence[Node] | Node,
  substitutes: dict[Node, T] | None=None,
  individual_kwargs: dict[Node, dict[str, Any]] | None=None,
  common_kwargs: dict[str, Any] | None=None
) -> dict[Node, T]:
  if individual_kwargs is None:
    individual_kwargs = dict()

  if common_kwargs is None:
    common_kwargs = dict()

  def apply(node, args):
    if node in individual_kwargs:
      return utils.func.apply_with_kwargs(node.get_output_for, *args, **individual_kwargs[node], **common_kwargs)
    else:
      return utils.func.apply_with_kwargs(node.get_output_for, *args, **common_kwargs)

  return static.propagate(apply, nodes, substitutes=substitutes)

@overload
def get_output(
  nodes: Node, substitutes: dict[Node, T] | None=None,
  individual_kwargs: dict[Node, dict[str, Any]] | None=None, common_kwargs: dict[str, Any] | None=None
) -> T: ...

@overload
def get_output(
  nodes: Sequence[Node], substitutes: dict[Node, T] | None = None,
  individual_kwargs: dict[Node, dict[str, Any]] | None = None, common_kwargs: dict[str, Any] | None = None
) -> tuple[T, ...]: ...

def get_output(nodes, substitutes=None, individual_kwargs=None, common_kwargs=None):
  results = get_all_outputs(
    nodes, substitutes=substitutes,
    individual_kwargs=individual_kwargs, common_kwargs=common_kwargs
  )

  if isinstance(nodes, Node):
    return results[nodes]
  else:
    return tuple(results[node] for node in nodes)

def get_all_output_shapes(nodes: Sequence[Node] | Node, substitutes: dict[Node, T] | None = None) -> dict[Node, Shape]:
  def apply(node: Node, args: Sequence[Shape]) -> Shape:
    return utils.func.apply_with_kwargs(node.get_output_shape_for, *args)

  return static.propagate(apply, nodes, substitutes=substitutes)

@overload
def get_output_shape(nodes: Node) -> Shape: ...

@overload
def get_output_shape(nodes: Sequence[Node]) -> tuple[Shape, ...]: ...

def get_output_shape(nodes):
  """
  Lazily computes output shapes of nodes.
  """
  def cached_shape(node: Node):
    return getattr(node, 'shape', None)

  def get_incoming(node: Node):
    result = cached_shape(node)

    if result is None:
      return node.incoming, None
    else:
      return (), result

  def operator(node: Node, args, cached):
    if cached is None:
      return node.get_output_shape_for(*args)
    else:
      return cached

  return dynamic.reduce(operator, nodes, get_incoming=get_incoming)

def get_nodes(nodes: Node, __class_or_tuple=None) -> tuple[Node, ...]:
  if __class_or_tuple is None:
    return static.filter(lambda _: True, nodes)
  else:
    return static.filter(lambda node: isinstance(node, __class_or_tuple), nodes)

def get_sources(nodes: Sequence[Node] | Node) -> tuple[Node, ...]:
  return static.filter(lambda node: len(node.incoming) == 0, nodes)

def get_mode_nodes(nodes: Node | Sequence[Node], mode: str):
  import inspect
  result = list()

  for node in get_nodes(nodes):
    params = inspect.signature(node.get_output_for).parameters

    if (
      mode in params and
      params[mode].kind != inspect.Parameter.VAR_KEYWORD and
      params[mode].kind != inspect.Parameter.VAR_POSITIONAL
    ):
      result.append(node)

  return result