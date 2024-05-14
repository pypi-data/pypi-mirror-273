from typing import Sequence

import jax
import jax.numpy as jnp

import math

__all__ = [
  'tensor_definition',
  'tensor_pack',
  'tensor_unpack',
  'tensor_size',

  'tree_sum',
  'tree_map_sum',

  'select'
]

def is_shape(x):
  if not isinstance(x, tuple):
    return False

  return all(isinstance(s, int) for s in x)

def tensor_definition(shape_or_array_tree, batch_dimensions: Sequence[int]=()):
  """
  Returns tree definition for packing and unpacking trees.
  See `tensor_pack` and `tensor_unpack`.

  :param shape_or_array_tree: tree containing either tensors or shapes of tensors;
  :param batch_dimensions: dimensions to consider as batch dimensions;
  :return: tensor-tree definition object for unpacking a tensor.
  """
  batch_dimensions = tuple(batch_dimensions)

  shape_tree = jax.tree_util.tree_map(
    lambda x: x.shape if hasattr(x, 'shape') else x,
    shape_or_array_tree
  )

  shape_tree_flat, shape_tree_def = jax.tree_util.tree_flatten(shape_tree, is_leaf=is_shape)
  original_shapes = [
    tuple(s for i, s in enumerate(shape) if i not in batch_dimensions)
    for shape in shape_tree_flat
  ]

  return shape_tree_def, original_shapes

def tensor_size(shape_or_array_tree, batch_dimensions: Sequence[int]=()):
  """
  Returns the size of packed tensor, i.e., size of all elements of all tensors in the tree
  (expect for the batch dimensions).

  :param shape_or_array_tree: tree containing either tensors or shapes of tensors;
  :param batch_dimensions: dimensions to consider as batch dimensions;
  :return: size of the packed tensor
  """
  _, original_shapes = tensor_definition(shape_or_array_tree, batch_dimensions=batch_dimensions)
  return sum(math.prod(shape) for shape in original_shapes)

def tensor_pack(tree, batch_dimensions=(0, )):
  """
  "Packs" an arbitrary tree of tensors into a tensor of shape (*batch, N) by
  flattening and concatenating all non-batch dimensions.

  `tensor_pack` also returns an object, a tensor-tree definition, that allows unpacking the resulting tensor
  into the original structure. The tensor-tree definition can also be applied to tensors with
  different batch dimension.

  The "packed" tensor is useful for performing linear algebra routines on a tree, for example, a linear regression:

      X = <samples, a tree with (batch, *) entries>
      y = <an array of size (batch, )>
      X_packed, tensor_def = tensor_pack(X, batch_dimensions=(0, )) ### an array of size (batch, N)
      W_packed = <coefficients for linear regression fitted to X_packed and y, an array of size (N, )>
      W = tensor_unpack(tree_def, W_packed) ### has the same structure as X

  :param tree: the original tree containing tensors;
  :param batch_dimensions: dimensions to consider as batch dimensions, must be consecutive starting with 0 or empty;
  :return: "packed" tensor, definition for unpacking.
  """
  batch_dimensions = tuple(batch_dimensions)

  tensor_def = tensor_definition(
    jax.tree_util.tree_map(jnp.asarray, tree),
    batch_dimensions=batch_dimensions
  )

  tree_mat = [
    x.reshape((
      *(x.shape[i] for i in batch_dimensions),
      math.prod(x.shape[i] for i in range(x.ndim) if i not in batch_dimensions)
    ))

    for x in jax.tree_util.tree_leaves(tree)
  ]

  return jnp.concatenate(tree_mat, axis=-1), tensor_def

def tensor_unpack(tensor_def, tensor, axis=-1):
  """
  "Unpacks" the `tensor` according to `tensor_def`.
  `tensor` must have the same size along `axis` as the tensor for which `tensor_def` was produced.
  In particular, `tensor` might have different batch dimensions and additional axes.

  :param tensor_def: `tensor_def` is returned by either `tensor_pack` or `tensor_defenition`.
  :param tensor: tensor to "unpack"
  :param axis: axis along which to "unpack";
  :return: a tree with the same structure as the original tensor.
  """
  tree_def, original_shapes = tensor_def
  axis = tensor.ndim + axis if axis < 0 else axis
  offset = tuple(slice(None, None, None) for _ in range(axis))

  tree_mat = list()
  i = 0

  for original_shape in original_shapes:
    size = math.prod(original_shape)

    index = (*offset, slice(i, i + size, None))

    subtensor = tensor[index]
    tree_mat.append(
      subtensor.reshape(
        (*subtensor.shape[:axis], *original_shape, *subtensor.shape[axis + 1:])
      )
    )
    i += size

  return jax.tree_util.tree_unflatten(tree_def, tree_mat)

class select(object):
  """
  A convenience object, `select(tree)[indx]` is equivalent to `jax.tree_util.tree_map(lambda x: x[indx], tree)`.
  """
  def __init__(self, x):
    self.x = x

  def __getitem__(self, item):
    return jax.tree_util.tree_map(
      lambda a: a[item] if isinstance(a, jax.Array) else jax.numpy.asarray(a)[item],
      self.x
    )

def tree_sum(tree) -> jax.Array:
  result: jax.Array = sum(x for x in jax.tree_util.tree_leaves(tree))

  return result

def tree_map_sum(f, *args) -> jax.Array:
  tree = jax.tree_util.tree_map(f, *args)
  return tree_sum(tree)