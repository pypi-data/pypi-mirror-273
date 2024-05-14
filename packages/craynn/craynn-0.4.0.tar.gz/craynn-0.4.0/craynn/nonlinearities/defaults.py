from .common import sigmoid, leaky_relu

__all__ = [
  'default_semibounded_nonlinearity',
  'default_bounded_nonlinearity',
  'default_nonlinearity'
]

default_bounded_nonlinearity = sigmoid()

### well, leaky relu is not exactly semi-bounded...
default_semibounded_nonlinearity = leaky_relu()

default_nonlinearity = leaky_relu()