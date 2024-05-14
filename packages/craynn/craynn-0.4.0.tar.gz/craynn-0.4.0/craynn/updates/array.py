import jax

from .meta import Dataset

__all__ = [
  'ArrayDataset',
  'array_dataset',
]

class ArrayDataset(Dataset):
  def __init__(self, *arrays):
    self._arrays = arrays
    if len(set(arr.shape[0] for arr in arrays)) > 1:
      import warnings
      warnings.warn(
        'Arrays\' sizes are not consistent: %s, '
        'this might lead to unexpected behaviour.' % (
          ','.join(str(arr.shape[0]) for arr in arrays),
        )
      )

    self._size = min(arr.shape[0] for arr in self._arrays)
    super(ArrayDataset, self).__init__()

  def __getitem__(self, item):
    return tuple(
      arr[item] for arr in self._arrays
    )

  def size(self):
    return self._size

  def materialize(self, batch_size=1, jit=True):
    return self._arrays

  def shapes(self):
    return tuple(arr.shape for arr in self._arrays)

def array_dataset(*data):
  dataset = ArrayDataset(*(
    jax.numpy.asarray(d) for d in data
  ))
  return dataset