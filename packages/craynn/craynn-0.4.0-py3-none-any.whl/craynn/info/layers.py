import math
import numpy as np

from .. import dag

from ..layers import Layer, get_layers
from ..parameters import Parameter, FreeParameter, get_all_free_parameters, get_parameters

__all__ = [
  'get_number_of_parameters',
  'get_total_number_of_parameters',
  'graph_description',
  'get_network_core'
]

def _get_number_of_parameters(layer):
  if isinstance(layer, FreeParameter):
    return math.prod(layer.shape)
  else:
    return 0

def get_number_of_parameters(layer_or_layers):
  def incoming(node: dag.Node):
    if isinstance(node, Layer):
      return node.parameters
    else:
      return node.incoming

  def reducer(layer, inputs):
    own_variables = _get_number_of_parameters(layer)
    num_parameters = len(getattr(layer, 'parameters', ()))

    if num_parameters > 0:
      return sum(inputs[:num_parameters]) + own_variables
    else:
      return own_variables

  return dag.reduce(reducer, layer_or_layers)

def get_total_number_of_parameters(layer, **properties):
  variables = get_all_free_parameters(layer, **properties)

  return sum(
    np.prod(var.shape, dtype='int64')
    for var in variables
  )

def get_attributes(layer, attributes):
  values = dict()

  for name, attr in attributes.items():
    if type(attr) is str:
      if hasattr(layer, attr):
        values[name] = getattr(layer, attr)

    elif callable(attr):
      values[name] = attr(layer)

  return values

def param_description(param):
  return '{name} {shape}: {properties}'.format(
    name=dag.get_name(param),
    shape=tuple(param.shape),
    properties=', '.join(
      '%s=%s' % (k, v)
      for k, v in getattr(param, 'properties', dict()).items()
    )
  )

def layer_description(layer, attributes, short=True):
  attrs = get_attributes(layer, attributes)
  additional = [ '%s=%s' % (k, v) for k, v in attrs.items() ]

  number_of_parameters = get_number_of_parameters(layer)
  output_shape = dag.get_output_shape(layer)

  if short:
    return '{name}{clazz} ({nparams} params): {out_shape}{additional}'.format(
      name='' if dag.get_name(layer) is None else ('%s ' % dag.get_name(layer)),
      clazz=layer.__class__.__name__,
      out_shape=output_shape,
      nparams=number_of_parameters,
      additional='' if len(additional) == 0 else ('\n  %s' % ', '.join(additional))
    )
  else:
    head = '{name}{clazz}: {out_shape}{additional}'.format(
      name='' if dag.get_name(layer) is None else ('%s ' % dag.get_name(layer)),
      clazz=layer.__class__.__name__,
      out_shape=output_shape,
      additional='' if len(additional) == 0 else ('\n  %s' % '\n  '.join(additional))
    )

    params = get_parameters(layer)
    if len(params) == 0:
      return head
    else:
      params_info ='\n  '.join([
        param_description(param)
        for param in params
      ])

      total_number_of_params = 'number of params: %d' % (number_of_parameters, )

      return '{head}\n  {params}\n  {total}'.format(
        head=head,
        params=params_info,
        total=total_number_of_params
      )

def graph_description(layer_or_layers, short=True, inputs=None, **attributes):
  all_layers = get_layers(layer_or_layers)

  if inputs is None:
    inputs = [
      layer
      for layer in all_layers
      if len(getattr(layer, 'incoming', tuple)()) == 0
    ]

  outputs = layer_or_layers

  input_summary = ', '.join(
    '{shape}'.format(shape=dag.get_output_shape(layer))
    if dag.get_name(layer) is None else
    '{name}: {shape}'.format(name=dag.get_name(layer), shape=dag.get_output_shape(layer))

    for layer in inputs
  )

  output_summary = ', '.join(
    '{shape}'.format(shape=dag.get_output_shape(layer))
    for layer in outputs
  )

  layer_delim = '\n' if short else '\n\n'

  layers_info = layer_delim.join(
    layer_description(
      layer,
      attributes=attributes,
      short=short
    )
    for layer in all_layers
  )

  summary = '{input_summary} -> {output_summary}\n{total}\n{sep}\n{layers_description}'.format(
    input_summary=input_summary,
    total='total number of params: %d' % get_total_number_of_parameters(layer_or_layers),
    sep='=' * 32,
    output_summary=output_summary,
    layers_description=layers_info
  )

  return summary

def get_network_core(layers):
  """
  Network dag, in this case, is a network with parameters
  that does not depend on any `Layer` excluded.
  :param layers: an instance of `Layer` or a list/tuple of `Layer`s
  :return: collection of Layers included in the network dag.
  """
  def operator(node, inputs):
    return isinstance(node, Layer) or any(inputs)

  if not isinstance(layers, (tuple, list)):
    layers = (layers, )

  results = dag.propagate(operator, layers)

  return tuple(
    node
    for node in results
    if results[node]
  )