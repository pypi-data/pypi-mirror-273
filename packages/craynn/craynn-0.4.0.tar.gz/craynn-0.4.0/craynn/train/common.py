from typing import Sequence, Callable

import jax
import jax.numpy as jnp

from .. import dag
from ..layers import Layer
from ..parameters import Parameter, get_all_free_parameters, get_parameters
from ..networks import pdict

__all__ = [
  'initialize_parameters',
  'normalize_parameters'
]

def initialize_parameters(key: jax.Array, network, **properties) -> pdict:
  if hasattr(network, 'free_parameters'):
    params: Sequence[Parameter] = network.free_parameters(**properties)
  else:
    ### assuming a layer/layers
    params: Sequence[Parameter] = get_all_free_parameters(network, **properties)

  rng_params = dag.get_mode_nodes(params, mode='rng')

  values = dag.get_output(
    params,
    individual_kwargs={
        param: dict(rng=k)
        for param, k in zip(rng_params, jax.random.split(key, num=len(rng_params)))
      }
    )

  return pdict(zip(params, values))

def get_reduction(parameter_signature, parameter_shape, output_signature, output_shape):
  aligned_parameter_signature = '*' * (len(parameter_shape) - len(parameter_signature)) + parameter_signature
  aligned_output_signature = '*' * (len(output_shape) - len(output_signature)) + output_signature

  sym_to_size_param = {
    sym: s
    for sym, s in zip(aligned_parameter_signature, parameter_shape)
    if sym != '*'
  }
  sym_to_size_output = {
    sym: s
    for sym, s in zip(aligned_output_signature, output_shape)
    if sym != '*'
  }

  common_dims = [symbol for symbol in output_signature if symbol in parameter_signature and symbol != '*']

  if any(sym_to_size_param[sym] != sym_to_size_output[sym] for sym in common_dims):
    raise ValueError(
      f'provided signatures are not compatible with the shapes: '
      f'{parameter_signature} {parameter_shape} / {output_signature} {output_shape}.'
    )

  raxes = tuple(i for i, symbol in enumerate(aligned_output_signature) if symbol not in common_dims)

  psig_to_pos = {
    sym: i
    for i, sym in enumerate([sym for sym in parameter_signature if sym in common_dims])
  }

  permutation = tuple(psig_to_pos[sym] for sym in common_dims)

  broadcast = tuple(
    None if sym not in common_dims else slice(None, None, None)
    for sym in aligned_parameter_signature
  )

  return raxes, permutation, broadcast

def normalize_layer(
  layer: Layer,
  substitutes: dict[Layer, jax.Array],
  params: dict[Parameter, jax.Array],
  weights=True, biases=True,
  learning_rate=1e-1, iterations=16,
  preactivation=True,
  batch: int | None=None,
  key: jax.Array | None=None
):
  from ..nonlinearities import linear

  layer_params = get_parameters(layer)

  if hasattr(layer, 'signature'):
    _, parameters_signatures, output_signature = getattr(layer, 'signature')()
  else:
    parameters_signatures = tuple('' for _ in layer_params)
    output_signature = ''

  if weights:
    W_signature_param = [
      (signature, param)
      for signature, param in zip(parameters_signatures, layer_params)
      if param in params
      if param.properties.get('weights', False)
    ]
  else:
    W_signature_param = []

  if biases:
    b_signature_param = [
      (signature, param)
      for signature, param in zip(parameters_signatures, layer_params)
      if param in params
      if param.properties.get('biases', False)
    ]
  else:
    b_signature_param = []

  if len(W_signature_param) == 0 and len(b_signature_param) == 0:
    return params

  if hasattr(layer, 'activation') and preactivation:
    old_activation = getattr(layer, 'activation')
    setattr(layer, 'activation', linear())
  else:
    old_activation = None

  for _ in range(iterations):
    if batch is None:
      output = dag.get_output(layer, substitutes={**substitutes, **params})
    else:
      substitutes_batch = {}
      for l, X in substitutes.items():
        key_indx, key = jax.random.split(key, num=2)
        indx = jax.random.randint(key_indx, minval=0, maxval=X.shape[0], shape=(batch, ))
        substitutes_batch[l] = X[indx]

      output = dag.get_output(layer, substitutes={**substitutes_batch, **params})

    for signature, param in b_signature_param:
      reduction_axes, permutation, broadcast = get_reduction(
        signature, params[param].shape, output_signature, output.shape
      )
      mean = jnp.mean(output, axis=reduction_axes)
      offset = mean / len(b_signature_param)
      update = -learning_rate * offset

      update = jnp.transpose(update, permutation)
      params[param] = params[param] + update[broadcast]

    for signature, param in W_signature_param:
      reduction_axes, permutation, broadcast = get_reduction(
        signature, params[param].shape, output_signature, output.shape
      )

      std = jnp.std(output, axis=reduction_axes)
      scale = jnp.float_power(std, 1 / len(W_signature_param))
      update = jnp.exp(-learning_rate * jnp.log(scale))
      update = jnp.transpose(update, permutation)
      params[param] = params[param] * update[broadcast]


  if hasattr(layer, 'activation') and preactivation:
    setattr(layer, 'activation', old_activation)

  return params

def normalize_parameters(
  network,
  substitutes: dict[Layer, jax.Array] | Sequence[jax.Array],
  parameters: dict[Parameter, jax.Array],
  weights=True, biases=True,
  learning_rate=0.1, iterations=128,
  preactivation=True,
  batch: int | None=None,
  key: jax.Array | None=None,
  progress=None
):
  """
  WARNING: this procedure assumes that output of each layer is sublinear with respect to its inputs, i.e.:
  `f(x, scale * W, b) <= scale * f(x, W, b)`
  and
  `f(x, W, b + offset) <= f(x, W, b) + offset`

  While this assumption is satisfied for the most of the commonly used layers, care should be taken.
  """
  all_layers = network.layers()

  if isinstance(substitutes, Sequence):
    substitutes = {l: x for l, x in zip(network.inputs(), substitutes)}

  if progress is None:
    progress = lambda x, *args, **kwargs: x

  for layer in progress(all_layers, desc='normalization'):
    parameters = normalize_layer(
      layer, substitutes, parameters,
      weights=weights, biases=biases,
      learning_rate=learning_rate, iterations=iterations,
      preactivation=preactivation,
      batch=batch, key=key
    )

  return pdict(parameters)