import jax

from .. import dag
from .. import layers
from .. import parameters

from .utils import get_signature, get_named_layers, pdict

__all__ = [
  'Network', 'network',
]


class Network(object):
  def __init__(self, inputs, outputs, **modes):
    self._inputs = inputs
    self._outputs = outputs
    self._modes = modes

    try:
      self.__call__.__signature__ = get_signature(inputs)
    except:
      pass

    all_layers = self.nodes()
    self._rng_layers = dag.get_mode_nodes(all_layers, mode='rng')
    self._named_layers = get_named_layers(all_layers)
    self._free_parameters = parameters.get_all_free_parameters(self.outputs(), )

  def outputs(self):
    if isinstance(self._outputs, (list, tuple)):
      return self._outputs
    else:
      return (self._outputs, )

  def inputs(self):
    return self._inputs

  def parameters(self, **properties):
    parameters.get_parameters(self._outputs, **properties)

  def free_parameters(self, **properties):
    if len(properties) == 0:
      return self._free_parameters
    else:
      check = parameters.check_properties(**properties)
      return [param for param in self._free_parameters if check(param)]

  def initialize(self, rng, **properties) -> pdict:
    from .. import train
    return train.initialize_parameters(rng, self, **properties)

  def normalize(
    self, key: jax.Array, *args,
    weights=True, biases=True,
    learning_rate: float=0.1, iterations: int=128,
    preactivation: bool=True,
    batch: int | None = None,
    progress=None
  ) -> pdict:
    from .. import train
    substitutes = self._map_inputs(args)
    inputs = {l: v for l, v in substitutes.items() if not isinstance(l, parameters.FreeParameter)}
    params = {l: v for l, v in substitutes.items() if isinstance(l, parameters.FreeParameter)}

    return train.normalize_parameters(
      key, self, inputs, params, weights=weights, biases=biases,
      learning_rate=learning_rate, iterations=iterations,
      preactivation=preactivation, batch=batch, progress=progress
    )


  def find_layer(self, layer_or_name):
    if isinstance(layer_or_name, str):
      return self._named_layers[layer_or_name]
    elif isinstance(layer_or_name, layers.Layer):
      return layer_or_name
    else:
      raise Exception("%s is not a layer or a layer's name" % (layer_or_name, ))

  def find_layers(self, layers_names):
    if isinstance(layers_names, (list, tuple)):
      return tuple(
        self.find_layer(ln)
        for ln in layers_names
      )
    else:
      return self.find_layer(layers_names)

  def subnet(self, inputs=None, outputs=None):
    inputs = self._inputs if inputs is None else self.find_layers(inputs)
    inputs = inputs if isinstance(inputs, (list, tuple)) else (inputs, )

    outputs = self._outputs if outputs is None else self.find_layers(outputs)

    return Network(inputs, outputs)

  def as_subnet(self, *incoming):
    from ..subnetworks import subnetwork
    return subnetwork(self.inputs(), self.outputs())(*incoming)

  def _map_parameters(self, values):
    from ..utils.axes import check_shape_consistency

    if len(values) != len(self._free_parameters):
      raise ValueError(
        'number of provided values (%d) does not match number of free parameters (%d)' % (
          len(values), len(self._free_parameters)
        )
      )

    for parameter, value in zip(self._free_parameters, values):
      if not check_shape_consistency(value.shape, parameter.shape):
        raise ValueError(
          'Shape of a value (%s) is not consistent with the shape of the corresponding parameter (%s)' % (
            value.shape, parameter.shape()
          )
        )

    return {
      parameter: value
      for parameter, value in zip(self._free_parameters, values)
    }

  def _map_inputs(self, args):
    inputs = list()
    substitutes = dict()

    for arg in args:
      if isinstance(arg, dict):
        for l, X in arg.items():
          if isinstance(l, str):
            if l not in self._named_layers:
              raise Exception(f'There is no layer with name {l}')
            layer = self._named_layers[l]

          elif isinstance(l, dag.Node):
            layer = l

          else:
            raise ValueError(
              f'Input dictionaries only accept str or Nodes (Layers and Parameters) as keys, got {l}.'
            )

          if layer in substitutes:
            raise ValueError(f'Two or more values are provided for the layer {l}.')

          substitutes[layer] = X

      else:
        inputs.append(arg)

    for input_layer, arg in zip(self.inputs(), args):
      if input_layer in substitutes:
        raise ValueError(f'Two or more values are provided for the layer {input_layer}')

      substitutes[input_layer] = arg

    return substitutes

  def __call__(self, *args, rng=None, **kwargs):
    """
    Returns result of network evaluation.

    Each element of `*args` must be either a tensor or a dictionary of type layer/parameter -> tensor.
    Keyword arguments allow to provide "modes" to the layer.
    Standalone tensors are matched with the network's inputs in the same order as inputs were defined.
    Dictionaries are directly matched to the corresponding layers/parameters.

    Note that it is not necessary to provide values for all input layers. For instance, for the following network:
    ```python
    net = network(x=(None, 2), y=(None, 2))(
      dense(4, name='z'),
      dense(2)
    )
    params = ...
    ```

    `net(params, {'z': jnp.zeros(shape=(3, 4))})` will be properly evaluated since input layers are not required for
    evaluation of the result. The same principle applies to the free parameters of the network.

    :param args: substitutes for layers/parameters: tensors are matched to the network's inputs,
      dictionaries are mapped directly;
    :param kwargs: modes for layers.
    :return: result of the network evaluation.
    """

    substitutes = self._map_inputs(args)

    try:
      if rng is not None:
        rng = {
          layer: dict(rng=v)
          for layer, v in zip(self._rng_layers, jax.random.split(rng, num=len(self._rng_layers)))
        }
      else:
        rng = None

      return dag.get_output(self._outputs, substitutes=substitutes, individual_kwargs=rng, **self._modes)

    except Exception as e:
      import itertools
      inputs_wo_substitute = [
        layer
        for layer in itertools.chain(self.inputs(), self.free_parameters())
        if layer not in substitutes
      ]

      if len(inputs_wo_substitute) > 0:
        raise ValueError(
          'Not all inputs were provided value, this might be the cause of the error: %s' % (inputs_wo_substitute, )
        ) from e
      else:
        raise

  def description(self, short=True, **attributes):
    from craynn.info.layers import graph_description
    return graph_description(self.outputs(), short=short, inputs=self.inputs(), **attributes)

  def __str__(self):
    return self.description(short=True)

  def __repr__(self):
    return self.description(short=True)

  def total_number_of_parameters(self):
    from ..info.layers import get_total_number_of_parameters
    return get_total_number_of_parameters(self.outputs())

  def nodes(self):
    return dag.get_nodes(self.outputs())

  def layers(self):
    return layers.get_layers(self.outputs())

  def input_shapes(self):
    return dag.get_output_shape(self.inputs())

  def output_shapes(self):
    return dag.get_output_shape(self.outputs())


