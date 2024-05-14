from typing import Sequence
import math

import jax
import jax.numpy as jnp

from . import tree, array, rng

__all__ = [
  'ortho_grad',
  'lstsq_fit', 'quick_lin_fit', 'lin_predict',
  'lstsq_quad_fit', 'quad_predict'
]

def ortho_grad(f, argnums: int | Sequence[int]=0, n_basis: int=None, scale: float=1e-3):
  """
  Returns a function that estimates gradient via finite difference using random
  orthogonal perturbations. If `n_basis` is specified, only `n_basis` evaluations
  (`n_basis` perturbation basis vectors) are used.

  The returned function accepts the same arguments as the original one, also accepts RNG key `key: jax.Array` as the
  first argument, for example:

  def f(x: X, y: Y):
    ...

  ortho_grad(f): (key, X, Y) -> (X, Y)

  :param f: function to differentiate;
  :param argnums: indices of arguments to differentiate w.r.t., similar to `jax.grad`;
  :param n_basis: number of basis vectors in perturbations, by default the complete basis is used;
  :param scale: scale of perturbations;
  :return: gradient estimator.
  """
  def df(key: jax.Array, *args):
    if isinstance(argnums, int):
      _argnums = ((argnums + len(args)) % len(args), )
    else:
      _argnums = tuple((i + len(args)) % len(args) for i in argnums)

    variables = tuple(args[i] for i in _argnums)

    tensor_def = tree.tensor_definition(variables, batch_dimensions=())
    N = tree.tensor_size(variables, batch_dimensions=())

    if n_basis is None:
      n = N
    else:
      assert n_basis <= N, 'number of requested orthonormal vectors is greater than the dimensionality of the input'
      n = n_basis

    f0 = f(*args)

    ### (n, N)
    U = rng.rand_ortho(key, size=n, ndim=N)

    delta = tree.tensor_unpack(tensor_def, U)
    perturbed = jax.tree_util.tree_map(lambda x, d: x[None] + scale * d, variables, delta)

    full_arguments = list(args)
    for i, j in enumerate(_argnums):
      full_arguments[j] = perturbed[i]

    f_vmapped = jax.vmap(f, in_axes=[0 if i in _argnums else None for i, _ in enumerate(args)], out_axes=0)

    fs = f_vmapped(*full_arguments)
    fs = (fs - f0) / scale
    grad = jax.tree_util.tree_map(
      lambda d: jnp.sum(d * fs),
      delta
    )

    if isinstance(argnums, int):
      return grad[0]
    else:
      return grad

  return df


def lin_normalize(xs, fs, mu, sigma):
  fs_m = jnp.mean(fs)
  fs_c = fs - fs_m

  xs_n = jax.tree_util.tree_map(lambda x, m: (x - m) / sigma, xs, mu)

  return xs_n, fs_c, fs_m

def lin_recover(W, b, mu, sigma, fs_m):
  W_r = jax.tree_util.tree_map(lambda w: w / sigma, W)

  b_r = b + fs_m - sum(
    jnp.sum(w_r * m) for w_r, m in zip(
      jax.tree_util.tree_leaves(W_r),
      jax.tree_util.tree_leaves(mu),
    )
  )

  return W_r, b_r

def lstsq_fit(xs, fs, mu=None, sigma=None):
  if mu is None:
    mu = jnp.mean(xs, axis=range(fs.ndim))

  if sigma is None:
    sigma = jnp.sqrt(jnp.mean(jnp.square(xs - mu)))

  xs_n, fs_c, fs_m = lin_normalize(xs, fs, mu, sigma)

  tensor, tensor_def = tree.tensor_pack(
    (xs_n, jnp.ones(shape=fs.shape)),
    batch_dimensions=range(fs.ndim)
  )

  M = tensor.reshape((fs.size, tensor.shape[-1]))

  weights, _, _, _ = jnp.linalg.lstsq(M, fs_c.ravel())
  W, offset = tree.tensor_unpack(tensor_def, weights)

  return lin_recover(W, offset, mu, sigma, fs_m)


def quick_lin_fit(xs, fs, mu, sigma, alpha=None):
  fs_m = jnp.mean(fs)

  if alpha is None:
    sqr_sigma = sigma * sigma
  else:
    sqr_sigma = sigma * sigma + alpha * alpha

  W = jax.tree_util.tree_map(
    lambda x, m: jnp.mean(
      (x - m) * array.left_broadcast(fs - fs_m, x),
      axis=range(fs.ndim)
    ) / sqr_sigma,
    xs, mu
  )

  b = fs_m - sum(
    jnp.sum(w * m) for w, m in zip(
      jax.tree_util.tree_leaves(W),
      jax.tree_util.tree_leaves(mu),
    )
  )

  return W, b

def lin_predict(xs, W, b):
  ps = jax.tree_util.tree_map(
    lambda x, w: jnp.sum(x * w, axis=range(x.ndim - w.ndim, x.ndim)),
    xs, W
  )

  return sum(jax.tree_util.tree_leaves(ps)) + b

def lstsq_quad_fit(xs, fs, mu=None, sigma=None):
  if mu is None:
    mu = jnp.mean(xs, axis=range(fs.ndim))

  if sigma is None:
    sigma = jnp.sqrt(jnp.mean(jnp.square(xs - mu)))

  fs_m = jnp.mean(fs)
  fs_c = fs - fs_m

  xs_n = jax.tree_util.tree_map(lambda x, m: (x - m) / sigma, xs, mu)
  xs_sqr_n = jax.tree_util.tree_map(lambda x: jnp.square(x) - 1, xs_n)

  tensor, tensor_def = tree.tensor_pack(
    (xs_sqr_n, xs_n, jnp.ones(shape=fs.shape)),
    batch_dimensions=range(fs.ndim)
  )

  M = tensor.reshape((fs.size, tensor.shape[-1]))

  weights, _, _, _ = jnp.linalg.lstsq(M, fs_c.ravel())
  W_sqr, W_lin, offset = tree.tensor_unpack(tensor_def, weights)

  W_sqr_r = jax.tree_util.tree_map(lambda w_sqr: w_sqr / (sigma * sigma), W_sqr)
  W_lin_r = jax.tree_util.tree_map(
    lambda w_sqr_r, w_lin, m: w_lin / sigma - 2 * w_sqr_r * m,
    W_sqr_r, W_lin, mu
  )

  b_sqr_correction = sum(
    jnp.sum(w_sqr_r * jnp.square(m)) - jnp.sum(w_sqr) for w_sqr_r, w_sqr, m in zip(
      jax.tree_util.tree_leaves(W_sqr_r),
      jax.tree_util.tree_leaves(W_sqr),
      jax.tree_util.tree_leaves(mu),
    )
  )

  b_lin_correction = -sum(
    jnp.sum(w_lin * m) / sigma for w_lin, m in zip(
      jax.tree_util.tree_leaves(W_lin),
      jax.tree_util.tree_leaves(mu),
    )
  )

  b = offset + fs_m + b_sqr_correction + b_lin_correction

  return W_sqr_r, W_lin_r, b

def quad_predict(xs, W_sqr, W_lin, b):
  ps = jax.tree_util.tree_map(
    lambda x, w_sqr, w_lin: \
      jnp.sum(jnp.square(x) * w_sqr, axis=range(x.ndim - w_sqr.ndim, x.ndim)) + \
        jnp.sum(x * w_lin, axis=range(x.ndim - w_lin.ndim, x.ndim)),

    xs, W_sqr, W_lin
  )

  return sum(jax.tree_util.tree_leaves(ps)) + b