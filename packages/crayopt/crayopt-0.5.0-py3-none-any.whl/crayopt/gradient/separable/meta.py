from typing import TypeVar

import jax

__all__ = [
  'SeparableGradientOptimizer',

  'SharedParameters',
  'SeparableParameters'
]

SharedParameters = TypeVar('SharedParameters')
SeparableParameters = TypeVar('SeparableParameters')


class SeparableGradientOptimizer(object):
  State: type

  def initial_state(self, shared: SharedParameters, separable: SeparableParameters) -> 'State':
    raise NotImplementedError()

  def advance(
    self,
    index: jax.Array,
    separable: SeparableParameters,
    state: 'State'
  ) -> tuple[SeparableParameters, 'State']:
    """
    Applies zero updates to a subset separable parameters given by `index`.

    :param index: array of int, subset if separable parameters the updates should be applied to;
    :param separable: full parameters tree;
    :param state: optimizer state;
    :return: updated separable parameters, updated state.
    """
    raise NotImplementedError()

  def __call__(
    self,
    index: jax.Array,
    shared: SharedParameters, separable: SeparableParameters,
    shared_gradient: SharedParameters, separable_parameters: SeparableParameters,
    state: 'State'
  ) -> tuple[SharedParameters, SeparableParameters, 'State']:
    raise NotImplementedError()