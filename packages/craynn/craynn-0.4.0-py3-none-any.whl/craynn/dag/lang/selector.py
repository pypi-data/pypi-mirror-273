from ..meta import get_name, GraphModel
from .. import evaluate

__all__ = [
  'IdentityStatement',
  'SelectStatement'
]

class IdentityStatement(GraphModel):
  def __call__(self, *incoming):
    return incoming

class Selector(GraphModel):
  def __init__(self, items, definition, achain, search_subgraph=False, replace=False):
    self.items = items
    self.search_subgraph = search_subgraph
    self.replace = replace
    self.op = achain(*definition)

  def __call__(self, *incoming):
    selected, index = _select(self.items, incoming, search_subgraph=self.search_subgraph)
    result = self.op(*selected)

    if self.replace:
      return _replace(incoming, index, result)
    else:
      return result


def _select(items, incoming, search_subgraph=False):
  results = []
  selected_index = [False, ] * len(incoming)
  index = list(range(len(incoming)))

  for item in items:
    if isinstance(item, int):
      results.append(incoming[item])
      selected_index[item] = True

    elif isinstance(item, slice):
      results.extend(incoming[item])
      for i in index[item]:
        selected_index[i] = True

    elif isinstance(item, str):
      if search_subgraph:
        matched = evaluate.filter(lambda n: n.name == item, incoming)
        if len(matched) == 0:
          raise ValueError('There is not any nodes named %s' % (item, ))
        else:
          results.extend(matched)

        for i, node in enumerate(incoming):
          if get_name(node) == item:
            selected_index[i] = True
      else:
        for i, node in enumerate(incoming):
          if get_name(node) == item:
            selected_index[i] = True
            results.append(node)

    else:
      raise ValueError('Items must be integers, slices or node names, got %s' % (item, ))

  return results, selected_index

def _replace(inputs, selection, op_results):
  op_index = 0
  results = []

  if not isinstance(op_results, (tuple, list)):
    if all(selection):
      return op_results
    else:
      op_results = (op_results, )

  for i, is_selected in enumerate(selection):
    if is_selected:
      if op_index < len(op_results):
        results.append(op_results[op_index])
        op_index += 1
      else:
        continue
    else:
      results.append(inputs[i])

  for i in range(op_index, len(op_results)):
    results.append(op_results[i])

  return results

class SelectModel(GraphModel):
  def __init__(self, *items, achain, search_subgraph=False, replace=False):
    self.items = items
    self.achain = achain
    self.search_subgraph = search_subgraph
    self.replace = replace

  def __call__(self, *definition):
    return Selector(
      self.items, definition,
      achain=self.achain,
      search_subgraph=self.search_subgraph,
      replace=self.replace
    )

  def __str__(self):
    return 'select({items})'.format(
      items=', '.join([str(x) for x in self.items])
    )

  def __repr__(self):
    return 'select({items}, search={search}, replace={replace})'.format(
      items=', '.join([str(x) for x in self.items]),
      search=self.search_subgraph,
      replace=self.replace
    )

class SelectStatement(object):
  def __init__(self, achain, search_subgraph=False, replace=False):
    self.search_subgraph = search_subgraph
    self.achain = achain
    self.replace = replace

  def __call__(self, *items):
    return SelectModel(*items, achain=self.achain, search_subgraph=self.search_subgraph, replace=self.replace)

  def __getitem__(self, items):
    if not isinstance(items, tuple):
      items = (items, )

    return self(*items)