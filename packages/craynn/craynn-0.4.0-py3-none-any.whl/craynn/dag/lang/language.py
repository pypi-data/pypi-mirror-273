from ..meta import GraphModel

from .achain import achain as achain_op
from .selector import SelectStatement, IdentityStatement

__all__ = [
  'achain',
  'repeat',
  'for_each',
  'with_inputs',
  'select',
  'seek',
  'identity'
]

class achain(GraphModel):
  def __init__(self, *definition):
    self.definition = definition

  def __call__(self, *incoming):
    return achain_op(incoming, self.definition)

class _repeat(GraphModel):
  def __init__(self, n, *definition):
    self.n = n
    self.definition = definition

  def __call__(self, *incoming):
    return achain(self.definition * self.n)(*incoming)

def repeat(n):
  def f(*definition):
    return _repeat(n, *definition)
  return f

class for_each(GraphModel):
  def __init__(self, *definition):
    self.definition = definition

  def __call__(self, *incoming):
    return [
      achain(self.definition)(node)
      for node in incoming
    ]

identity = IdentityStatement()

select = SelectStatement(
  achain=achain,
  search_subgraph=False,
  replace=False
)

seek = SelectStatement(
  achain=achain,
  search_subgraph=True,
  replace=False
)

with_inputs = SelectStatement(
  achain=achain,
  search_subgraph=False,
  replace=True
)