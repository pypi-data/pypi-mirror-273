import functools

import jax
import jax.numpy as jnp

__all__ = [
  'gsum', 'soft_maximum', 'soft_minimum'
]

def gsum(*xs):
  return functools.reduce(
    lambda a, b: a + b,
    xs
  )

def soft_maximum(alpha, *xs):
  m = functools.reduce(lambda a, b: jnp.maximum(a, b), xs)
  normed = [x - m for x in xs]
  coefs = [jnp.exp(alpha * x_) for x_ in normed]
  total = gsum(coefs)

  return gsum(c * x / total for c, x in zip(coefs, xs))

def soft_minimum(alpha, *xs):
  return soft_maximum(-alpha, *xs)