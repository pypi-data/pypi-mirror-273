import jax

__all__ = [
  'Dataset'
]

class Dataset(object):
  def __init__(self):
    ### allows nice `dataset.subset[:100] syntax`
    self.subset = SubsetConstructor(self)

  def __getitem__(self, item):
    raise NotImplementedError()

  def size(self):
    raise NotImplementedError()

  def __len__(self):
    return int(self.size())

  def materialize(self, batch_size=1, jit=True):
    raise NotImplementedError()

  def shapes(self):
    raise NotImplementedError()

  def get_subset(self, item):
    from .subsets import SlicedSubset, IndexedSubset
    if isinstance(item, slice):
      return SlicedSubset(self, item)
    else:
      return IndexedSubset(self, item)

  def seq(self, batch_size=1):
    from .utils import sliced_seq

    if batch_size is None:
      for i in range(len(self)):
        yield self[i]

    else:
      for indx in sliced_seq(self.size(), batch_size=batch_size):
        yield self[indx]

  def indexed_seq(self, batch_size=1):
    from .utils import sliced_seq

    if batch_size is None:
      for i in range(len(self)):
        yield i, self[i]

    else:
      for indx in sliced_seq(self.size(), batch_size=batch_size):
        yield indx, self[indx]

  def batch(self, rng, size=1):
    if size is None:
      indx = jax.random.randint(
        rng, shape=(), dtype=jax.numpy.int32, minval=0, maxval=self.size()
      )

    else:
      indx = jax.random.randint(
        rng, shape=(size, ), dtype=jax.numpy.int32, minval=0, maxval=self.size()
      )

    return self[indx]

  def eval(self, f=None, batch_size=1, jit=True):
    if f is None:
      return self.materialize(batch_size=batch_size, jit=jit)
    else:
      return self.map(f).materialize(batch_size=batch_size, jit=jit)

  def map(self, f):
    from .common import MappedDataset
    return MappedDataset(self, f)

  def zip(self, other):
    from .common import ZippedDataset
    return ZippedDataset(self, other)


class SubsetConstructor(object):
  def __init__(self, dataset : Dataset):
    self.dataset = dataset

  def __getitem__(self, item):
    return self(item)

  def __call__(self, item):
    if isinstance(item, int):
      item = slice(item, item + 1) if item != -1 else slice(item, None)

    return self.dataset.get_subset(item)