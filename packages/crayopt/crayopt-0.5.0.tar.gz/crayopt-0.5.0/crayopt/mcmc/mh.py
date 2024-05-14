from collections import namedtuple

import math

import jax
import jax.numpy as jnp

from typing import Callable

from .. import utils

from .meta import Samples, ZerothOrderMCMC

__all__ = [
  'MetropolisHastings',
  'PriorSampling',
  'MixedMetropolisHastings'
]

MetropolisHastingsState = namedtuple('MetropolisHastingsState', ['samples', 'log_p'])

class MetropolisHastings(ZerothOrderMCMC):
  """
  Metropolis-Hastings algorithm, rejection sampling MCMC with Gaussian proposal distribution.
  """

  State = MetropolisHastingsState

  def __init__(self, alpha: float):
    """
    Metropolis-Hastings algorithm, rejection sampling MCMC with Gaussian proposal distribution.

    :param alpha: scale of the proposal distribution;
    """
    self.alpha = alpha

  def initial_state(self, samples: Samples, log_p: jax.Array) -> MetropolisHastingsState:
    return MetropolisHastingsState(samples=samples, log_p=log_p)

  def finalize(self, state: MetropolisHastingsState) -> Samples:
    return state.samples

  def propose(self, key: jax.Array, state: MetropolisHastingsState) -> Samples:
    return jax.tree_util.tree_map(
      lambda x, k: x + self.alpha * jax.random.normal(k, shape=x.shape, dtype=x.dtype),
      state.samples, utils.rng.tree_split(key, state.samples)
    )

  def __call__(
    self, key: jax.Array,
    proposal: Samples, log_p: jax.Array,
    state: MetropolisHastingsState
  ) -> MetropolisHastingsState:

    log_p_samples = state.log_p
    log_p_proposal = log_p

    ### due to symmetry of the proposal distribution transition probs cancel out
    transition_log_prob = log_p_proposal - log_p_samples

    ### - log U ~ Exp(1)
    log_u = -jax.random.exponential(key, shape=transition_log_prob.shape, dtype=transition_log_prob.dtype)

    accepted = log_u < transition_log_prob

    updated = jax.tree_util.tree_map(
      lambda p, x: jnp.where(
        jnp.expand_dims(accepted, axis=range(accepted.ndim, x.ndim)),
        p, x
      ),
      proposal, state.samples
    )

    log_p_updated = jnp.where(accepted, log_p_proposal, log_p_samples)

    return MetropolisHastingsState(samples=updated, log_p=log_p_updated)

PriorSamplingState = namedtuple('PriorSamplingState', ['current', 'log_p', 'log_prior'])

class PriorSampling(ZerothOrderMCMC):
  """
  A degenerate case of Metropolis-Hastings algorithm where the proposal distribution
  does not depend on the current state of the chain but covers a large space instead.

  In a sense, prior sampling is a Bayesian analog of random search.
  """
  State = PriorSamplingState

  def __init__(self, mean: float=0.0, sigma: float=1.0):
    self.mean = jnp.asarray(mean, dtype=float)
    self.sigma = jnp.asarray(sigma, dtype=float)

  def log_prior(self, sample: Samples, log_p: jax.Array):
    return -0.5 * sum(
      jnp.sum(jnp.square((x - self.mean) / self.sigma), axis=range(log_p.ndim, x.ndim))
      for x in jax.tree_util.tree_leaves(sample)
    )

  def initial_state(self, samples: Samples, log_p: jax.Array) -> PriorSamplingState:
    return PriorSamplingState(current=samples, log_p=log_p, log_prior=self.log_prior(samples, log_p))

  def finalize(self, state: PriorSamplingState) -> Samples:
    return state.current

  def propose(self, key: jax.Array, state: PriorSamplingState) -> Samples:
    return jax.tree_util.tree_map(
      lambda x, k: jax.random.normal(k, shape=x.shape, dtype=x.dtype),
      state.current, utils.rng.tree_split(key, state.current)
    )

  def __call__(
    self, key: jax.Array,
    proposal: Samples, log_p: jax.Array,
    state: PriorSamplingState
  ) -> PriorSamplingState:

    log_p_sample = state.log_p
    log_p_proposal = log_p

    log_prior_sample = state.log_prior
    log_prior_proposal = self.log_prior(proposal, log_p)

    transition_log_prob = log_p_proposal - log_p_sample + log_prior_sample - log_prior_proposal

    log_u = -jax.random.exponential(key, shape=transition_log_prob.shape, dtype=transition_log_prob.dtype)

    accepted = log_u < transition_log_prob

    updated = jax.tree_util.tree_map(
      lambda p, x: jnp.where(jnp.expand_dims(accepted, axis=range(accepted.ndim, x.ndim)), proposal, x),
      proposal, state.current
    )

    updated_log_p = jnp.where(accepted, log_p_proposal, log_p_sample)
    updated_log_prior = jnp.where(accepted, log_prior_proposal, log_prior_sample)

    return PriorSamplingState(updated, log_p=updated_log_p, log_prior=updated_log_prior)

