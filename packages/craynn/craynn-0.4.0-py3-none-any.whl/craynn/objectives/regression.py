from typing import Optional

import jax
import jax.nn as jnn
import jax.numpy as jnp

__all__ = [
  'mse', 'mae',
  'gm_neg_log_likelihood',
]

def mse(target: jax.Array, predictions: jax.Array, axes: int | tuple[int, ...] | None=None):
  assert len(target.shape) == len(predictions.shape), 'target and predictions have different dimensionality'
  if axes is None:
    axes = range(1, target.ndim)

  return jnp.mean(jnp.square(target - predictions), axis=axes)

def mae(target: jax.Array, predictions: jax.Array, axes: int | tuple[int, ...] | None=None):
  assert len(target.shape) == len(predictions.shape), 'target and predictions have different dimensionality'
  if axes is None:
    axes = range(1, target.ndim)

  return jnp.mean(jnp.abs(target - predictions), axis=axes)


def gm_neg_log_likelihood(
  target: jax.Array,
  means: jax.Array, log_sigmas: jax.Array, logit_priors: jax.Array | None=None
):
  """
  Gaussian Mixture (GM) negative log likelihood, analogous to MSE but for multi-trend predictions.

  :param target: targets, array of shape `(*, )`
  :param means: predicted means of GM components, array of shape `(*, k)`
  :param log_sigmas: log sigma of each GM component, array of shape `(*, k)`
  :param logit_priors: if not None, logits of mixture components' probabilities, array of shape `(k, )`
    otherwise, components are assumed to be equally probable
  :return: negative log likelihood
  """
  inv_sigmas = jnp.exp(-log_sigmas)
  se = jnp.square((target[..., None] - means) * inv_sigmas)

  if logit_priors is None:
    neg_log_likelihoods = -jnn.logsumexp(
      -log_sigmas - 0.5 * se,
      axis=-1
    )
  else:
    neg_log_likelihoods = -jnn.logsumexp(
      -log_sigmas - 0.5 * se + jnn.log_softmax(logit_priors),
      axis=-1
    )

  return neg_log_likelihoods