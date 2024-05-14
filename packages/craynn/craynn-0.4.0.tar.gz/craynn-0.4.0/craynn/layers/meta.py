from typing import Type, Sequence, TypeAlias

from .. import dag

__all__ = [
  'Layer', 'LayerModel', 'InputLayer',
  'get_layers', 'get_input_layers',

  'model_selector',
]

### inputs layout, parameters layout, output layout
LayerSignature: TypeAlias = tuple[tuple[str, ...], tuple[str, ...], str]

class Layer(dag.Node):
  def __init__(self, *incoming, parameters=(), name=None, shape=None):
    self.parameters = parameters
    self.incoming_layers = incoming

    super(Layer, self).__init__(
      *(parameters + incoming),
      name=name
    )

    self.shape = dag.get_output_shape(self) if shape is None else shape

  def get_output_shape_for(self, *input_shapes, **kwargs):
    raise NotImplementedError()

  def get_output_for(self, *inputs, **kwargs):
    raise NotImplementedError()

  def signature(self) -> LayerSignature:
    return (
      tuple('' for _ in self.incoming_layers),
      tuple('' for _ in self.parameters),
      ''
    )


class LayerModel(dag.NodeModel):
  LayerType: Type[Layer]

  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs

  def __call__(self, *incoming: Layer) -> 'LayerType':
    return self.LayerType(*incoming, *self.args, **self.kwargs)


class InputLayer(Layer):
  def __init__(self, shape, name=None):
    super(InputLayer, self).__init__(name=name, shape=shape)

  def get_output_shape_for(self):
    return self.shape

  def get_output_for(self, *inputs, **kwargs):
    raise ValueError('Input was asked to return a value, this should not have happened.')

def get_layers(nodes: dag.Node | Sequence[dag.Node]) -> tuple[Layer, ...]:
  return tuple(
    node
    for node in dag.get_nodes(nodes)
    if isinstance(node, Layer)
  )

def get_input_layers(nodes: dag.Node | Sequence[dag.Node]) -> tuple[Layer, ...]:
  return tuple(
    layer
    for layer in get_layers(nodes)
    if len(dag.get_incoming(layer)) == 0
  )

def model_selector(criterion):
  """Decorator, changes signature and inserts checks into a layer model selector.

  This is a wrapper which inserts a common procedures for a selector:
  - signature checks for each model (must all be the same);
  - binding of model parameters;
  - replacement of selector signature by models' shared signature.

  Model selector is a nodes layer model that selects a particular layer model from a provided list
  based on properties of incoming layer, i.e. defers selection of a model until network construction.

  Type of the selector: `list of models` -> `incoming layer` -> `layer`.

  Parameters
  ----------
  criterion : Selector
    selector to modify. This function can assume that models have the same signature (i.e. accept the same parameters).

  Returns
  -------
  Selector
    Selector with changed signature and validity checks.

  Examples
  -------
  Selecting model with proper dimensionality for convolutional layer
  based on dimensionality of the incoming layer:

  >>> @model_selector
  >>> def dimensionality_selector(models):
  >>>   def common_model(incoming):
  >>>     ndim = len(dag.get_output_shape(incoming)) - 2
  >>>     return models[ndim]
  >>>   return common_model
  """

  def selector(models):
    from inspect import signature, Signature, Parameter
    assert len(models) > 0

    models_signatures = [
      signature(model) for model in models
      if model is not None
    ]

    if len(set(models_signatures)) != 1:
      pretty_signatures = '\n  '.join([ str(signature) for signature in set(models_signatures)])
      raise ValueError('All models must have the same signature, got:%s' % pretty_signatures)

    common_signature = models_signatures[0]
    pretty_parameters = [Parameter('self', Parameter.POSITIONAL_ONLY)]
    pretty_parameters.extend(common_signature.parameters.values())
    pretty_signature = Signature(parameters=pretty_parameters, return_annotation=common_signature.return_annotation)

    bound_criterion = criterion(models)

    def __init__(self, *args, **kwargs):
      self.args = args
      self.kwargs = kwargs

      common_signature.bind(*args, **kwargs)

    def __call__(self, *incoming):
      selected_model = bound_criterion(*incoming)
      if selected_model is None:
        raise ValueError('Invalid incoming layer!')

      return selected_model(*self.args, **self.kwargs)(*incoming)

    __init__.__signature__ = pretty_signature

    model = type(
      '%s' % (getattr(criterion, '__name__', 'model_selector'), ),
      (LayerModel, ),
      dict(
        __init__ = __init__,
        __call__ = __call__
      )
    )

    return model

  return selector
