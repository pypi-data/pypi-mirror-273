from typing import Literal, Union

import jax
import jax.numpy as jnp

__all__ = [
  'conv_transpose',

  'conv_output_shape',
  'conv_transposed_output_shape',
  
  'normalized_shape',
  'get_padding',

  'get_channel_dim',
  'get_spatial_dims',
]

### jax and tf operate with an upper case padding modes, while
### lower case modes seem nicer.
PADDINGS = {'VALID', 'SAME'}
Padding = Union[int, tuple[int, ...], Literal['valid', 'same']]

def get_conv_spec(ndim: int):
  if ndim == 1:
    return 'NCH', 'OIH', 'NCH'
  elif ndim == 2:
    return 'NCHW', 'OIHW', 'NCHW'
  elif ndim == 3:
    return 'NCHWD', 'OIHWD', 'NCHWD'
  else:
    raise ValueError('4+ dimensional conv is not supported')

def conv_output_shape(input_shape, kernel_shape, strides, padding, dilation, conv_spec):
  effective_kernel_shape = kernel_shape[:2] + tuple(
    (k - 1) * s + 1
    for k, s in zip(kernel_shape[2:], dilation)
  )

  return jax.lax.conv_general_shape_tuple(
    input_shape, effective_kernel_shape,
    window_strides=strides,
    padding=padding,
    ### for some reason this function accepts conv spec instead of declared dim numbers
    dimension_numbers=conv_spec
  )

def get_transposed_padding(
  padding: tuple[tuple[int, int], ...] | Literal['VALID', 'SAME'],
  kernel_shape: tuple[int, ...],
  strides: tuple[int, ...],
  dilation: tuple[int, ...]
):
  if padding == 'SAME':
    return padding

  kernel_spatial = kernel_shape[2:]
  ndim = len(kernel_spatial)

  if padding == 'VALID':
    padding = tuple((0, 0) for _ in range(ndim))

  return tuple(
    (pl * s + (k - 1) * d, pr * s + (k - 1) * d)
    for (pl, pr), s, k, d in zip(padding, strides, kernel_spatial, dilation)
  )

def conv_transpose(
  input: jnp.ndarray,
  kernel: jnp.ndarray,
  strides: tuple[int, ...],
  padding: tuple[tuple[int, int], ...] | Literal['VALID', 'SAME'],
  dimension_numbers,
  feature_group_count: int = 1,
  dilation: tuple[int, ...] | None = None
):
  """
  An alternative implementation of `jax.lax.conv_transpose`: the function also uses
  `jax.lax.conv_general_dilated` but remaps `strides`, `padding` and `dilation` to match the conventional definition
  of transposed convolution.
  Also provides `feature_group_count` parameter.,

  :param input: a tensor (LHS) to convolve;
  :param kernel: a kernel (RHS) with which to convolve;
  :param strides: strides of the transposed convolution (maps to lhs_dilation);
  :param padding: padding, the same as in forward convolution, this function automatically adjusts padding to emulate
    conventional transpose conv, e.g., input of length 1 and kernel of length 3 result in an array of length 3.
  :param dimension_numbers: the same as in `jax.lax.conv_general_dilated`
  :param feature_group_count: the same as in `jax.lax.conv_general_dilated`
  :param dilation: dilation of the kernel.
  :return: result of the transposed convolution.
  """

  assert all(s <= k for s, k in zip(strides, kernel.shape[2:])), 'Strides larger than kernel are not supported'

  transposed_padding = get_transposed_padding(padding, kernel_shape=kernel.shape, strides=strides, dilation=dilation)

  return jax.lax.conv_general_dilated(
      input,
      kernel,
      window_strides=tuple(1 for _ in strides),
      padding=transposed_padding,
      dimension_numbers=dimension_numbers,
      feature_group_count=feature_group_count,
      lhs_dilation=strides,
      rhs_dilation=dilation
    )

def conv_transposed_output_shape(input_shape, kernel_shape, strides, padding, dilation, conv_spec):
  effective_kernel_shape = kernel_shape[:2] + tuple(
    (k - 1) * d + 1
    for k, d in zip(kernel_shape[2:], dilation)
  )

  effective_input_shape = input_shape[:2] + tuple(
    (w - 1) * s + 1 for w, s in zip(input_shape[2:], strides)
  )

  ### the function inflates kernel itself
  transposed_padding = get_transposed_padding(padding, kernel_shape=kernel_shape, strides=strides, dilation=dilation)

  return jax.lax.conv_general_shape_tuple(
    effective_input_shape, effective_kernel_shape,
    window_strides=tuple(1 for _ in strides),
    padding=transposed_padding,
    ### for some reason this function accepts conv spec instead of declared dim numbers
    dimension_numbers=conv_spec
  )

def normalized_shape(shape: int | tuple[int, ...], ndim: int):
  if type(shape) is int:
    return (shape, ) * ndim
  else:
    try:
      if all(type(n) is int for n in shape) and len(shape) == ndim:
        return tuple(shape)
      else:
        raise ValueError('shape is neither iterable of size %d, nor int [%s]' % (ndim, shape))
    except:
      raise ValueError('shape is neither iterable of size %d, nor int [%s]' % (ndim, shape))

def get_padding(padding: Padding, ndim: int):
  if isinstance(padding, str):
    padding = padding.upper()
    if padding not in PADDINGS:
      raise ValueError(f'Unknown padding: {padding}')

    return padding

  elif isinstance(padding, int):
    return tuple((padding, padding) for _ in range(ndim))

  elif isinstance(padding, tuple):
    if len(padding) != ndim:
      raise ValueError(f'Length of padding ({padding}) does not agree with ndim={ndim}')

    canonical_padding = []

    for p in padding:
      if isinstance(p, int):
        canonical_padding.append((p, p))
      else:
        left, right = padding
        if not isinstance(left, int) or not isinstance(right, int):
          raise ValueError(f'Unknown padding: {padding}')
        canonical_padding.append((left, right))

    return tuple(canonical_padding)

  else:
    raise ValueError(f'Unknown padding: {padding}')

def get_channel_dim(shape):
  return shape[1]

def get_spatial_dims(shape):
  return shape[2:]