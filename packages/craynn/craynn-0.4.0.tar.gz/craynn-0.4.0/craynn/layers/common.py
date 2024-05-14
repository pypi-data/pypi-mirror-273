import functools
import math

import jax
import jax.numpy as jnp

from ..utils import normalize_axis, soft_maximum, soft_minimum
from ..parameters import constant_parameter

from .meta import Layer, InputLayer, LayerModel

__all__ = [
  'const_input',

  'CustomLayer', 'custom_layer',
  'FunctionLayer', 'function_layer',

  'ConcatLayer', 'concat',
  'FlattenLayer', 'flatten',
  'ReshapeLayer', 'reshape',
  'ExpandLayer', 'expand',

  'ElementwiseLayer', 'ElementwiseSumLayer', 'ElementwiseMeanLayer',
  'ElementwiseMaxLayer', 'ElementwiseMinLayer',

  'elementwise', 'elementwise_sum', 'elementwise_mean',
  'elementwise_max', 'elementwise_min',

  'BroadcastLayer', 'broadcast',
  'ExpandConcatLayer', 'expand_concat',

  'GeneralPoolLayer', 'GeneralMaxPoolLayer', 'GeneralMeanPoolLayer', 'GeneralSumPoolLayer',
  'general_max_pool', 'general_mean_pool', 'general_sum_pool',

  'BatchPoolLayer', 'MaxBatchPoolLayer', 'MeanBatchPoolLayer', 'SumBatchPoolLayer',
  'max_batch_pool', 'mean_batch_pool', 'sum_batch_pool',

  'CumSumLayer', 'cumsum'
]


class ConstInput(InputLayer):
  def __init__(self, const, name=None):
    self.value = jnp.array(const)
    super(ConstInput, self).__init__(shape=const.shape, name=name)

  def get_output_for(self):
    return self.value

class const_input(LayerModel):
  LayerType = ConstInput

  def __init__(self, const, name=None):
    super().__init__(const, name=name)


_default_shape_f = lambda *input_shapes: input_shapes[0]

class CustomLayer(Layer):
  def __init__(self, *incoming, f, shape_f=_default_shape_f, name=None):
    self.f = f
    self.shape_f = shape_f

    super(CustomLayer, self).__init__(*incoming, name=name)

  def get_output_for(self, *inputs):
    return self.f(*inputs)

  def get_output_shape_for(self, *input_shapes):
    return self.shape_f(*input_shapes)

class custom_layer(LayerModel):
  LayerType = CustomLayer

  def __init__(self, f, shape_f=_default_shape_f, name=None):
    super().__init__(f, shape_f=shape_f, name=name)


class FunctionLayer(Layer):
  def __init__(self, *incoming, f, name=None):
    if name is None:
      name = f.__name__

    self.f = f

    super(FunctionLayer, self).__init__(*incoming, name=name)

  def get_output_for(self, *incoming):
    return self.f(*incoming)

  def get_output_shape_for(self, *input_shapes):
    return input_shapes[0]

class function_layer(LayerModel):
  LayerType = FunctionLayer

  def __init__(self, f, name=None):
    super().__init__(f, name=name)


class ConcatLayer(Layer):
  def __init__(self, *incoming, axis=-1, name=None):
    assert len(incoming) > 0
    self.axis = axis

    super(ConcatLayer, self).__init__(*incoming, name=name)

  def get_output_for(self, *inputs):
    return jnp.concatenate(inputs, axis=self.axis)

  def get_output_shape_for(self, *input_shapes):
    from ..utils.axes import normalize_axis

    first = input_shapes[0]
    axis = normalize_axis(first, self.axis)

    def gsum(xs):
      total = 0
      for x in xs:
        if x is None:
          return None
        else:
          total += x

      return total

    return tuple(
      first[i] if i != axis else gsum(s[i] for s in input_shapes)
      for i in range(len(first))
    )

class concat(LayerModel):
  LayerType = ConcatLayer

  def __init__(self, axis: int=-1, name=None):
    super().__init__(axis=axis, name=name)


