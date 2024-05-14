import math

import jax
import jax.numpy as jnp

from .common import RandomInit, RandomInitModel

__all__ = [
  'glorot_scaling',
  'GlorotNormalInit', 'glorot_normal_init',
  'GlorotUniformInit', 'glorot_uniform_init',
]

SQRT3 = math.sqrt(3)

def glorot_scaling(shape):
  in_units, out_units = shape[-2:]
  receptive_field_area = math.prod(shape[:-2])

  return jnp.sqrt(2.0 / (in_units + out_units) / receptive_field_area)

class GlorotNormalInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    if len(shape) < 2:
      return self.gain * jax.random.normal(rng, shape=shape, dtype=dtype)
    else:
      scale = glorot_scaling(shape)
      return self.gain * scale * jax.random.normal(rng, shape=shape, dtype=dtype)

class GlorotUniformInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    if len(shape) < 2:
      return self.gain * jax.random.uniform(rng, shape=shape, minval=-SQRT3, maxval=SQRT3, dtype=dtype)
    else:
      scale = SQRT3 * glorot_scaling(shape)
      return self.gain * jax.random.uniform(rng, shape=shape, minval=-scale, maxval=scale, dtype=dtype)

class glorot_normal_init(RandomInitModel):
  ParameterType = GlorotNormalInit

class glorot_uniform_init(RandomInitModel):
  ParameterType = GlorotUniformInit
