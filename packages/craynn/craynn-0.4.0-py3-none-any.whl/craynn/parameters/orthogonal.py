### inspired by https://github.com/Lasagne/Lasagne/blob/master/lasagne/init.py#L327-L367
### Copyright (c) 2014-2015 Lasagne contributors, (c) 2020 Maxim Borisyak

import math
import jax
import jax.numpy as jnp

from .common import RandomInit, RandomInitModel

__all__ = [
  'OrthogonalInit', 'orthogonal_init'
]

class OrthogonalInit(RandomInit):
  def sample(self, rng: jax.Array, shape: tuple[int, ...]=(), dtype: jnp.dtype=float):
    matrix_shape = (shape[0], math.prod(shape[1:]))

    R = jax.random.normal(rng, shape=matrix_shape, dtype=dtype)
    u, _, v = jnp.linalg.svd(R, full_matrices=False)
    W = (u if matrix_shape[0] > matrix_shape[1] else v)

    return W.reshape(shape)

class orthogonal_init(RandomInitModel):
  ParameterType = OrthogonalInit

