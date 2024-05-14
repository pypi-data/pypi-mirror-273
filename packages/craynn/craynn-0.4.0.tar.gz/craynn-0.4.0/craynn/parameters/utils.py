__all__ = [
  'combine_properties',
]

def combine_properties(manual_properties, default_properties):
  props = default_properties.copy()
  props.update(manual_properties)

  return props