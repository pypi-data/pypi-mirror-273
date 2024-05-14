from collections import namedtuple

import math

import jax
import jax.numpy as jnp

from ...utils.array import left_broadcast as lbr
from .meta import SeparableGradientOptimizer, SharedParameters, SeparableParameters

__all__ = [
  'adam'
]

AdamState = namedtuple(
  'AdamState', [
    'shared_first_momentum',
    'separable_first_momentum',

    'shared_second_momentum',
    'separable_second_momentum',

    'last_updated',
    'iteration',
  ]
)

class adam(SeparableGradientOptimizer):
  State = AdamState

  def __init__(
    self,
    learning_rate=1e-3,
    beta1=0.9, beta2=0.999,
    beta1_separable=None, beta2_separable=0.99,
    update_unselected: bool=True,
    eps=1e-8
  ):
    """
    Implementation of Adam optimizer for the separable case.

    Note: commonly, separable parameters correspond to individual samples, thus, noise due to subsampling only
    affects shared parameters. Thus, by default, momentum is disabled for the separable parameters
    (i.e., `beta1_separable=None`).

    :param learning_rate: learning rate, roughly corresponds to the scale of parameter updates;
    :param beta1: exponential decay rate for the first momentum corresponding to shared parameters;
    :param beta2: exponential decay rate for the second momentum corresponding to shared parameters;
    :param beta1_separable: exponential decay rate for the first momentum of separable parameters,
      if None the momentum is disabled.
    :param beta2_separable: exponential decay rate for the first momentum of separable parameters;
    :param update_unselected: if True mimics adam's behaviour assuming that the gradients of separable
      parameters not selected in a batch are zeros, i.e., updating momenta and advancing
      the parameters (computed lazily) due to the first momentum (if beta1_separable is not None), otherwise,
      the updates happen only for the samples selected for the batch.
    :param eps: a small bias for numerical stability.
    """
    super(adam, self).__init__()
    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    self.beta1_separable = beta1_separable
    self.beta2_separable = beta2_separable

    self.update_unselected = update_unselected

    self.beta1_over_sqrt_beta2 = self.beta1 / math.sqrt(self.beta2)
    if self.beta1_separable is None:
      self.beta1_over_sqrt_beta2_separable = None
    else:
      self.beta1_over_sqrt_beta2_separable = self.beta1_separable / math.sqrt(self.beta2_separable)

    self.eps = eps

  def initial_state(self, shared: SharedParameters, separable: SeparableParameters) -> AdamState:
    from ... import utils
    dtype = utils.dtype.get_common_dtype((shared, separable))

    n_batch, = set(x.shape[0] for x in jax.tree_util.tree_leaves(separable))

    return AdamState(
      shared_first_momentum=jax.tree_util.tree_map(jnp.zeros_like, shared),
      separable_first_momentum=(
        None if self.beta1_separable is None else jax.tree_util.tree_map(jnp.zeros_like, separable)
      ),
      shared_second_momentum=jax.tree_util.tree_map(jnp.zeros_like, shared),
      separable_second_momentum=jax.tree_util.tree_map(jnp.zeros_like, separable),

      last_updated=jnp.zeros(shape=(n_batch, ), dtype=dtype),
      iteration=jnp.zeros(shape=(), dtype=dtype),
    )

  def advance(
    self,
    index: jax.Array,
    separable: SeparableParameters,
    state: AdamState
  ) -> tuple[SeparableParameters, AdamState]:
    delta = state.iteration - state.last_updated[index]
    ### for computing updates analytically, we assume that effective learning rate = const
    ### for stability, we compute it for the earliest update

    if not self.update_unselected:
      return separable, state

    if self.beta1_separable is None:
      ### only second momentum update
      separable_updated = separable
      separable_first_momentum_updated = None

    else:
      effective_beta1 = jnp.power(self.beta1, state.last_updated[index] + 1)
      effective_beta2 = jnp.power(self.beta2, state.last_updated[index] + 1)
      effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2) / (1 - effective_beta1)

      factor = (1 - jnp.power(self.beta1_over_sqrt_beta2, delta)) / (1 - self.beta1_over_sqrt_beta2)

      separable_updated = jax.tree_util.tree_map(
        lambda x, v, m: x.at[index].set(
          x[index] - lbr(effective_learning_rate * factor, x[index]) * v[index] / (jnp.sqrt(m[index]) + self.eps)
        ),
        separable, state.separable_first_momentum, state.separable_second_momentum
      )

      separable_first_momentum_updated = jax.tree_util.tree_map(
        lambda v: v.at[index].set(
          lbr(jnp.power(self.beta1, delta), v[index]) * v[index]
        ),
        state.separable_first_momentum
      )

    separable_second_momentum_updated = jax.tree_util.tree_map(
      lambda m: m.at[index].set(
        lbr(jnp.power(self.beta2, delta), m[index]) * m[index]
      ),
      state.separable_second_momentum
    )

    last_updated_updated = state.last_updated.at[index].set(state.iteration)

    return separable_updated, AdamState(
      shared_first_momentum=state.shared_first_momentum,
      shared_second_momentum=state.shared_second_momentum,

      separable_first_momentum=separable_first_momentum_updated,
      separable_second_momentum=separable_second_momentum_updated,

      last_updated=last_updated_updated,
      iteration=state.iteration
    )

  def finalize(self, separable: SeparableParameters, state: AdamState):
    n, = set(x.shape[0] for x in jax.tree_util.tree_leaves(separable))

    separable_updated, state_updated = self.advance(jnp.arange(n), separable, state)

    return separable_updated

  def __call__(
    self,
    index: jax.Array,
    shared: SharedParameters, separable: SeparableParameters,
    shared_gradient: SharedParameters, separable_gradient: SeparableParameters,
    state: AdamState
  ) -> tuple[SharedParameters, SeparableParameters, AdamState]:
    iteration_updated = state.iteration + 1

    effective_beta1 = jnp.power(self.beta1, iteration_updated)
    effective_beta2 = jnp.power(self.beta2, iteration_updated)
    effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2) / (1 - effective_beta1)

    shared_first_momentum_updated = jax.tree_util.tree_map(
      lambda v, g: self.beta1 * v + (1 - self.beta1) * g,
      state.shared_first_momentum, shared_gradient
    )

    shared_second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.beta2 * m + (1 - self.beta2) * jnp.square(g),
      state.shared_second_momentum, shared_gradient
    )

    updated_shared = jax.tree_util.tree_map(
      lambda x, v, m: x - effective_learning_rate * v / (jnp.sqrt(m) + self.eps),
      shared, shared_first_momentum_updated, shared_second_momentum_updated
    )

    ### separable updates

    separable_second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: m.at[index].set(self.beta2_separable * m[index] + (1 - self.beta2_separable) * jnp.square(g)),
      state.separable_second_momentum, separable_gradient
    )

    effective_beta2_separable = jnp.power(self.beta2_separable, iteration_updated)

    if self.beta1_separable is None:
      separable_first_momentum_updated = None
      ### effective beta1 = 0
      effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2_separable)

      updated_separable = jax.tree_util.tree_map(
        lambda x, g, m: x.at[index].set(
          x[index] - effective_learning_rate * g / (jnp.sqrt(m[index]) + self.eps)
        ),
        separable, separable_gradient, separable_second_momentum_updated
      )
    else:
      separable_first_momentum_updated = jax.tree_util.tree_map(
        lambda v, g: v.at[index].set(self.beta1_separable * v[index] + (1 - self.beta1_separable) * g),
        state.separable_first_momentum, separable_gradient
      )

      effective_beta1_separable = jnp.power(self.beta1_separable, iteration_updated)

      effective_learning_rate = \
        self.learning_rate * jnp.sqrt(1 - effective_beta2_separable) / (1 - effective_beta1_separable)

      updated_separable = jax.tree_util.tree_map(
        lambda x, v, m: x.at[index].set(
          x[index] - effective_learning_rate * v[index] / (jnp.sqrt(m[index]) + self.eps)
        ),
        separable, separable_first_momentum_updated, separable_second_momentum_updated
      )

    last_updated_updated = state.last_updated.at[index].set(iteration_updated)

    return updated_shared, updated_separable, AdamState(
      shared_first_momentum=shared_first_momentum_updated,
      shared_second_momentum=shared_second_momentum_updated,

      separable_first_momentum=separable_first_momentum_updated,
      separable_second_momentum=separable_second_momentum_updated,

      last_updated=last_updated_updated,
      iteration=iteration_updated
    )