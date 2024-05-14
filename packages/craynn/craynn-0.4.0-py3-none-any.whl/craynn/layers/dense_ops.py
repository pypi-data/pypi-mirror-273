import jax.numpy as jnp

from .. import dag
from ..nonlinearities import default_semibounded_nonlinearity
from ..parameters import default_weight_init, default_bias_init

from .meta import Layer, LayerModel, LayerSignature

__all__ = [
  'DenseLayer',
  'dense',

  'TensorDenseLayer',
  'tensor_dense',
]

class DenseLayer(Layer):
  def __init__(
    self, incoming, num_units,
    activation=default_semibounded_nonlinearity,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    """
    Dense (also called fully-connected) layer.
    Dense layer consists of `num_units` units, each of which takes
    weighted sum of inputs and applies `activation` function. In matrix form:
        f(X `dot` W + b)
    where:
      - W --- a weight matrix of size `(input_dim, num_units)`;
      - b --- a bias vector of size `(num_units, )`;
      - X --- input matrix of size `(batch_size, input_dim)`.

    If `X` has dimensionality `m > 2` first `m - 1` axes are treated as batch dimensions.

    :param incoming: incoming layer;
    :param num_units: number of output units;
    :param activation: activation function `f`;
    :param W: weight matrix, parameter with default properties `weights=True`, `trainable=True`;
    :param b: bias vector, parameter with default properties `biases=True`, `trainable=True`;
    :param name: name for the layer.
    """
    input_shape = dag.get_output_shape(incoming)
    self.num_units = num_units

    if len(input_shape) < 2:
      raise ValueError(
        'Dense layer accepts only tensors of dimensionality higher than or equal to 2 [got %s]!' % (input_shape, )
      )

    self.activation = activation

    self.W = W(
      shape=(input_shape[-1], num_units),
      name='W', weights=True, trainable=True
    )
    self.b = b(
      shape=(num_units,),
      name='b', biases=True, trainable=True
    )

    super(DenseLayer, self).__init__(
      incoming,
      name=name,
      parameters=(self.W, self.b)
    )

  def get_output_for(self, W, b, X):
    return self.activation(
      jnp.matmul(X, W) + b
    )

  def get_output_shape_for(self, W_shape, b_shape, X_shape):
    if len(X_shape) < 2:
      raise ValueError('Dense layer accepts only 2+ dimensional tensors!')

    return X_shape[:-1] + (self.num_units,  )

  def signature(self) -> LayerSignature:
    return (
      ('I', ),
      ('IO', 'O'),
      'O'
    )

class dense(LayerModel):
  LayerType = DenseLayer

  def __init__(
    self, num_units,
    activation=default_semibounded_nonlinearity,
    W=default_weight_init, b=default_bias_init,
    name=None
  ):
    super().__init__(num_units, activation=activation, W=W, b=b, name=name)

class TensorDenseLayer(Layer):
  def __init__(self, incoming, num_units,
               activation=default_semibounded_nonlinearity,
               W=default_weight_init,
               b=default_bias_init,
               axis=-1,
               name=None):
    input_shape = dag.get_output_shape(incoming)
    self.num_units = num_units
    self.axis = (len(input_shape) + axis) % len(input_shape)

    self.b_broadcast = tuple(
      (None if i != self.axis else slice(None, None, None))
      for i in range(len(input_shape))
    )

    self.activation = activation

    super(TensorDenseLayer, self).__init__(
      incoming,
      name=name,
      parameters=(
        W(shape=(input_shape[self.axis], num_units), name='W', weights=True, trainable=True),
        b(shape=(num_units,), name='b', biases=True, trainable=True)
      ),
    )

  def get_output_for(self, W, b, input):
    product = jnp.transpose(
      jnp.tensordot(input, W, axes=[(self.axis, ), (0, )]),
      axes=(*range(self.axis, ), -1, *range(self.axis, input.ndim - 1))
    )

    return self.activation(product + b[self.b_broadcast])

  def get_output_shape_for(self, W_shape, b_shape, input_shape):
    return tuple([
      (input_shape[i] if i != self.axis else self.num_units)
      for i in range(len(input_shape))
    ])

class tensor_dense(LayerModel):
  LayerType = TensorDenseLayer

  def __init__(
    self, num_units,
    activation=default_semibounded_nonlinearity,
    W=default_weight_init,
    b=default_bias_init,
    axis=-1,
    name=None
  ):
    super().__init__(num_units, activation=activation, W=W, b=b, axis=axis, name=name)