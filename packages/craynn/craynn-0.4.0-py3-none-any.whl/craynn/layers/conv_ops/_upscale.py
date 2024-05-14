import jax

from ... import dag
from ...parameters import default_weight_init, default_bias_init
from ...nonlinearities import linear
from ..meta import Layer, LayerModel

from ._conv import DepthwiseTransposedConvLayer
from . import conv_utils

__all__ = [
  'UpscaleLayer',
  'NearestUpscaleLayer', 'LinearUpscaleLayer', 'CubicUpscaleLayer',
  'upscale', 'linear_upscale', 'cubic_upscale',
  
  'DepthwiseTransposedUpscaleLayer', 'deconv_upscale'
]

class UpscaleLayer(Layer):
  method: jax.image.ResizeMethod

  def __init__(self, incoming, kernel_size=2, name=None):
    incoming_shape = dag.get_output_shape(incoming)
    self.ndim = len(incoming_shape) - 2

    if self.ndim < 1:
      raise ValueError(f'UpscaleLayer accepts tensors which are at least 3D, got {incoming_shape}')

    self.kernel_size = conv_utils.normalized_shape(kernel_size, self.ndim)

    super(UpscaleLayer, self).__init__(incoming, name=name)

  def get_output_for(self, incoming):
    target_shape = self.get_output_shape_for(incoming.shape)
    return jax.image.resize(incoming, shape=target_shape, method=self.method)

  def get_output_shape_for(self, incoming_shape):
    return incoming_shape[:2] + tuple(
      k * s for k, s in zip(self.kernel_size, incoming_shape[2:])
    )

class UpscaleLayerModel(LayerModel):
  def __init__(self, kernel_size=2, name=None):
    super().__init__(kernel_size=kernel_size, name=name)

class NearestUpscaleLayer(UpscaleLayer):
  method = jax.image.ResizeMethod.NEAREST

class upscale(LayerModel):
  LayerType = NearestUpscaleLayer

class LinearUpscaleLayer(UpscaleLayer):
  method = jax.image.ResizeMethod.LINEAR

class linear_upscale(LayerModel):
  LayerType = LinearUpscaleLayer

class CubicUpscaleLayer(UpscaleLayer):
  method = jax.image.ResizeMethod.LINEAR

class cubic_upscale(LayerModel):
  LayerType = CubicUpscaleLayer

class DepthwiseTransposedUpscaleLayer(DepthwiseTransposedConvLayer):
  def __init__(
    self, incoming: Layer,
    kernel_size: int | tuple[int, ...] = 2,
    activation=linear(),
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(DepthwiseTransposedUpscaleLayer, self).__init__(
      incoming=incoming,
      kernel_size=kernel_size,
      activation=activation,
      padding=0,
      strides=kernel_size,
      dilation=1,
      W=W, b=b,
      name=name
    )

class deconv_upscale(LayerModel):
  LayerType = DepthwiseTransposedUpscaleLayer

  def __init__(
    self,
    kernel_size: int | tuple[int, ...] = 2,
    activation=linear(),
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(kernel_size, activation=activation, W=W, b=b, name=name)