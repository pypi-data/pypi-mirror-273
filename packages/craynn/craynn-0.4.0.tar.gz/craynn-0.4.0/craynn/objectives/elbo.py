import jax
import jax.numpy as jnp

__all__ = [
  'elbo'
]

def elbo(
  X_original: jax.Array, X_reconstructed: jax.Array, latent_mean: jax.Array, latent_std: jax.Array,
  sigma_reconstructed: float=1.0, beta: float | None=None, exact: bool=False,
  axes: tuple[int, ...] | int | None=None
):
  """
  Returns Evidence Lower Bound for normally distributed (z | X), (X | z) and z:
    P(z | X) = N(`latent_mean`, `latent_std`);
    P(X | z) = N(`X_reconstructed`, `sigma_reconstructed`);
    P(z) = N(0, 1).

  :param X_original: ground-truth sample;
  :param X_reconstructed: reconstructed sample;
  :param latent_mean: estimated mean of the posterior P(z | X);
  :param latent_std: estimated sigma of the posterior P(z | X);
  :param sigma_reconstructed: variance for reconstructed sample, i.e. X | z ~ N(X_original, sigma_reconstructed)
    If a scalar, `Var(X | z) = sigma_reconstructed * I`, if tensor then `Var(X | z) = diag(sigma_reconstructed)`
  :param beta: coefficient for beta-VAE
  :param exact: if true returns exact value of ELBO, otherwise returns rearranged ELBO equal to the original
    up to a multiplicative constant, possibly increasing computational stability for low `sigma_reconstructed`.
  :param axes: axes of reduction for samples, typically, all axes except for batch ones, if `None` all axes expect
    for the first one. Latent batch axes are considered the same as the sample batch axes.

  :return: Evidence Lower Bound (renormalized, if `exact=False`).
  """

  if beta is None:
    ### posterior_penalty below is missing 1/2 coefficient.
    beta = 0.5
  else:
    beta = beta / 2

  if exact:
    normalization = jnp.array(0.5 / jnp.square(sigma_reconstructed), dtype=jnp.float32)
  else:
    normalization = jnp.array(2 * beta * jnp.square(sigma_reconstructed), dtype=jnp.float32)

  if axes is None:
    sample_axes = range(1, X_original.ndim)
    latent_axes = range(1, latent_mean.ndim)
  else:
    sample_axes = axes
    sample_batch_axes = tuple(i for i in range(X_original.ndim) if i not in sample_axes)
    latent_axes = tuple(i for i in range(latent_mean.ndim) if i not in sample_batch_axes)

  reconstruction_loss = jnp.mean(jnp.square(X_original - X_reconstructed), axis=sample_axes)

  posterior_penalty = jnp.mean(
    jnp.square(latent_std) + jnp.square(latent_mean) - 2 * jnp.log(latent_std),
    axis=latent_axes
  )

  if exact:
    return normalization * reconstruction_loss + beta * posterior_penalty
  else:
    return reconstruction_loss + normalization * posterior_penalty