def __is_shape(shape_or_layer):
  return hasattr(shape_or_layer, '__iter__') and all([ (type(s) is int or s is None) for s in shape_or_layer ])

def _get_input_layer(shape_or_layer, name=None, index=None):
  if __is_shape(shape_or_layer) :
    shape = shape_or_layer

    if name is not None:
      return layers.InputLayer(shape=shape, name=name)
    elif index is not None:
      return layers.InputLayer(shape=shape, name='input%d' % index)
    else:
      return layers.InputLayer(shape=shape, name='input')

  elif isinstance(shape_or_layer, (layers.Layer, parameters.Parameter)) :
    return shape_or_layer


def _make_network(factory, inputs, named_inputs):
  input_layers = []

  for i, input in enumerate(inputs):
    input_layers.append(_get_input_layer(input, name=None, index=i))

  for i, (name, input) in enumerate(named_inputs.items()):
    input_layers.append(_get_input_layer(input, name=name, index=i))

  explicit_names = [ layer.name for layer in input_layers if layer.name is not None ]
  assert len(set(explicit_names)) == len(explicit_names)

  outputs = factory(*input_layers)

  return Network(input_layers, outputs)


def network(*inputs, **named_inputs):
  """
  Allows nice syntax:
  ```
    net(<shape of input 1>, <shape of input 2>, ..., named_input=<shape of the named_input>)(
      constructor
    )
  ```
  or
  ```
    net(<input shape>)(
      constructor
    )
  ```
  for single input.
  """
  def constructor(*factory):
    return _make_network(dag.achain(*factory), inputs, named_inputs)

  return constructor