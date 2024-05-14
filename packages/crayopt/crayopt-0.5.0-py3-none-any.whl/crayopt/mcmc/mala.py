from typing import Sequence
from collections import namedtuple

import math

import jax
import jax.numpy as jnp

from .. import utils
from .meta import Samples, FirstOrderMCMC

__all__ = [
  'MALA',
  'AdaLangevin',
]

def log_prob_transition(random_walk: Samples, alpha: float, batch_dims: int=1) -> jnp.ndarray:
  """
  Returns unnormalized log probabilities for a random walk instance `random_walk` generated with step size `alpha`.
  :param random_walk: an instance of random walk as returned by `langevin_step`;
  :param alpha: step size used to generate the instance of random walk, i.e., sigma = sqrt(2 * alpha)
  :param batch_dims: number of batch dimensions;
  :return: unnormalized log probabilities.
  """

  return utils.tree.tree_map_sum(
    lambda eps: (-0.25 / alpha) * jnp.sum(jnp.square(eps), axis=range(batch_dims, eps.ndim)),
    random_walk
  )

MALAState = namedtuple('MALAState', ['samples', 'log_p', 'grad_log_p'])

class MALA(FirstOrderMCMC):
  """
  Monte-Carlo Markov chain based on descritized Langevin dynamics with rejection sampling,
  also known as Metropolis adjusted Langevin algorithm (MALA).
  Continuous Langevin dynamics converges on the target distribution, however, the discrete version
  requires rejection sampling to avoid biases due to finite steps.
  """

  State = MALAState

  def __init__(self, alpha: float, rejection_sampling: bool=True):
    self.alpha = alpha
    self.sqrt_2_alpha = math.sqrt(2 * self.alpha)
    self.rejection_sampling = rejection_sampling

  def initial_state(self, samples: Samples, log_p: jax.Array, grad_log_p: Samples) -> MALAState:
    return MALAState(samples, log_p, grad_log_p)

  def finalize(self, state: MALAState) -> Samples:
    return state.samples

  def propose(self, key: jax.Array, state: MALAState) -> Samples:
    random_walk = jax.tree_util.tree_map(
      lambda x, k: jax.random.normal(k, shape=x.shape, dtype=x.dtype),
      state.samples,
      utils.rng.tree_split(key, state.samples)
    )
    return jax.tree_util.tree_map(
      lambda x, g, eps: x + self.alpha * g + self.sqrt_2_alpha * eps,
      state.samples,
      state.grad_log_p,
      random_walk
    )

  def __call__(
    self, key: jax.Array,
    proposal: Samples, log_p: jax.Array, grad_log_p: Samples,
    state: MALAState
  ) -> MALAState:
    if not self.rejection_sampling:
      return MALAState(proposal, log_p, grad_log_p)

    else:
      samples = state.samples
      log_p_samples = state.log_p
      grad_log_p_samples = state.grad_log_p

      log_p_proposal = log_p
      grad_log_p_proposal = grad_log_p

      delta = jax.tree_util.tree_map(
        lambda x, p: p - x,
        samples, proposal
      )

      noise = jax.tree_util.tree_map(
        lambda d, g: d - self.alpha * g,
        delta, grad_log_p_samples
      )

      log_p_x_to_proposal = log_prob_transition(noise, self.alpha, log_p.ndim)

      delta_sample = jax.tree_util.tree_map(
        lambda d, gp: d + self.alpha * gp,
        delta, grad_log_p_proposal
      )

      log_p_proposal_to_x = log_prob_transition(delta_sample, self.alpha, log_p.ndim)

      transition_log_prob = log_p_proposal - log_p_samples  + log_p_proposal_to_x - log_p_x_to_proposal

      log_u = -jax.random.exponential(key, shape=transition_log_prob.shape, dtype=transition_log_prob.dtype)

      accepted = log_u < transition_log_prob

      updated = jax.tree_util.tree_map(
        lambda x, p: jnp.where(jnp.expand_dims(accepted, axis=range(accepted.ndim, x.ndim)), p, x),
        samples, proposal
      )

      updated_log_p = jnp.where(accepted, log_p_proposal, log_p_samples)
      updated_grad_log_p = jax.tree_util.tree_map(
        lambda gx, gp: jnp.where(jnp.expand_dims(accepted, axis=range(accepted.ndim, gx.ndim)), gp, gx),
        grad_log_p_samples, grad_log_p_proposal
      )

      return MALAState(updated, updated_log_p, updated_grad_log_p)

AdaLangevinState = namedtuple('AdaLangevinState', [
  'samples', 'log_p', 'grad_log_p', 'second_momentum', 'uniform',
])

class AdaLangevin(FirstOrderMCMC):
  """
  Adaptive version of Langevin sampler that uses adam-like normalization.
  This sampler is approximate --- it samples more frequently from regions with high gradient!
  """

  State = AdaLangevinState

  def __init__(self, alpha: float, rho: float=0.99, eps: float=1e-9):
    self.alpha = alpha
    self.rho = rho
    self.eps = eps

  def initial_state(self, samples: Samples, log_p: jax.Array, grad_log_p: Samples) -> AdaLangevinState:
    return AdaLangevinState(
      samples, log_p, grad_log_p,
      second_momentum=jax.tree_util.tree_map(lambda g: jnp.square(g), grad_log_p),
      uniform=samples,
    )

  def finalize(self, state: AdaLangevinState) -> Samples:
    return state.uniform

  def propose(self, key: jax.Array, state: AdaLangevinState) -> Samples:
    random_walk = jax.tree_util.tree_map(
      lambda x, k: jax.random.normal(k, shape=x.shape, dtype=x.dtype),
      state.samples,
      utils.rng.tree_split(key, state.samples)
    )

    normalization = jax.tree_util.tree_map(
      lambda m: self.alpha / jnp.sqrt(m + self.eps),
      state.second_momentum
    )

    return jax.tree_util.tree_map(
      lambda x, g, eps, norm: x + \
                              utils.array.left_broadcast(norm, g) * g + \
                              utils.array.left_broadcast(jnp.sqrt(2 * norm), eps) * eps,
      state.samples,
      state.grad_log_p,
      random_walk,
      normalization
    )

  def __call__(
    self, key: jax.Array,
    proposal: Samples, log_p: jax.Array, grad_log_p: Samples,
    state: AdaLangevinState
  ) -> AdaLangevinState:
    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.rho * m + (1 - self.rho) * jnp.square(g),
      state.second_momentum, grad_log_p
    )
    return AdaLangevinState(
      proposal, log_p, grad_log_p, second_momentum_updated,
      uniform=proposal,
    )