from functools import reduce as _reduce

class FlattenLayer(Layer):
  def __init__(self, incoming, outdim=2, name=None):
    self.outdim = outdim

    super(FlattenLayer, self).__init__(incoming, name=name)

  def get_output_for(self, incoming):
    keep = self.outdim - 1
    return jnp.reshape(incoming, newshape=(*incoming.shape[:keep], -1))

  def get_output_shape_for(self, input_shapes):
    keep = self.outdim - 1
    return (
      *input_shapes[:keep],
      _reduce(
        lambda a, b: a * b if a is not None and b is not None else None,
        input_shapes[self.outdim - 1:],
        1
      ),
    )

class flatten(LayerModel):
  LayerType = FlattenLayer

  def __init__(self, outdim: int=2, name=None):
    super().__init__(outdim=outdim, name=name)


class ReshapeLayer(Layer):
  def __init__(self, incoming, new_shape, name=None):

    assert len([dim for dim in new_shape if (dim is None or dim < 0)]) < 2, 'ambiguous new shape'

    self.new_shape = tuple(
      (-1 if s is None else s)
      for s in new_shape
    )

    super(ReshapeLayer, self).__init__(incoming, name=name)

  def get_output_for(self, incoming):
    return jnp.reshape(incoming, self.new_shape)

  def get_output_shape_for(self, input_shape):
    import numpy as np

    if -1 in self.new_shape:
      if all(dim is not None for dim in input_shape):
        total = math.prod(input_shape)
        known_dims = np.prod([ dim for dim in self.new_shape if dim is not None], dtype='int64')
        assert total % known_dims == 0, 'can not broadcast %s into %s' % (input_shape, self.new_shape)
        inferred = total // known_dims

        return tuple(dim if dim is not None else inferred for dim in self.new_shape)

      else:
        return tuple(dim if dim >= 0 else None for dim in self.new_shape)

    else:
      return self.new_shape

class reshape(LayerModel):
  LayerType = ReshapeLayer

  def __init__(self, new_shape: tuple[int, ...], name=None):
    super().__init__(new_shape, name=name)


class ExpandLayer(Layer):
  def __init__(self, incoming, item, name=None):
    super(ExpandLayer, self).__init__(incoming, name=name)

    assert all(
      dim == slice(None, None, None) or (isinstance(dim, int) and dim > 0)
      for dim in item
    )
    self.item = item

  def get_output_shape_for(self, input_shape):
    return tuple(
      dim if s == slice(None, None, None) else s
      for dim, s in zip(input_shape, self.item)
    )

  def get_output_for(self, input):
    shape = tuple(
      dim if s == slice(None, None, None) else s
      for dim, s in zip(input.shape, self.item)
    )
    return jnp.broadcast_to(input, shape)

class _expand(LayerModel):
  LayerType = ExpandLayer

  def __init__(self, item, name=None):
    super().__init__(item, name=name)

class ExpandExpression(object):
  def __call__(self, item, name=None):
    return _expand(item, name=name)

  def __getitem__(self, item):
    return _expand(item)

expand = ExpandExpression()


class ExpandConcatLayer(Layer):
  def __init__(self, *incoming, axis=-1, name=None):
    self.axis = axis

    super(ExpandConcatLayer, self).__init__(*incoming, name=name)

  def get_output_shape_for(self, *input_shapes):
    axis = normalize_axis(len(input_shapes[0]), self.axis)

    def get_shape(dims, i):
      if i == axis:
        if any(dim is None for dim in dims):
          return None
        else:
          return sum(dims)

      concrete_dims = [d for d in dims if d is not None]
      if len(concrete_dims) > 0:
        return max(concrete_dims)
      else:
        return None

    return tuple(
      get_shape(dims, i)
      for i, dims in enumerate(zip(*input_shapes))
    )

  def get_output_for(self, *inputs):
    axis = normalize_axis(inputs[0].ndim, self.axis)

    shape = tuple(
      max(dims) if i != axis else None
      for i, dims in enumerate(zip(*(x.shape for x in inputs)))
    )

    return jnp.concatenate([
      jnp.broadcast_to(
        x,
        tuple(s if s is not None else x.shape[i] for i, s, in enumerate(shape))
      ) for x in inputs
    ], axis=self.axis)

