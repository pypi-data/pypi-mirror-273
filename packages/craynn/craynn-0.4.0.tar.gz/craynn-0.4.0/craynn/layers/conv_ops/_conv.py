import jax

from ... import dag

from ...parameters import default_weight_init, default_bias_init
from ...nonlinearities import default_nonlinearity

from ..meta import Layer, LayerModel, LayerSignature

from . import conv_utils

__all__ = [
  'GeneralConvLayer',

  'ConvLayer', 'TransposedConvLayer',
  'conv', 'deconv',

  'PaddedConvLayer', 'PaddedTransposedConvLayer',
  'pconv', 'pdeconv',

  'DepthwiseGeneralConvLayer',

  'DepthwiseConvLayer', 'DepthwiseTransposedConvLayer',
  'depthwise_conv', 'depthwise_deconv'
]

class GeneralConvLayer(Layer):
  def __init__(
    self, incoming: Layer,
    transposed: bool,
    num_filters: int,
    kernel_size: int | tuple[int, ...]=3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding='valid',
    strides: int | tuple[int, ...]=1,
    dilation: int | tuple[int, ...]=1,
    groups: int | None=None,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    """
    Convolutional layer.

    :param incoming: incoming layer;
    :param ndim: dimensionality of the kernel;
    :param num_filters: number of filters
    :param kernel_size: spatial size of the convolutional kernel
    :param activation: activation function;
    :param padding: either a padding mode ('valid', 'same') or a concrete padding;
    :param strides: kernel strides;
    :param groups: number of kernel groups, must divide number of input and output channels,
      if None, matches number of input channels;
    :param dilation: kernel dilation;
    :param W: kernel parameter model;
    :param b: bias parameter model;
    :param name: name for the layer.
    """
    self.transposed = transposed

    input_shape = dag.get_output_shape(incoming)
    self.ndim = len(input_shape) - 2

    if self.ndim < 1:
      raise ValueError(f'Conv layer needs at least 3D input, got {input_shape}.')

    if num_filters <= 0:
      raise ValueError(f'`num_filters` must be > 0, got {num_filters}!')

    self.input_channels = conv_utils.get_channel_dim(input_shape)
    self.num_channels = num_filters

    self.kernel_size = conv_utils.normalized_shape(kernel_size, ndim=self.ndim)
    if groups is None:
      self.groups = 1
    else:
      self.groups = groups

    if self.num_channels % self.groups != 0:
      raise ValueError(f'`num_channels` should be divisible by `groups`, got {self.num_channels} and {self.groups}')

    self.channel_multiplier = self.input_channels // self.groups

    self.kernel_shape = (self.num_channels, self.channel_multiplier) + self.kernel_size

    self.dilation = conv_utils.normalized_shape(dilation, ndim=self.ndim)
    self.strides = conv_utils.normalized_shape(strides, ndim=self.ndim)

    self.padding = conv_utils.get_padding(padding, ndim=self.ndim)

    self.activation = activation

    self.W = W(self.kernel_shape, name='W', weights=True, conv_kernel=True, trainable=True)
    self.b = b((self.num_channels, ), name='b', biases=True, trainable=True)

    self.conv_spec = conv_utils.get_conv_spec(self.ndim)
    self.dimension_numbers = jax.lax.conv_dimension_numbers(input_shape, self.kernel_shape, self.conv_spec)

    super(GeneralConvLayer, self).__init__(
      incoming,
      name=name,
      parameters=(self.W, self.b),
    )

  def get_output_for(self, W, b, X):
    if self.transposed:
      convolved = conv_utils.conv_transpose(
        X, W,
        strides=self.strides,
        padding=self.padding,
        dilation=self.dilation,
        feature_group_count=self.groups,
        dimension_numbers=self.dimension_numbers
      )
    else:
      convolved = jax.lax.conv_general_dilated(
        X, W,
        window_strides=self.strides,
        padding=self.padding,
        rhs_dilation=self.dilation,
        feature_group_count=self.groups,
        dimension_numbers=self.dimension_numbers
      )

    broadcast = (None, ) + (slice(None), ) + (None, ) * self.ndim
    return self.activation(
       convolved + b[broadcast]
    )

  def get_output_shape_for(self, W_shape, b_shape, input_shape):
    if len(input_shape) != self.ndim + 2:
      raise ValueError(
        '%dD conv layer accepts only %dD tensors [got %s]!' % (self.ndim, self.ndim + 2, input_shape)
      )

    if self.transposed:
      return conv_utils.conv_transposed_output_shape(
        input_shape,
        self.kernel_shape,
        strides=self.strides,
        dilation=self.dilation,
        padding=self.padding,
        conv_spec=self.conv_spec
      )
    else:
      return conv_utils.conv_output_shape(
        input_shape,
        self.kernel_shape,
        strides=self.strides,
        dilation=self.dilation,
        padding=self.padding,
        conv_spec=self.conv_spec
      )

  def signature(self) -> LayerSignature:
    return (
      ('A' + '*' * self.ndim, ),
      ('CB' + '*' * self.ndim, 'C'),
      'C' + '*' * self.ndim
    )

### everything for a nice signature
class ConvLayer(GeneralConvLayer):
  def __init__(
    self, incoming: Layer,
    num_filters: int,
    kernel_size: int | tuple[int, ...]=3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding='valid',
    strides: int | tuple[int, ...]=1,
    dilation: int | tuple[int, ...]=1,
    groups: int | None=1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      incoming, transposed=False, num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding=padding, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class conv(LayerModel):
  LayerType = ConvLayer

  def __init__(
    self,
    num_filters: int,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    groups: int | None = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding=padding, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class TransposedConvLayer(GeneralConvLayer):
  def __init__(
    self, incoming: Layer,
    num_filters: int,
    kernel_size: int | tuple[int, ...]=3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding='valid',
    strides: int | tuple[int, ...]=1,
    dilation: int | tuple[int, ...]=1,
    groups: int | None=1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      incoming, transposed=True, num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding=padding, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class deconv(LayerModel):
  LayerType = TransposedConvLayer

  def __init__(
    self,
    num_filters: int,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    groups: int | None = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding=padding, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )


class PaddedConvLayer(ConvLayer):
  def __init__(
    self, incoming: Layer,
    num_filters: int,
    kernel_size: int | tuple[int, ...]=3,
    activation=default_nonlinearity,
    strides: int | tuple[int, ...]=1,
    dilation: int | tuple[int, ...]=1,
    groups: int | None=1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      incoming, num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding='same', strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class pconv(LayerModel):
  LayerType = PaddedConvLayer

  def __init__(
    self,
    num_filters: int,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    groups: int | None = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )


class PaddedTransposedConvLayer(TransposedConvLayer):
  def __init__(
    self, incoming: Layer,
    num_filters: int,
    kernel_size: int | tuple[int, ...]=3,
    activation=default_nonlinearity,
    strides: int | tuple[int, ...]=1,
    dilation: int | tuple[int, ...]=1,
    groups: int | None=1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      incoming, num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, padding='same', strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class pdeconv(LayerModel):
  LayerType = PaddedTransposedConvLayer

  def __init__(
    self,
    num_filters: int,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    groups: int | None = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super().__init__(
      num_filters=num_filters, kernel_size=kernel_size,
      activation=activation, strides=strides, dilation=dilation, groups=groups,
      W=W, b=b, name=name
    )

class DepthwiseGeneralConvLayer(GeneralConvLayer):
  def __init__(
    self, incoming: Layer, transposed: bool,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    input_shape = dag.get_output_shape(incoming)
    input_channels = conv_utils.get_channel_dim(input_shape)

    super(DepthwiseGeneralConvLayer, self).__init__(
      incoming=incoming,
      transposed=transposed,
      num_filters=input_channels,
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=strides,
      dilation=dilation,
      groups=input_channels,
      W=W, b=b,
      name=name,
    )

class DepthwiseConvLayer(DepthwiseGeneralConvLayer):
  def __init__(
    self, incoming: Layer,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(DepthwiseConvLayer, self).__init__(
      incoming=incoming,
      transposed=False,
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=strides,
      dilation=dilation,
      W=W, b=b,
      name=name,
    )

class depthwise_conv(LayerModel):
  LayerType = DepthwiseConvLayer

  def __init__(
    self,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(depthwise_conv, self).__init__(
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=strides,
      dilation=dilation,
      W=W, b=b,
      name=name,
    )

class DepthwiseTransposedConvLayer(DepthwiseGeneralConvLayer):
  def __init__(
    self, incoming: Layer,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(DepthwiseTransposedConvLayer, self).__init__(
      incoming=incoming,
      transposed=True,
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=strides,
      dilation=dilation,
      W=W, b=b,
      name=name,
    )

class depthwise_deconv(LayerModel):
  LayerType = DepthwiseTransposedConvLayer

  def __init__(
    self,
    kernel_size: int | tuple[int, ...] = 3,
    activation=default_nonlinearity,
    padding: conv_utils.Padding = 'valid',
    strides: int | tuple[int, ...] = 1,
    dilation: int | tuple[int, ...] = 1,
    W=default_weight_init,
    b=default_bias_init,
    name=None
  ):
    super(depthwise_deconv, self).__init__(
      kernel_size=kernel_size,
      activation=activation,
      padding=padding,
      strides=strides,
      dilation=dilation,
      W=W, b=b,
      name=name,
    )