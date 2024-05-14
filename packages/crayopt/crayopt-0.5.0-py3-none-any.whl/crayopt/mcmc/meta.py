import jax
import jax.numpy as jnp

from typing import TypeVar, Callable

__all__ = [
  'MCMC', 'ZerothOrderMCMC', 'FirstOrderMCMC',
  'Samples',
]

Samples = TypeVar('Samples')

class MCMC(object):
  """
  The base class for Markov-Chain Monte-Carlo methods.
  """

  State: type

  def finalize(self, state: 'State') -> Samples:
    raise NotImplementedError()

  def propose(self, key: jax.Array, state: 'State') -> Samples:
    raise NotImplementedError()


class ZerothOrderMCMC(MCMC):
  """
  The base class for 'zero-order' Markov-Chain Monte-Carlo methods that use only `log_p` evaluations.
  """

  State: type

  def initial_state(self, samples: Samples, log_p: jax.Array) -> 'State':
    raise NotImplementedError()

  def __call__(self, key: jax.Array, proposal: Samples, log_p: jax.Array, state: 'State') -> 'State':
    raise NotImplementedError()


class FirstOrderMCMC(MCMC):
  """
  The base class for first-order Markov-Chain Monte-Carlo methods that use `log_p` and gradient evaluations.
  """

  State: type

  def initial_state(self, samples: Samples, log_p: jax.Array, grad_log_p: Samples) -> 'State':
    raise NotImplementedError()

  def __call__(self, key: jax.Array, proposal: Samples, log_p: jax.Array, grad_log_p: Samples, state: 'State') -> 'State':
    raise NotImplementedError()