class expand_concat(LayerModel):
  LayerType = ExpandConcatLayer

  def __init__(self, axis=-1, name=None):
    super().__init__(axis=axis, name=name)


class BroadcastLayer(Layer):
  def __init__(self, incoming, broadcast_spec, name=None):
    self.broadcast_spec = broadcast_spec
    super(BroadcastLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X):
    return X[self.broadcast_spec]

  def get_output_shape_for(self, input_shape):
    output_shape = []
    current_axis = 0

    for b in self.broadcast_spec:
      if b is None:
        output_shape.append(None)
      else:
        output_shape.append(input_shape[current_axis])
        current_axis += 1

    output_shape.extend(input_shape[current_axis:])
    return tuple(output_shape)

class _broadcast(LayerModel):
  LayerType = BroadcastLayer

  def __init__(self, broadcasting, name=None):
    super(_broadcast, self).__init__(broadcasting, name=name)

class BroadcastExpression(object):
  def __getitem__(self, item):
    return _broadcast(item)

broadcast = BroadcastExpression()


class ElementwiseLayer(Layer):
  @staticmethod
  def operator(*inputs):
    raise NotImplementedError()

  def __init__(self, *incoming, name=None):
    super(ElementwiseLayer, self).__init__(*incoming, name=name)

  def get_output_for(self, *inputs):
    return self.operator(*inputs)

  def get_output_shape_for(self, *input_shapes):
    return input_shapes[0]

class elementwise(LayerModel):
  def __init__(self, name=None):
    super().__init__(name)


class ElementwiseSumLayer(ElementwiseLayer):
  @staticmethod
  def operator(*inputs):
    return functools.reduce(lambda a, b: a + b, inputs)

class elementwise_sum(elementwise):
  LayerType = ElementwiseSumLayer

class ElementwiseMeanLayer(ElementwiseLayer):
  @staticmethod
  def operator(*inputs):
    return ElementwiseSumLayer.operator(*inputs) / len(inputs)

class elementwise_mean(elementwise):
  LayerType = ElementwiseMeanLayer

class ElementwiseMaxLayer(ElementwiseLayer):
  @staticmethod
  def operator(*inputs):
    return functools.reduce(lambda a, b: jnp.maximum(a, b), inputs)

class elementwise_max(elementwise):
  LayerType = ElementwiseMaxLayer

class ElementwiseMinLayer(ElementwiseLayer):
  @staticmethod
  def operator(*inputs):
    return functools.reduce(lambda a, b: jnp.minimum(a, b), inputs)

class elementwise_min(elementwise):
  LayerType = ElementwiseMinLayer

class ElementwiseSoftmaxLayer(ElementwiseLayer):
  @staticmethod
  def operator(alpha, *inputs):
    return soft_maximum(alpha, *inputs)

  def __init__(self, *incoming, alpha=constant_parameter(1.0), name=None):
    super(ElementwiseLayer, self).__init__(
      *incoming,
      parameters=(
        alpha(shape=()),
      ),
      name=name
    )

class elementwise_softmax(LayerModel):
  LayerType = ElementwiseSoftmaxLayer

  def __init__(self, alpha=constant_parameter(1.0), name=None):
    super().__init__(alpha=alpha, name=name)

class ElementwiseSoftminLayer(ElementwiseLayer):
  @staticmethod
  def operator(alpha, *inputs):
    return soft_minimum(alpha, *inputs)

  def __init__(self, *incoming, alpha=constant_parameter(1.0), name=None):
    super(ElementwiseLayer, self).__init__(
      *incoming,
      parameters=(
        alpha(shape=()),
      ),
      name=name
    )

