import jax
import jax.numpy as jnp

__all__ = [
  'tree_split',
  'rand_ortho',
  'rand_ortho_extension'
]

def tree_split(key, x):
  """
  Splits `rng` into RNG keys for each tensor in `x`.
  The result has the same structure as `x` (as interpreted by `jax.tree_utils`).
  """

  x_flat, treedef = jax.tree_util.tree_flatten(x)
  keys = jax.random.split(key, num=len(x_flat))
  return jax.tree_util.tree_unflatten(treedef, keys)

def rand_ortho(key: jax.Array, size: int, ndim: int):
  """
  Generates a random `ndim`-dimensional orthonormal basis of size `size`.

  :param key: RNG key;
  :param size: number of the basis vectors;
  :param ndim: dimensionality of the space;
  :return: an orthonormal matrix of size (size, ndim).
  """

  A = jax.random.normal(key, shape=(ndim, size))
  Q, _ = jnp.linalg.qr(A, mode='reduced')

  return Q.T

def rand_ortho_extension(key: jax.Array, v: jax.Array, size: int):
  """
  Generates a random `ndim`-dimensional orthonormal basis of size `size`
  with `v` (or `-v`) as one of the basis vectors.

  :param key: RNG key;
  :param v: the initial vector for extension;
  :param size: number of the basis vectors;
  :return: an orthonormal matrix of size (size, ndim).
  """

  ndim, = v.shape
  assert size <= ndim

  A = jnp.zeros(shape=(ndim, size))
  A = A.at[:, 0].set(v)
  A = A.at[:, 1:].set(
    jax.random.normal(key, shape=(ndim, size - 1))
  )
  Q, _ = jnp.linalg.qr(A, mode='reduced')

  return Q.T