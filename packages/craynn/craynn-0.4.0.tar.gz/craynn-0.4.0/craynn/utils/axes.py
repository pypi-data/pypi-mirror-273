__all__ = [
  'normalize_axis',
  'check_shape_consistency',
]

def normalize_axis(tensor_or_dim, axis):
  if isinstance(tensor_or_dim, int):
    dim = tensor_or_dim
  elif isinstance(tensor_or_dim, tuple):
    dim = len(tensor_or_dim)
  else:
    dim = len(tensor_or_dim.shape)

  if isinstance(axis, int):
    return axis % dim
  else:
    return tuple(a % dim for a in axis)

def check_shape_consistency(concrete_shape, abstract_shape):
  return all(
    sc == sa or sa is None
    for sc, sa in zip(concrete_shape, abstract_shape)
  )