class elementwise_softmin(LayerModel):
  LayerType = ElementwiseSoftminLayer

  def __init__(self, alpha=constant_parameter(1.0), name=None):
    super().__init__(alpha=alpha, name=name)


class GeneralPoolLayer(Layer):
  @staticmethod
  def operator(xs, axis):
    raise NotImplementedError()

  def __init__(self, incoming, axis=(-1, ), name=None):
    self.axis = (axis, ) if isinstance(axis, int) else axis
    super(GeneralPoolLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X):
    return self.operator(X, axis=self.axis)

  def get_output_shape_for(self, input_shape):
    from ..utils.axes import normalize_axis
    normalized_axis = tuple(
      normalize_axis(input_shape, ax)
      for ax in self.axis
    )

    return tuple(
      dim
      for axis, dim in enumerate(input_shape)
      if axis not in normalized_axis
    )

class GeneralPoolModel(LayerModel):
  def __init__(self, axis=(-1, ), name=None):
    super().__init__(axis=axis, name=name)

class GeneralMaxPoolLayer(GeneralPoolLayer):
  @staticmethod
  def operator(xs, axis):
    return jnp.max(xs, axis=axis)

class GeneralMinPoolLayer(GeneralPoolLayer):
  @staticmethod
  def operator(xs, axis):
    return jnp.min(xs, axis=axis)

class GeneralMeanPoolLayer(GeneralPoolLayer):
  @staticmethod
  def operator(xs, axis):
    return jnp.mean(xs, axis=axis)

class GeneralSumPoolLayer(GeneralPoolLayer):
  @staticmethod
  def operator(xs, axis):
    return jnp.sum(xs, axis=axis)

class general_max_pool(GeneralPoolModel):
  LayerType = GeneralMaxPoolLayer

class general_min_pool(GeneralPoolModel):
  LayerType = GeneralMinPoolLayer

class general_mean_pool(GeneralPoolModel):
  LayerType = GeneralMeanPoolLayer

class general_sum_pool(GeneralPoolModel):
  LayerType = GeneralSumPoolLayer


class BatchPoolLayer(Layer):
  @staticmethod
  def operator(X, axis):
    raise NotImplementedError()

  def __init__(self, incoming, axis=(0, ), name=None):
    super(BatchPoolLayer, self).__init__(incoming, name=name)
    self.axis = axis

  def get_output_shape_for(self, input_shape):
    return input_shape

  def get_output_for(self, X):
    averaged = self.operator(X, axis=self.axis)
    return jnp.broadcast_to(averaged, shape=X.shape)

class BatchPoolLayerModel(LayerModel):
  def __init__(self, axis=-2, name=None):
    super().__init__(axis=axis, name=name)

class MeanBatchPoolLayer(BatchPoolLayer):
  @staticmethod
  def operator(X, axis):
    return jnp.mean(X, axis=axis, keepdims=True)

class SumBatchPoolLayer(BatchPoolLayer):
  @staticmethod
  def operator(X, axis):
    return jnp.sum(X, axis=axis, keepdims=True)

class MaxBatchPoolLayer(BatchPoolLayer):
  @staticmethod
  def operator(X, axis):
    return jnp.max(X, axis=axis, keepdims=True)

class mean_batch_pool(BatchPoolLayerModel):
  LayerType = MeanBatchPoolLayer

class sum_batch_pool(BatchPoolLayerModel):
  LayerType = SumBatchPoolLayer

class max_batch_pool(BatchPoolLayerModel):
  LayerType = MaxBatchPoolLayer

class CumSumLayer(Layer):
  def __init__(self, incoming, axis=-2, name=None):
    super(CumSumLayer, self).__init__(incoming, name=name)
    self.axis = axis

  def get_output_shape_for(self, input_shape):
    return input_shape

  def get_output_for(self, X):
    return jnp.cumsum(X, axis=self.axis)

class cumsum(LayerModel):
  LayerType = CumSumLayer

  def __init__(self, axis=-2, name=None):
    super().__init__(axis=axis, name=name)