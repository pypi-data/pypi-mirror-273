from ..dag import achain
from ..layers import elementwise_sum as _elementwise_sum, rezero as _rezero

__all__ = [
  'residual_connection',
  'rezero_connection',
]

def residual_connection(*body, merge_op=_elementwise_sum()):
  def constructor(incoming):
    origin = incoming
    net = achain(*body)(incoming)
    return merge_op(origin, net)

  return constructor

def rezero_connection(*body, rezero=_rezero()):
  def constructor(incoming):
    origin = incoming
    net = achain(*body)(incoming)
    return rezero(origin, net)

  return constructor

