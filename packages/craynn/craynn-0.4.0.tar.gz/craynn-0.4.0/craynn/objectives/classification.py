import jax
import jax.nn as jnn
import jax.numpy as jnp

__all__ = [
  'logit_binary_crossentropy', 'logit_categorical_crossentropy',
  'binary_crossentropy', 'categorical_crossentropy',

  'concat_binary'
]

def logit_binary_crossentropy(target: jax.Array, predictions: jax.Array):
  """
  Numerically stable cross-entropy loss for binary logit predictions.

  :param target: 0-1 vector of the class labels;
  :param predictions: logit predictions;
  :return: binary cross-entropy loss for each sample.
  """
  return target * jnn.softplus(-predictions) + (1 - target) * jnn.softplus(predictions)


def logit_categorical_crossentropy(target: jax.Array, predictions: jax.Array):
  """
  Numerically stable cross-entropy loss for categorical logit predictions.

  :param target: one-hot encoded labels of shape `(*, num classes)`;
  :param predictions: logit predictions of shape `(*, num classes)`;
  :return: cross-entropy loss for each sample.
  """
  ### seems like reduce_logsumexp can safely handle large values.
  neg_log_softmax = jnn.logsumexp(predictions, axis=-1)[..., None] - predictions

  return jnp.sum(target * neg_log_softmax, axis=-1)

def binary_crossentropy(target: jax.Array, predictions: jax.Array, eps: float | None=None):
  """
  Cross-entropy loss for binary predictions.
  If possible, prefer `logit_binary_crossentropy` as it is a more numerically stable function.

  :param target: 0-1 labels;
  :param predictions: probability estimations for `target = 1`, must be in `[0, 1]`;
  :param eps: a small constant added to predictions for numerical stability, ignored if it is `None`;
  :return: cross-entropy loss for each sample.
  """

  if eps is None:
    return target * jnp.log(predictions) + (1 - target) * jnp.log(1 - predictions)
  else:
    return target * jnp.log(predictions + eps) + (1 - target) * jnp.log(1 - predictions + eps)


def categorical_crossentropy(target: jax.Array, predictions: jax.Array, eps: float | None=None):
  """
  Cross-entropy loss for categorical predictions.
  If possible, prefer `logit_categorical_crossentropy` as it is a more numerically stable function.

  :param target: one-hot encoded labels of shape `(*, num classes)`;
  :param predictions: predictions of shape `(*, num classes)`, must sum to 1;
  :param eps: a small constant added to predictions for numerical stability, ignored if it is `None`;
  :return: cross-entropy loss for each sample.
  """

  if eps is None:
    return jnp.sum(target * jnp.log(predictions), axis=-1)
  else:
    return jnp.sum(target * jnp.log(predictions + eps), axis=-1)


def concat_binary(X_neg, X_pos, keep_priors=True):
  """
  A utility function that converts negative and positive samples into samples + labels.
  Helpful, for example, for implementing GANs:

      X_neg = generator(Z)
      X_pos = <sample from a dataset>
      X, y, w = concat_binary(X_neg, X_pos, keep_priors)
      p = discriminator(X)
      loss = jnp.mean(w * logit_binary_crossentropy(y, p)) / jnp.mean(w)

  :param X_neg: negative samples batch;
  :param X_pos: positive samples batch;
  :param keep_priors: if False, returns weights to even the contribution of each class, otherwise, returns None;
  :return: concatenated samples, labels, either weights (if `keep_priors=True`) or None.
  """
  X = jnp.concatenate([X_neg, X_pos], axis=0)

  target = jnp.concatenate([
    jnp.zeros(shape=(X_neg.shape[0], ), dtype=X_neg.dtype),
    jnp.zeros(shape=(X_pos.shape[0], ), dtype=X_pos.dtype),
  ], axis=0)

  if not keep_priors:
    n_neg = X_neg.shape[0]
    n_pos = X_pos.shape[0]

    total = n_neg + n_pos

    w_neg = 0.5 * total / n_neg
    w_pos = 0.5 * total / n_pos

    weights = jnp.concatenate([
      w_neg * jnp.ones(shape=(X_neg.shape[0], ), dtype=X_neg.dtype),
      w_pos * jnp.ones(shape=(X_pos.shape[0], ), dtype=X_neg.dtype),
      ])
  else:
    weights = None

  return X, target, weights
