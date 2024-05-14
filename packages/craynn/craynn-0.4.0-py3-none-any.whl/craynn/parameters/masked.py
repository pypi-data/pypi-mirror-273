import jax.random

from .defaults import default_weight_init
from .meta import Parameter, ParameterModel

__all__ = [
  'MaskedParameter', 'masked_parameter',
  'DropConnect', 'drop_connect'
]

class MaskedParameter(Parameter):
  def __init__(self, shape, mask: ParameterModel, w: ParameterModel=default_weight_init, name=None, **properties):
    self.w = w(
      shape=shape,
      **properties,
      name=(name + '_w') if name is not None else None
    )

    self.mask = mask(
      shape=shape,
      mask=True,
      **properties,
      name=(name + '_mask') if name is not None else None
    )

    super(MaskedParameter, self).__init__(
      self.w, self.mask,
      shape=shape,
      name=name,
      **properties
    )

  def get_output_for(self, w, mask):
    return w * mask

  def get_output_shape_for(self, w_shape, mask_shape):
    assert w_shape == mask_shape, "Mask's shape does not match weights' shape."
    return w_shape

class masked_parameter(ParameterModel):
  ParameterType = MaskedParameter

  def __init__(
    self,
    mask: ParameterModel, w: ParameterModel=default_weight_init,
    name=None,
    composite=True, **properties
  ):
    super().__init__(dict(**properties, composite=composite), mask=mask, w=w, name=name)

class DropConnect(Parameter):
  def __init__(self, shape, w: ParameterModel=default_weight_init, p: float=0.1, name=None, **properties):
    self.w = w(
      shape=shape,
      **properties,
      name=(name + '_w') if name is not None else None
    )

    self.p = p

    super(DropConnect, self).__init__(
      self.w,
      shape=shape,
      name=name,
      **properties
    )

  def get_output_for(self, w, rng=None):
    if rng is None:
      return w
    else:
      mask = jax.random.bernoulli(rng, shape=w.shape, p=1 - self.p)
      return mask * w / (1 - self.p)


  def get_output_shape_for(self, w_shape):
    return w_shape

class drop_connect(ParameterModel):
  ParameterType = DropConnect

  def __init__(
    self,
    w: ParameterModel=default_weight_init, p: float=0.1,
    name=None,
    composite=True, **properties
  ):
    super().__init__(dict(**properties, composite=composite), w=w, p=p, name=name)