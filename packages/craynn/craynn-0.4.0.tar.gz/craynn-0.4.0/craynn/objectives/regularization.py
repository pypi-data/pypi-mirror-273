from collections.abc import Mapping, Sequence
import jax.numpy as jnp

__all__ = [
  'l2_reg',
  'l1_reg',
]

def l2_reg(params, mean=False):
  """
  L2 regularization.

  :param params: parameters;
  :param mean: if True, average penalty within each variable.
  """
  reduce = jnp.mean if mean else jnp.sum

  if isinstance(params, Mapping):
    variables = params.values()

  elif isinstance(params, Sequence):
    variables = params

  else:
    variables = (params, )

  return sum(
    reduce(jnp.square(W)) for W in variables
  )

def l1_reg(params, mean=False):
  """
  L1 regularization.

  :param params: parameters;
  :param mean: if True, average penalty within each variable.
  """
  reduce = jnp.mean if mean else jnp.sum

  if isinstance(params, Mapping):
    variables = params.values()
  elif isinstance(params, (list, tuple)):
    variables = params
  else:
    variables = (params,)

  return sum(
    reduce(jnp.abs(W)) for W in variables
  )