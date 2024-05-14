from inspect import *
import jax
from jax.tree_util import register_pytree_node_class

from ..dag import get_name
from ..layers import InputLayer

__all__ = [
  'get_signature', 'get_named_layers', 'pdict'
]

def get_signature(inputs):
  return Signature(
    parameters=[
      Parameter(name=input.name, kind=Parameter.POSITIONAL_OR_KEYWORD)
      for input in inputs
    ]
  )

def get_named_layers(layers):
  named_layers = dict()
  for layer in layers:
    name = get_name(layer)

    if name is None:
      continue

    if name not in named_layers:
      named_layers[name] = layer
    else:
      if isinstance(layer, InputLayer) and isinstance(named_layers[name], InputLayer):
        raise Exception('Collision in input names: %s' % (name, ))

  return named_layers

@register_pytree_node_class
class pdict(dict):
  """
  A convenience extension of dict which allows to easily filter parameters by properties.
  """
  def tree_flatten(self):
    return self.values(), self.keys()

  @classmethod
  def tree_unflatten(cls, aux_data, children):
    return cls(zip(aux_data, children))

  def filter(self, **properties):
    from ..parameters import check_properties

    check_props = check_properties(**properties)
    return pdict((param, value) for param, value in self.items() if check_props(param))

  def __call__(self, **properties):
    return self.filter(**properties)