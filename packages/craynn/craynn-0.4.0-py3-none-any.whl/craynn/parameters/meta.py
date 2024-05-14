from typing import Type, Sequence

import jax
import jax.numpy as jnp

from .. import dag

from .utils import combine_properties

__all__ = [
  'Parameter', 'ParameterModel',

  'FreeParameter',

  'check_properties',
  'get_parameters', 'get_all_parameters', 'get_all_free_parameters',

  'ParameterCloneMachine', 'shared_parameter'
]

class Parameter(dag.Node):
  def __init__(self, *incoming, shape=(), name=None, **properties):
    self.shape = shape
    self.properties = properties
  
    super(Parameter, self).__init__(*incoming, name=name)

  def get_output_for(self, *incoming, **modes):
    raise NotImplementedError()

  def get_output_shape_for(self, *input_shapes):
    return self.shape

  def __str__(self):
    name = self.__class__.__name__ if self.name is None else self.name
    shape = 'x'.join(['%d' % (s, ) for s in self.shape])
    props = [('shape', shape)]
    props.extend(self.properties.items())

    return '%s (%s)' % (
      name,
      ', '.join(['%s=%s' % (k, v) for k, v in props])
    )

  def __repr__(self):
    return str(self)


class ParameterModel(dag.NodeModel):
  ParameterType: Type[Parameter]

  def __init__(self, properties, *args, **kwargs):
    self.args = args
    self.properties = properties
    self.kwargs = kwargs

  def __call__(self, shape, name=None, **properties) -> 'ParameterType':
    if self.kwargs.get(name, None) is None:
      kwargs = {**self.kwargs, 'name': name}
    else:
      kwargs = self.kwargs

    return self.ParameterType(
      shape, *self.args, **kwargs,
      **combine_properties(self.properties, properties)
    )


class FreeParameter(Parameter):
  def __init__(self, shape=(), dtype: jnp.dtype=jnp.float32, name=None, **properties):
    self.dtype = dtype

    super(FreeParameter, self).__init__(shape=shape, name=name, **properties)

  def get_output_for(self, **modes):
    raise NotImplementedError()


def check_properties(**properties):
  effective_properties = tuple(
    (k, v)
    for k, v in properties.items()
    if v is not None
  )

  def predicate(param):
    props = getattr(param, 'properties', {})

    return all([
      (props.get(k, False) == v)
      for k, v in effective_properties
    ])

  return predicate

def get_all_parameters(nodes: dag.Node | Sequence[dag.Node], **properties) -> list[Parameter]:
  """
  Get all parameters that satisfy all `properties` from the subgraph defined by `node`.

  A parameter satisfies a property `prop = value` if:
    - value is None;
    - the parameter has property `prop` and its value equals to `value` or
    - the parameter lacks property `prop` and `value = False`.

  Note, that `prop = None` matches all parameters, this is done to
  place commonly used properties to default arguments and enable autocomplete for them.

  :param nodes: an instance of Node (e.g. Layer or Parameter), a list or a tuple of nodes.
  :param properties: properties to select by.
  :return: list of all parameters that satisfy `properties`
  """
  check_props = check_properties(**properties)

  return [
    node
    for node in dag.get_nodes(nodes)
    if isinstance(node, Parameter)
    if check_props(node)
  ]


def get_all_free_parameters(nodes: dag.Node | Sequence[dag.Node], **properties) -> list[Parameter]:
  """
  Get all *free* parameters that satisfy all `properties` from the subgraph defined by `node`.

  A node is considered to be a free parameter if it is an instance of FreeParameter.

  :param nodes: an instance of Node (e.g. Layer or Parameter), a list or a tuple of nodes.
  :param properties: properties to select by.
  :return: list of all parameters that satisfy `properties`
  """
  check_props = check_properties(**properties)

  return [
    node
    for node in dag.get_nodes(nodes)
    if isinstance(node, FreeParameter)
    if check_props(node)
  ]


def get_parameters(node: dag.Node, **properties) -> list[Parameter]:
  """
  Get parameters of the node. Note, that unlike `get_all_parameters`,
  this function returns only parameters of `node` and does not inspects parameters of incoming nodes.
  In particular, if node depends on a parameter that, in its turn, depends on another parameter,
  only the first parameter will be returned.

  :param node: an instance of Node (e.g. Layer or Parameter).
  :param properties: properties to select by.
  :return: list of all parameters that satisfy `properties`
  """
  check_props = check_properties(**properties)

  return [
    param
    for param in getattr(node, 'parameters', ())
    if check_props(param)
  ]

def get_free_parameters(node: dag.Node, **properties):
  """
  Get free parameters of the node. Note, that unlike `get_parameters`,
  this function returns only free parameters of `node` and does not inspects parameters of incoming nodes,
  but it does unravels parameter dependencies.

  :param node: an instance of Node (e.g. Layer or Parameter).
  :param properties: properties to select by.
  :return: list of all parameters of a node that satisfy `properties`
  """
  check_props = check_properties(**properties)

  own_parameters = getattr(node, 'parameters', ())

  return [
    param
    for param in dag.get_nodes(own_parameters)
    if isinstance(param, FreeParameter)
    if check_props(param)
  ]

class ParameterCloneMachine(object):
  def __init__(self, parameter_constructor):
    self.parameter_constructor = parameter_constructor
    self.parameter = None
    self._shape = None

  def __call__(self, shape, name=None, **additional_properties):
    if self.parameter is None:
      self.parameter = self.parameter_constructor(shape, name, **additional_properties)
      self._shape = shape
      return self.parameter

    else:
      assert shape == self._shape, 'Can not clone parameter for different shape.'
      return self.parameter

shared_parameter = ParameterCloneMachine

