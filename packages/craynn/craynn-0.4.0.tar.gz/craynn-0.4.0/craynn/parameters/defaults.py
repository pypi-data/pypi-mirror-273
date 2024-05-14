from .common import zeros_init, normal_init
from .glorot import glorot_normal_init

__all__ = [
  'default_weight_init',
  'default_bias_init',
  'default_input_init'
]

default_input_init = normal_init()
default_weight_init = glorot_normal_init()
default_bias_init = zeros_init()