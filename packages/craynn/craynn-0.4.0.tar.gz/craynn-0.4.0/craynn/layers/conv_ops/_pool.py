from typing import Callable

import math

import jax
import jax.numpy as jnp

from ... import dag

from ...parameters import default_weight_init, default_bias_init
from ...nonlinearities import linear

from ..meta import Layer, LayerModel
from ._conv import DepthwiseConvLayer
from . import conv_utils

__all__ = [
  'PoolingLayer', 'PoolingLayerModel',
  'MaxPoolLayer', 'max_pool',
  'MeanPoolLayer', 'mean_pool',

  'ConvPoolLayer', 'conv_pool',
]


class PoolingLayer(Layer):
  normalization: bool
  initial_value: float

  def operator(self) -> Callable[[jax.Array, jax.Array], jax.Array]:
    raise NotImplementedError()

  def __init__(
    self, incoming,
    kernel_size: int | tuple[int, ...]=2,
    pad: conv_utils.Padding='valid',
    strides: None | int | tuple[int, ...]=None,
    name=None
  ):
    input_shape = dag.get_output_shape(incoming)
    ndim = len(input_shape) - 2

    if ndim < 1:
      raise ValueError(f'Input shape for a pool layer must be at least 3D, got {input_shape}.')

    self.ndim = ndim

    self.kernel_size = conv_utils.normalized_shape(kernel_size, ndim=ndim)

    if strides is None:
      strides = self.kernel_size

    self.strides = conv_utils.normalized_shape(strides, ndim=ndim)
    self.padding = conv_utils.get_padding(pad, ndim)

    if self.normalization:
      self.normalization_constant = 1.0 / math.prod(self.kernel_size)
    else:
      self.normalization_constant = None

    self.conv_spec = conv_utils.get_conv_spec(ndim=ndim)

    super(PoolingLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X):
    ### https://github.com/google/jax/issues/7815
    reduced = jax.lax.reduce_window(
      operand=X,
      init_value=self.initial_value,
      computation=self.operator(),
      window_dimensions=(1, 1) + self.kernel_size,
      window_strides=(1, 1) + self.strides,
      padding=self.padding
    )

    if self.normalization_constant is None:
      return reduced
    else:
      return self.normalization_constant * reduced

  def get_output_shape_for(self, input_shape):
    if len(input_shape) != self.ndim + 2:
      raise ValueError(
        '%dD pool layer accepts only %dD tensors [got %s]!' % (input_shape, self.ndim, len(input_shape))
      )

    return conv_utils.conv_output_shape(
        input_shape,
        (input_shape[1], input_shape[1], *self.kernel_size),
        strides=self.strides,
        dilation=(1, ) * self.ndim,
        padding=self.padding,
        conv_spec=self.conv_spec
      )

class PoolingLayerModel(LayerModel):
  def __init__(
    self, kernel_size: int | tuple[int, ...]=2,
    pad: conv_utils.Padding='valid',
    strides: None | int | tuple[int, ...]=None,
    name=None
  ):
    super().__init__(kernel_size=kernel_size, pad=pad, strides=strides, name=name)

class MaxPoolLayer(PoolingLayer):
  def operator(self):
    return jax.lax.max

  initial_value = -math.inf
  normalization = False

class max_pool(PoolingLayerModel):
  LayerType = MaxPoolLayer

class MeanPoolLayer(PoolingLayer):
  def operator(self):
    return jax.lax.add

  initial_value = 0
  normalization = True

class mean_pool(PoolingLayerModel):
  LayerType = MeanPoolLayer


class ConvPoolLayer(DepthwiseConvLayer):
  def __init__(
    self, incoming: Layer,
    kernel_size: int | tuple[int, ...] = 2,
    activation=linear(),
    padding: conv_utils.Padding = 'same',
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(ConvPoolLayer, self).__init__(
      incoming=incoming,
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=kernel_size,
      dilation=1,
      W=W, b=b,
      name=name
    )

class conv_pool(LayerModel):
  LayerType = ConvPoolLayer

  def __init__(self,
    kernel_size: int | tuple[int, ...] = 2,
    activation=linear(),
    padding: conv_utils.Padding = 'same',
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(kernel_size=kernel_size, activation=activation, padding=padding, W=W, b=b, name=name)