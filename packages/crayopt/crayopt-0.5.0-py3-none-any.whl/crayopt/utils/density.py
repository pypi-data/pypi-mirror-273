import math

import jax
import jax.numpy as jnp

__all__ = [
  'center_mean', 'area', 'levels', 'count', 'project'
]

def center_mean(fs):
  import itertools

  n_comb = 2 ** (fs.ndim)

  return sum(
    fs[shift]
    for shift in itertools.product(*(
      (slice(1, None, None), slice(None, -1, None))
      for _ in range(fs.ndim)
    ))
  ) / n_comb

def area(*xs: jax.Array):
  deltas = [x[1:] - x[:-1] for x in xs]

  broadcasted = []

  for i, ds in enumerate(deltas):
    broadcast = tuple(
      slice(None, None, None) if i == j else None
      for j, _ in enumerate(deltas)
    )
    broadcasted.append(ds[broadcast])

  return math.prod(broadcasted)

def levels(fs: jax.Array, *xs: jax.Array, n: int):
  fs_m = center_mean(fs)
  ds = area(*xs)

  fs_ = fs_m.ravel()
  ds_ = ds.ravel()
  indx = jnp.argsort(fs_ * ds_)
  Fs = jnp.cumsum(fs_[indx] * ds_[indx])

  qs = jnp.linspace(0, Fs[-1], num=n + 1)[1:-1]

  clusters = jnp.sum(Fs[None, :] < qs[:, None], axis=0)

  rev_indx = jnp.argsort(indx)

  clusters_ = clusters[rev_indx]

  probs = jnp.array([
    jnp.sum(fs_[clusters_ == i] * ds_[clusters_ == i])
    for i in range(n)
  ])

  probs = probs / jnp.sum(probs)

  return probs, clusters_.reshape(fs_m.shape)

def count(points, clusters, *xs):
  n = jnp.max(clusters) + 1
  indices = tuple(
    jnp.clip(jnp.searchsorted(x, points[:, i]), 1, x.shape[0] - 1) - 1
    for i, x in enumerate(xs)
  )

  cluster_indx = clusters[indices]

  return jnp.bincount(cluster_indx, minlength=n)

def project(points, log_p, *xs):
  indices = tuple(
    jnp.clip(jnp.searchsorted(x, points[:, i]), 1, x.shape[0] - 1) - 1
    for i, x in enumerate(xs)
  )

  return log_p[indices]