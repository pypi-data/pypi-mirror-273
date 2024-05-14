import math

import jax
import jax.numpy as jnp

from . import density
from . import functions

__all__ = [
  'gaussian',
  'gaussian_mixture',
  'gaussian_circle',
  'gaussian_disjoint',
  'hat',
  'himmelblau',
  'rosenbrock_log1p'
]

class Distribution(object):
  def __call__(self, x):
    return self.log_p(x)

  def log_p(self, x):
    raise NotImplementedError()

  def name(self):
    return self.__class__.__name__

  def support(self):
    raise NotImplementedError()

  def sample(self, key: jax.Array, batch: tuple[int, ...] = ()):
    raise NotImplementedError()

  def initial_guess(self, key: jax.Array, batch: tuple[int, ...]=()):
    support = self.support()
    delta = support[1] - support[0]
    origin = support[0]
    return jax.random.uniform(key, minval=0, maxval=1, shape=(*batch, origin.shape[0])) * delta + origin

  def grid(self, n):
    support = self.support()

    xs = tuple(
      jnp.linspace(support[0, i], support[1, i], num=n)
      for i in range(support.shape[1])
    )

    return xs, jnp.stack(jnp.meshgrid(*xs, indexing='ij'), axis=-1)

LOG_2_PI = math.log(2 * math.pi)

class gaussian(Distribution):
  def __init__(self, mean=0.0, sigma=1.0, ndim=2):
    self.mean = jnp.asarray(mean, dtype=float)
    self.sigma = jnp.asarray(sigma, dtype=float)

    if self.mean.ndim < 1:
      self.mean = jnp.broadcast_to(self.mean[None], shape=(ndim, ))
    else:
      assert self.mean.shape[0] == ndim

    if self.sigma.ndim < 1:
      self.sigma = jnp.broadcast_to(self.sigma[None], shape=(ndim,))
    else:
      assert self.sigma.shape[0] == ndim

    self.ndim = ndim

  def log_p(self, x):
    return -jnp.sum(
      jnp.log(self.sigma) + 0.5 * jnp.square((x - self.mean) / self.sigma),
      axis=-1
    ) - 0.5 * self.ndim * LOG_2_PI

  def support(self):
    return jnp.stack([self.mean - 3 * self.sigma, self.mean + 3 * self.sigma], axis=0)

  def sample(self, key: jax.Array, batch: tuple[int, ...]=()):
    eps = jax.random.normal(key, shape=(*batch, self.ndim))
    return self.sigma * eps + self.mean

class gaussian_mixture(Distribution):
  def __init__(self, means, sigmas):
    self.means = jnp.asarray(means, dtype=float)
    self.sigmas = jnp.asarray(sigmas, dtype=float)

  def log_p(self, x):
    import jax.scipy as jsp

    cs = -jnp.log(self.sigmas) - 0.5 * LOG_2_PI

    return jsp.special.logsumexp(
      jnp.sum(cs - 0.5 * jnp.square((x[..., None, :] - self.means) / self.sigmas), axis=-1),
      axis=-1
    ) - math.log(self.means.shape[0])

  def support(self):
    lower = jnp.min(self.means - 3 * self.sigmas, axis=0)
    upper = jnp.max(self.means + 3 * self.sigmas, axis=0)
    return jnp.stack([lower, upper], axis=0)

  def sample(self, key: jax.Array, batch: tuple[int, ...] = ()):
    key_c, key_eps = jax.random.split(key, num=2)
    indx = jax.random.randint(key_c, minval=0, maxval=self.means.shape[0], shape=batch)
    means = self.means[indx]
    stds = self.sigmas[indx]

    eps = jax.random.normal(key_eps, shape=(*batch, means.shape[1]))
    return eps * stds + means

class gaussian_circle(gaussian_mixture):
  def __init__(self, n_components=7, n_dim=2):
    ts = jnp.linspace(0, 2 * jnp.pi, num=n_components)[:-1]
    mus = jnp.stack(
      [jnp.cos(ts), jnp.sin(ts)] + [jnp.zeros(shape=(n_components, )) for _ in range(2, n_dim)],
      axis=-1
    )
    sigma = 2 * jnp.pi / n_components / 4
    sigmas = sigma * jnp.ones(shape=(*ts.shape, n_dim))
    
    super().__init__(mus, sigmas)


class gaussian_disjoint(gaussian_mixture):
  def __init__(self, n_dim=2):
    mus = jnp.array([
      [-1, -1],
      [+1, -1],
      [-1, +1],
      [+1, +1],
    ])
    mus = jnp.concatenate([mus, jnp.zeros(shape=(4, n_dim - 2))], axis=-1)
    sigmas = 0.25 * jnp.ones(shape=(4, n_dim))

    super().__init__(mus, sigmas)

class hat(gaussian_mixture):
  def __init__(self, n_dim=2):
    mus = jnp.zeros(shape=(2, n_dim))
    sigmas = jnp.stack([
      jnp.ones(shape=(n_dim, )),
      0.1 * jnp.ones(shape=(n_dim,))
    ], axis=0)

    super().__init__(mus, sigmas)

class CustomDistribution(Distribution):
  n_grid = 101

  def __init__(self):
    xs, grid = self.grid(self.n_grid)
    ps = jnp.exp(self.f(grid))

    ds = density.area(*xs)
    fs = density.center_mean(ps)
    Z = jnp.sum(ds * fs)

    self.log_Z = jnp.log(Z)
    self.probs = (ds * fs) / Z
    self.xs = xs
    self._grid = grid

  def f(self, x):
    raise NotImplementedError()

  def log_p(self, x):
    return self.f(x) - self.log_Z

  def support(self):
    raise NotImplementedError()

  def sample(self, key: jax.Array, batch: tuple[int, ...] = ()):
    ps = self.probs.ravel()
    fs = jnp.cumsum(ps)

    key_u, key_eps = jax.random.split(key, num=2)

    u = jax.random.uniform(key_u, minval=0, maxval=1, shape=batch)
    indices = jnp.clip(jnp.searchsorted(fs, u), 0, fs.shape[0] - 1)
    indices = jnp.unravel_index(indices, shape=self.probs.shape)

    delta = jax.random.uniform(key_eps, minval=0, maxval=1, shape=(*batch, len(self.xs)))

    return jnp.stack([
      x[indx] + delta[..., i] * (x[indx + 1] - x[indx])
      for i, (x, indx) in enumerate(zip(self.xs, indices))
    ], axis=-1)


class himmelblau(CustomDistribution):
  def f(self, x):
    return -0.025 * functions.himmelblau(x)

  def support(self):
    return jnp.array(functions.himmelblau.search_domain(), dtype=float).T

class rosenbrock_log1p(CustomDistribution):
  def f(self, x):
    ### rosenbrok has a long tail
    sigma = 1.0
    C = -2 * math.log(sigma) - math.log(2 * math.pi)
    return -functions.rosenbrock_2d_log1p(x) - 0.5 * jnp.sum(jnp.square((x - 1) / sigma), axis=-1) + C

  def support(self):
    return jnp.array([
      [-1.5, -0.5],
      [2.5, 3.5]
    ])