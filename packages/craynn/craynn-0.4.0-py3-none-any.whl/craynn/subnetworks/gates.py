from ..dag import achain

from ..nonlinearities import linear
from ..layers import dense, flatten, switch_gate
from ..parameters import glorot_normal_init

__all__ = [
  'gated_connection'
]

default_gate = (
  dense(1, activation=linear(), W=glorot_normal_init(scale=0.1)),
  flatten(1)
)

def gated_connection(*body, gate=default_gate):
  def constructor(incoming):
    origin = incoming
    net = achain(*body)(incoming)
    activation = achain(gate)(incoming)

    return switch_gate()(origin, net, activation)

  return constructor
