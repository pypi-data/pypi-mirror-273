import jax

from .meta import Parameter, ParameterModel
from .defaults import default_weight_init

__all__ = [
  'NoisyParameter', 'noisy_parameter'
]

class NoisyParameter(Parameter):
  def __init__(self, shape, eps=1e-3, w=default_weight_init, name=None, **properties):
    self.eps = eps

    self.w = w(
      shape=shape, **properties,
      name=(name + '_w') if name is not None else None
    )

    super(NoisyParameter, self).__init__(
      self.w, shape=shape, name=name,
      **properties
    )

  def get_output_for(self, w, rng: jax.Array):
    if rng is None:
      return w
    else:
      return w + self.eps * jax.random.normal(rng, shape=w.shape, dtype=w.dtype)

  def get_output_shape_for(self, w_shape):
    return w_shape

class noisy_parameter(ParameterModel):
  ParameterType = NoisyParameter

  def __init__(self, eps=1e-3, w=default_weight_init, name=None, composite=True, **properties):
    super().__init__(dict(**properties, composite=composite), eps=eps, w=w, name=name)
