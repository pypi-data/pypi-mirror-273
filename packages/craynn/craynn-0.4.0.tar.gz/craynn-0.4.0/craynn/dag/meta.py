from typing import Sequence, TypeAlias, Type

__all__ = [
  'Node',
  'GraphModel',
  'NodeModel',

  'get_incoming',
  'get_name',
]

Shape: TypeAlias = tuple[int, ...]

class Node(object):
  def __init__(self, *incoming, name=None):
    self.incoming = incoming
    self.name = name

  def __str__(self):
    if self.name is None:
      return self.__class__.__name__
    else:
      return self.name

  def __repr__(self):
    return str(self)

  def __lt__(self, other):
    """
    This effectively declares that all node are equal.
    Some frameworks, like jax, internally flatten dictionaries of type node -> T, presumably, using
    `sorted` on the keys which requires comparison operators.
    """
    return False

  def get_output_for(self, *incoming: 'Node', **modes):
    raise NotImplementedError()

  def get_output_shape_for(self, *input_shapes: Shape) -> Shape:
    raise NotImplementedError()

def get_mutator(cls):
  """
  Returns class that allows to make some parameters of the corresponding model fixed or
  defaults redefined:

      model = node_model.with_fixed(x=1).with_defaults(y=2)

  is equivalent to:

      model = lambda *args, y=2, **kwargs: node_model(*args, x=1, y=y, **kwargs)
  """

  def __init__(self, fixed=None, defaults=None):
    self._fixed = fixed if fixed is not None else dict()
    self._defaults = defaults if defaults is not None else dict()

  def with_fixed(self, **kwargs):
    self._fixed.update(kwargs)
    return self

  def with_defaults(self, **kwargs):
    self._defaults.update(kwargs)
    return self

  def __str__(self):
    fixed_str = ', '.join(
      '%s=%s' % (k, v)
      for k, v in self._fixed.items()
    )

    defaults_str = ', '.join(
      '%s->%s' % (k, v)
      for k, v in self._defaults.items()
    )
    return '%s mutator(%s, %s)' % (
      cls.__name__,
      fixed_str,
      defaults_str
    )

  def __repr__(self):
    return str(self)

  def __call__(self, *args, **kwargs):
    for k in self._fixed:
      if k in kwargs:
        raise ValueError('attempting to redefine fixed argument')
      else:
        kwargs[k] = self._fixed[k]

    for k in self._defaults:
      kwargs[k] = kwargs.get(k, self._defaults[k])

    return cls(*args, **kwargs)

  from craynn.utils.func import signature_with_self
  __call__.__signature__ = signature_with_self(cls)

  return type(
    '%sMutator' % (cls.__name__, ),
    (object, ),
    dict(
      __init__ = __init__,
      __call__ = __call__,
      with_fixed = with_fixed,
      with_defaults = with_defaults,
      __str__ = __str__,
      __repr__ = __repr__
    )
  )

class MetaModel(type):
  """
  Metaclass for the NodeModel.
  Upon creation of a new NodeModel, a Mutator class is derived and assigned to the newly created class.
  """
  def __new__(mcs, name, bases, dct):
    cls = super().__new__(mcs, name, bases, dct)
    cls.mutator = get_mutator(cls)

    return cls

class GraphModel(object):
  def __call__(self, *incoming) -> Node | Sequence[Node]:
    raise NotImplementedError()

class NodeModel(object, metaclass=MetaModel):
  """
  Base class for (*Node) -> Node callables (a.k.a. node models).
  """
  @classmethod
  def with_fixed(cls, **kwargs):
    return cls.mutator(fixed=kwargs)

  @classmethod
  def with_defaults(cls, **kwargs):
    return cls.mutator(defaults=kwargs)


def get_incoming(node: Node) -> Sequence[Node]:
  return getattr(node, 'incoming', ())

def get_name(node: Node) -> str:
  return getattr(node, 'name', None)