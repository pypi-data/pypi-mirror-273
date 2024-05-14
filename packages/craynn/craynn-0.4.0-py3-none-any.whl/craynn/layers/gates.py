import jax.numpy as jnp
import jax.nn as jnn

from .. import dag
from .meta import Layer, LayerModel

from ..parameters import zeros_init

__all__ = [
  'SoftmaxGate', 'softmax_gate',
  'SwitchGateLayer', 'switch_gate',
  'ReZeroGate', 'rezero'
]

class SoftmaxGate(Layer):
  def __init__(self, *incoming, w=zeros_init(), name=None):
    incoming_shape = dag.get_output_shape(incoming[0])
    self.w_broadcast = (None, ) * len(incoming_shape) + (Ellipsis, )

    super(SoftmaxGate, self).__init__(
      *incoming,
      name=name,
      parameters=(
        w(shape=(len(incoming),), weights=True, trainable=True, name='w')
      )
    )

  def get_output_for(self, w, *inputs):
    stacked = jnp.stack(inputs, axis=-1)
    coefs = jnn.softmax(w)

    return jnp.sum(stacked * coefs[self.w_broadcast], axis=-1)

  def get_output_shape_for(self, *input_shapes):
    return input_shapes[0]

class softmax_gate(LayerModel):
  LayerModel = SoftmaxGate

  def __init__(self, w=zeros_init(), name=None):
    super().__init__(w=w, name=name)

class SwitchGateLayer(Layer):
  def __init__(self, *incoming, name=None):
    gate, incoming1, incoming2 = incoming

    shape_incoming = dag.get_output_shape(incoming1)
    shape_gate = dag.get_output_shape(gate)

    self.gate_broadcast = (slice(None, None, None), ) * len(shape_gate) + \
                          (None, ) * (len(shape_incoming) - len(shape_gate))

    super(SwitchGateLayer, self).__init__(
      *incoming,
      parameters=(),
      name=name,
    )

  def get_output_shape_for(self, input_shape_gate, input_shape_1, input_shape_2):
    assert input_shape_1 == input_shape_2, 'Switch gate requires two incoming layers to have the same output shape'
    assert len(input_shape_gate) == 1, 'Gate input must be 1D'

    return input_shape_1

  def get_output_for(self, gate, input1, input2):
    activation = jnn.sigmoid(gate)
    return activation[self.gate_broadcast] * input1 + (1 - activation)[self.gate_broadcast] * input2

class switch_gate(LayerModel):
  LayerType = SwitchGateLayer

  def __init__(self, name=None):
    super().__init__(name=name)


class ReZeroGate(Layer):
  def __init__(self, *incoming, gate=zeros_init(), name=None):
    self.gate = gate(
      shape=(),
      name='gate',
      trainable=True,
      gate=True
    )
    
    super().__init__(
      *incoming,
      name=name,
      parameters=(self.gate, )
    )

  def get_output_for(self, gate, original, residual):
    return original + gate * residual

  def get_output_shape_for(self, gate_shape, original_shape, residual_shape):
    assert original_shape == residual_shape
    return original_shape

class rezero(LayerModel):
  LayerType = ReZeroGate

  def __init__(self, gate=zeros_init(), name=None):
    super().__init__(gate=gate, name=name)