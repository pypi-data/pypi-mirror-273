import jax
import jax.numpy as jnp

from .meta import Layer, LayerModel

__all__ = [
  'NoiseLayer', 'NoiseLayerModel',
  'GaussianNoiseLayer', 'gaussian_noise',

  'DropoutLayer', 'dropout',
  'RandomExpScalingLayer', 'random_exp_scaling',
  'RandomLogNormScalingLayer', 'random_lognorm_scaling'
]

class NoiseLayer(Layer):
  def operator(self, X: jax.Array, rng: jax.Array):
    raise NotImplementedError()

  def __init__(self, incoming, scale: float=1.0e-2, name=None):
    self.scale = scale

    super(NoiseLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X, rng: jax.Array | None=None):
    if rng is None:
      return X
    else:
      return X + self.scale * self.operator(X, rng)

  def get_output_shape_for(self, input_shape):
    return input_shape

class NoiseLayerModel(LayerModel):
  def __init__(self, scale: float=1.0e-3, name=None):
    super().__init__(scale=scale, name=name)


class GaussianNoiseLayer(NoiseLayer):
  def operator(self, X: jax.Array, rng: jax.Array):
    return X + self.scale * jax.random.normal(rng, shape=X.shape, dtype=X.dtype)

class gaussian_noise(NoiseLayerModel):
  LayerType = GaussianNoiseLayer


class DropoutLayer(Layer):
  def __init__(self, incoming, p=0.2, name=None):
    self.p = p

    super(DropoutLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X, rng=None):
    if rng is None:
      return X
    else:
      mask = jax.random.bernoulli(rng, shape=X.shape, p=1 - self.p)
      return mask * X / (1 - self.p)

  def get_output_shape_for(self, input_shape):
    return input_shape

class dropout(LayerModel):
  LayerType = DropoutLayer

  def __init__(self, p: float=0.2, name=None):
    super().__init__(p=p, name=name)


class RandomExpScalingLayer(Layer):
  def __init__(self, incoming, name=None):
    super(RandomExpScalingLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X, rng: jax.Array | None=None):
    if rng is None:
      return X
    else:
      mask = jax.random.exponential(rng, shape=X.shape, dtype=X.dtype)
      ### mean of exp is 1
      return mask * X

  def get_output_shape_for(self, input_shape):
    return input_shape

class random_exp_scaling(LayerModel):
  LayerType = RandomExpScalingLayer

  def __init__(self, name=None):
    super().__init__(name=name)

class RandomLogNormScalingLayer(Layer):
  def __init__(self, incoming, sigma: float=1.0, name=None):
    import math

    self.sigma = sigma
    self.mean = math.exp(0.5 * sigma * sigma)
    super(RandomLogNormScalingLayer, self).__init__(incoming, name=name)

  def get_output_for(self, X, rng: jax.Array | None=None):
    if rng is None:
      return X
    else:
      mask = jax.random.lognormal(rng, sigma=self.sigma, shape=X.shape, dtype=X.dtype)
      ### mean of exp is 1
      return mask * X / self.mean

  def get_output_shape_for(self, input_shape):
    return input_shape

class random_lognorm_scaling(LayerModel):
  LayerType = RandomLogNormScalingLayer

  def __init__(self, sigma: float=1.0, name=None):
    super().__init__(sigma=sigma, name=name)