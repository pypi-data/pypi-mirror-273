from collections import namedtuple

import math

import jax
import jax.numpy as jnp

from .meta import BlackBoxOptimizer, Parameters
from ..utils.array import left_broadcast
from ..utils.tree import tensor_pack, tensor_unpack, tensor_definition, tensor_size
from ..utils.rng import rand_ortho, rand_ortho_extension, tree_split

__all__ = [
  'uadam',
]


UAdamState = namedtuple(
  'UAdamState',
  ['current', 'first_momentum', 'second_momentum', 'effective_beta1', 'effective_beta2']
)

class uadam(BlackBoxOptimizer):
  State = UAdamState

  def __init__(
    self,
    learning_rate=1e-3, beta1=0.9, beta2=0.999,
    scale=None, alpha=0.1,
    eps=1e-8
  ):
    super(uadam, self).__init__()
    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    if scale is None:
      self.scale = learning_rate
    else:
      self.scale = scale

    self.alpha = alpha

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> UAdamState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return UAdamState(
      current=parameters,
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      effective_beta1=jnp.ones(shape=tuple(), dtype=dtype),
      effective_beta2=jnp.ones(shape=tuple(), dtype=dtype),
    )

  def propose(self, key: jax.Array, state: UAdamState, batch: tuple[int, ...] = ()) -> Parameters:
    key_v, key_U = jax.random.split(key, num=2)

    if self.alpha is None:
      ndim = tensor_size(state.current, batch_dimensions=())
      tensor_def = tensor_definition(state.current, batch_dimensions=())
      U = rand_ortho(key, size=math.prod(batch), ndim=ndim)
    else:
      current_v = jax.tree_util.tree_map(
        lambda k, v, m: v / jnp.sqrt(m + self.eps) + self.alpha * jax.random.normal(k, shape=v.shape, dtype=v.dtype),
        tree_split(key_v, state.first_momentum), state.first_momentum, state.second_momentum
      )

      u, tensor_def = tensor_pack(current_v, batch_dimensions=())
      U = rand_ortho_extension(key, u, size=math.prod(batch))

    U = jnp.reshape(U, (*batch, U.shape[1]))
    delta = tensor_unpack(tensor_def, U)

    broadcast = tuple(None for _ in batch)

    return jax.tree_util.tree_map(
      lambda x, d: x[broadcast] + self.scale * d,
      state.current, delta
    )

  def __call__(
    self, proposal: Parameters, values: jax.Array, state: UAdamState
  ) -> tuple[Parameters, UAdamState]:
    vs = values - jnp.mean(values)

    gradient = jax.tree_util.tree_map(
      lambda p, c: jnp.sum(
        (p - c) * left_broadcast(vs, p) / self.scale / self.scale,
        axis=range(values.ndim)
      ),
      proposal, state.current
    )

    first_momentum_updated = jax.tree_util.tree_map(
      lambda v, g: self.beta1 * v + (1 - self.beta1) * g,
      state.first_momentum, gradient
    )

    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.beta2 * m + (1 - self.beta2) * jnp.square(g),
      state.second_momentum, gradient
    )

    effective_beta1 = state.effective_beta1 * self.beta1
    effective_beta2 = state.effective_beta2 * self.beta2

    effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2) / (1 - effective_beta1)

    updated_parameters = jax.tree_util.tree_map(
      lambda x, v, m: x - effective_learning_rate * v / (jnp.sqrt(m) + self.eps),
      state.current, first_momentum_updated, second_momentum_updated
    )

    return updated_parameters, UAdamState(
      current=updated_parameters,
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
      effective_beta1=effective_beta1,
      effective_beta2=effective_beta2
    )