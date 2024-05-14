from .meta import Dataset

__all__ = [
  'MappedDataset', 'ZippedDataset'
]

class MappedDataset(Dataset):
  def __init__(self, dataset : Dataset, f):
    self.f = f
    self.dataset = dataset

    super(MappedDataset, self).__init__()

  def __getitem__(self, item):
    result = self.f(*self.dataset[item])

    if isinstance(result, (tuple, list)):
      return result
    else:
      return (result, )

  def get_subset(self, item):
    return self.dataset.subset(item).map(self.f)

  def size(self):
    return self.dataset.size()

  def materialize(self, batch_size=1, jit=True):
    from .utils import xmap

    result = xmap(
      self.f,
      self.dataset.indexed_seq(batch_size=batch_size),
      jit=jit
    )

    if isinstance(result, (tuple, list)):
      return result
    else:
      return (result, )

  def shapes(self):
    size = len(self.dataset)
    probe = self[:1]

    return tuple(
      (size, ) + p.shape[1]
      for p in probe
    )


class ZippedDataset(Dataset):
  def __init__(self, first: Dataset, second: Dataset):
    self.first = first
    self.second = second

    super(ZippedDataset, self).__init__()

  def __getitem__(self, item):
    return *self.first[item], *self.second[item]

  def get_subset(self, item):
    return self.first.subset(item).zip(self.second.subset(item))

  def size(self):
    return self.first.size()

  def materialize(self, batch_size=1, jit=True):
    return *self.first.materialize(batch_size=batch_size, jit=True), \
           *self.first.materialize(batch_size=batch_size, jit=True)

  def shapes(self):
    return *self.first.shapes(), *self.second.shapes()