__all__ = [
  'achain',
]

def flatten(l):
  if isinstance(l, list):
    return [flatten(x) for x in l]
  else:
    return l

def achain(incoming, definition):
  if not isinstance(incoming, (tuple, list)):
    incoming = (incoming, )

  if not hasattr(definition, '__iter__'):
    try:
      return definition(*incoming)
    except Exception as e:
      raise Exception('An error occurred while try to apply %s to %s' % (definition, incoming)) from e

  elif isinstance(definition, list):
    results = list()

    for op in definition:
      try:
        result = achain(incoming, op)
      except Exception as e:
        raise Exception('An error occurred while try to apply %s to %s' % (op, incoming)) from e

      if isinstance(result, (tuple, list)):
        results.extend(result)
      else:
        results.append(result)

    return results

  elif isinstance(definition, tuple):
    result = incoming

    for op in definition:
      try:
        result = achain(result, op)
      except Exception as e:
        raise Exception('An error occurred while try to apply %s to %s' % (op, result)) from e

    return result

  else:
    raise ValueError('Unknown chain definition: %s' % (definition, ))