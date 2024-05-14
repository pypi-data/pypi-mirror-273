import jax

from .meta import Dataset
from .array import ArrayDataset

__all__ = [
  'SlicedSubset',
  'IndexedSubset'
]

class SlicedSubset(ArrayDataset):
  def __init__(self, dataset : Dataset, item):
    super(SlicedSubset, self).__init__(*(
      d[item] for d in dataset.materialize()
    ))

class IndexedSubset(Dataset):
  def __init__(self, dataset : Dataset, indx):
    self.indx = jax.numpy.array(indx, dtype=jax.numpy.int32)
    self.dataset = dataset

    super(IndexedSubset, self).__init__()

  def __getitem__(self, item):
    subindx = self.indx[item]
    return self.dataset[subindx]

  def size(self):
    return self.indx.shape[0]

  def materialize(self, batch_size=1, jit=True):
    return tuple(
      d[self.indx] for d in self.dataset.materialize(batch_size=batch_size, jit=jit)
    )

  def shapes(self):
    size = self.size()
    return tuple(
      (size, ) + shape[1:]
      for shape in self.dataset.shapes()
    )