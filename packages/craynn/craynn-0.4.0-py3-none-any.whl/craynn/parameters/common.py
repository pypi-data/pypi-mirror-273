import jax
import jax.numpy as jnp

from .meta import Parameter, ParameterModel, FreeParameter

__all__ = [
  'ConstantParameter', 'constant_parameter',

  'ZerosInit', 'zeros_init',
  'OnesInit', 'ones_init',

  'RandomInit', 'RandomInitModel',
  'NormalInit', 'normal_init',
  'UniformInit', 'uniform_init',
  'LaplaceInit', 'laplace_init',
  
  'ConstInit', 'const_init',
]

class ConstantParameter(Parameter):
  def __init__(self, shape, value, name=None, **properties):
    dtype = getattr(value, 'dtype', jnp.float32)
    self.value = jnp.array(value, dtype=dtype)

    super(ConstantParameter, self).__init__(shape=value.shape, name=name, **properties)

  def get_output_for(self,):
    return self.value

class constant_parameter(ParameterModel):
  ParameterType = ConstantParameter

  def __init__(self, value, name=None, **properties):
    super().__init__(properties, value, name=name)


class ZerosInit(FreeParameter):
  def get_output_for(self):
    return jnp.zeros(shape=self.shape, dtype=self.dtype)

class zeros_init(ParameterModel):
  ParameterType =  ZerosInit

  def __init__(self, name=None, dtype: jnp.dtype=float, **properties):
    super().__init__(properties, dtype=dtype, name=name)


class OnesInit(FreeParameter):
  def get_output_for(self):
    return jnp.ones(shape=self.shape, dtype=self.dtype)

class ones_init(ParameterModel):
  ParameterType = OnesInit

  def __init__(self, name=None, dtype: jnp.dtype=float, **properties):
    super().__init__(properties, dtype=dtype, name=name)

class RandomInit(FreeParameter):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    raise NotImplementedError()

  def __init__(self, shape=(), gain: float=1, dtype: jnp.dtype=jnp.float32, name=None, **properties):
    self.gain = gain
    super(RandomInit, self).__init__(shape=shape, name=name, dtype=dtype, **properties)

  def get_output_for(self, rng: jax.Array):
    return self.gain * self.sample(rng, shape=self.shape, dtype=self.dtype)

class RandomInitModel(ParameterModel):
  def __init__(self, gain: float=1, dtype: jnp.dtype=jnp.float32, name=None, **properties):
    super().__init__(properties, gain=gain, dtype=dtype, name=name)

class NormalInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    return jax.random.normal(rng, shape=shape, dtype=dtype)

class UniformInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    return jax.random.uniform(rng, minval=-0.5, maxval=0.5, shape=shape, dtype=dtype)

class LaplaceInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    return jax.random.laplace(rng, shape=shape, dtype=dtype)

class normal_init(RandomInitModel):
  ParameterType = NormalInit

class uniform_init(RandomInitModel):
  ParameterType = UniformInit

class laplace_init(RandomInitModel):
  ParameterType = UniformInit


class ConstInit(FreeParameter):
  def __init__(self, shape, value, dtype: jnp.dtype=jnp.float32, name=None, **properties):
    super(ConstInit, self).__init__(shape=shape, name=name, dtype=dtype, **properties)

    if not hasattr(value, 'shape'):
      value = jnp.asarray(value, dtype=dtype)

    assert len(value.shape) <= len(shape), \
      'the provided value has larger dimensionality than the requested shape ' \
      '(%d vs %d)' % (len(value.shape), len(shape))

    ndim = len(value.shape)
    assert all(sdim % vdim == 0 for sdim, vdim in zip(shape[-ndim:], value.shape)), \
      'the provided value (%s) does not match the last dimensions of the requested shape (%s)' % (value.shape, shape)

    if ndim == 0:
      repeats = shape
    else:
      repeats = shape[:-ndim] + tuple(sdim // vdim == 0 for sdim, vdim in zip(shape[-ndim:], value.shape))

    self.value = jnp.tile(value, repeats)

  def get_output_for(self):
    return self.value

class const_init(ParameterModel):
  ParameterType = ConstInit

  def __init__(self, value, dtype: jnp.dtype=jnp.float32, name=None, **properties):
    super().__init__(properties, value, dtype, name=name)