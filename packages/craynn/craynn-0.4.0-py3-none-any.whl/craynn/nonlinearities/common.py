import jax
import jax.numpy as jnp
import jax.nn as jnn

from .meta import Nonlinearity

__all__ = [
  'sigmoid',
  'leaky_sigmoid',
  'tanh',
  'leaky_tanh',
  'relu',
  'leaky_relu',
  'softplus',
  'softmax',
  'elu',
  'silu',
  'gelu',
  'linear',
  'gaussian',
  'square'
]

class sigmoid(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.sigmoid(x)

class tanh(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.tanh(x)

class leaky_sigmoid(Nonlinearity):
  def __init__(self, leakiness: float=0.05):
    self.leakiness = leakiness
    super().__init__(leakiness=leakiness)

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.sigmoid(x) + self.leakiness * x

class leaky_tanh(Nonlinearity):
  def __init__(self, leakiness: float=0.05):
    self.leakiness = leakiness
    super().__init__(leakiness=leakiness)

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.tanh(x) + self.leakiness * x

class relu(Nonlinearity):
  name = 'ReLU'

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.relu(x)

class leaky_relu(Nonlinearity):
  name = 'leaky_ReLU'

  def __init__(self, leakiness: float=0.05):
    self.leakiness = leakiness
    super().__init__(leakiness=leakiness)

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.leaky_relu(x, negative_slope=self.leakiness)

class softplus(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.softplus(x)

class softmax(Nonlinearity):
  def __init__(self, axis: int | tuple[int, ...] | None = -1):
    self.axis = axis
    super().__init__(axis=axis)

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.softmax(x, axis=self.axis)

class elu(Nonlinearity):
  name = 'ELU'

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.elu(x)

class silu(Nonlinearity):
  name = 'SiLU'

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.silu(x)

class gelu(Nonlinearity):
  name = 'GELU'

  def __call__(self, x: jax.Array) -> jax.Array:
    return jnn.gelu(x)

class linear(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return x

class gaussian(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return jnp.exp(-jnp.square(x))

class square(Nonlinearity):
  def __call__(self, x: jax.Array) -> jax.Array:
    return 1 - jnp.square(x)