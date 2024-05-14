import jax

__all__ = [
  'Nonlinearity'
]


class Nonlinearity(object):
  name: str = None

  def __init__(self, **hyperparameters):
    self.hyperparameters = hyperparameters
    
    super(Nonlinearity, self).__init__()

  def __call__(self, x: jax.Array) -> jax.Array:
    raise NotImplementedError()

  def __str__(self):
    return '%s(%s)' % (
      self.__class__.__name__ if self.name is None else self.name,
      ', '.join([
        '%s=%s' % (k, v) for k, v in self.hyperparameters.items()
      ])
    )