MixedMetropolisHastingsState = namedtuple('MixedMetropolisHastingsState', ['current', 'log_p', 'log_prior'])

class MixedMetropolisHastings(ZerothOrderMCMC):
  """
  A merge between a conventional Metropolis-Hastings (MH) and Prior Sampling (PS) algorithms.

  Proposal distribution in MH is centered around the current state of the chain
  and typically has small standard deviation, thus, it is prone to being stuck in a local minima.
  Proposal distribution in PS is typically very wide and is independent from the current state of the chain,
  however, converges much slower than MH in a convex region.

  Mixed Metropolis Hasting combines both algorithms by sampling proposals from a mixture of the local and the global
  distributions. The algorithm generally follows MH, i.e., slightly perturbs the current sample, however,
  with a certain probability tries to jump into a completely independent location.
  """

  State = PriorSamplingState

  def __init__(self, alpha: float, mean: float=0, sigma: float=1, p_prior: float=0.1):
    self.alpha = alpha
    self.mean = jnp.asarray(mean, dtype=float)
    self.sigma = jnp.asarray(sigma, dtype=float)

    self.p_prior = p_prior

    self.log_p_ps = math.log(p_prior)
    self.log_p_mh = math.log1p(-p_prior)

  def log_prior(self, sample: Samples, log_p: jax.Array):
      return -0.5 * sum(
        jnp.sum(jnp.square((x - self.mean) / self.sigma), axis=range(log_p.ndim, x.ndim))
        for x in jax.tree_util.tree_leaves(sample)
      )

  def initial_state(self, samples: Samples, log_p: jax.Array) -> MixedMetropolisHastingsState:
    return MixedMetropolisHastingsState(samples, log_p=log_p, log_prior=self.log_prior(samples, log_p))

  def finalize(self, state: PriorSamplingState) -> Samples:
    return state.current

  def propose(self, key: jax.Array, state: MixedMetropolisHastingsState) -> Samples:
    key_mh, key_ps, key_mix = jax.random.split(key, num=3)

    proposal_mh = jax.tree_util.tree_map(
      lambda k, x: x + self.alpha * jax.random.normal(k, shape=x.shape, dtype=x.dtype),
      utils.rng.tree_split(key_mh, state.current), state.current
    )
    proposal_ps = jax.tree_util.tree_map(
      lambda k, x: self.mean + self.sigma * jax.random.normal(key, shape=x.shape, dtype=x.dtype),
      utils.rng.tree_split(key_ps, state.current), state.current
    )

    switch_mixture = jax.random.bernoulli(key_mix, p=self.p_prior, shape=state.log_p.shape)

    def mix(w, a, b):
      return jnp.where(jnp.expand_dims(w, axis=range(w.ndim, a.ndim)), a, b)

    return jax.tree_util.tree_map(
      lambda a, b: mix(switch_mixture, a, b),
      proposal_ps, proposal_mh
    )

  def __call__(
    self, key: jax.Array,
    proposal: Samples, log_p: jax.Array,
    state: MixedMetropolisHastingsState
  ) -> MixedMetropolisHastingsState:

    log_p_sample = state.log_p
    log_p_proposal = log_p

    log_prior_sample = state.log_prior
    log_prior_proposal = self.log_prior(proposal, log_p)

    delta = jax.tree_util.tree_map(lambda p, x: p - x, proposal, state.current)

    ### for MH transition probabilities are the same
    log_transition_mh = -0.5 * sum(
      jnp.sum(jnp.square(d / self.alpha), axis=range(log_p_sample.ndim, d.ndim))
      for d in jax.tree_util.tree_leaves(delta)
    )

    log_p_proposal_to_x = jnp.logaddexp(log_prior_sample + self.log_p_ps, log_transition_mh + self.log_p_mh)
    log_p_x_to_proposal = jnp.logaddexp(log_prior_proposal + self.log_p_ps, log_transition_mh + self.log_p_mh)

    transition_log_prob = log_p_proposal - log_p_sample + log_p_proposal_to_x - log_p_x_to_proposal

    log_u = -jax.random.exponential(key, shape=transition_log_prob.shape, dtype=transition_log_prob.dtype)

    accepted = log_u < transition_log_prob

    updated = jax.tree_util.tree_map(
      lambda p, x: jnp.where(jnp.expand_dims(accepted, axis=range(log_p.ndim, len(x.shape))), p, x),
      proposal, state.current
    )

    updated_log_p = jnp.where(accepted, log_p_proposal, log_p_sample)
    updated_log_prior = jnp.where(accepted, log_prior_proposal, log_prior_sample)

    return MixedMetropolisHastingsState(current=updated, log_p=updated_log_p, log_prior=updated_log_prior)