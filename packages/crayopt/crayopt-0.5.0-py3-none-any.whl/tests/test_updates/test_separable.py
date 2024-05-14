import os
import jax
import jax.numpy as jnp

import matplotlib.pyplot as plt

import crayopt


def f(x, w, b):
  return b[:, None] + jnp.matmul(x, w)

def test_separable(seed, plot_root):
  rng = jax.random.PRNGKey(seed)

  rng, key_w, key_x0, key_x, key_eps = jax.random.split(rng, num=5)

  nX, nY = 3, 2
  n, m = 6, 3
  batch = 4

  b_true = jax.random.normal(key_x0, shape=(n, nY))
  w_true = jax.random.normal(key_w, shape=(nX, nY))
  data = jax.random.uniform(key_x, shape=(n, m, nX), minval=-1, maxval=1)

  labels = f(data, w_true, b_true) + 0.1 * jax.random.normal(key_eps, shape=(n, m, nY))

  def loss(X_batch, y_batch, w, x0):
    pred = f(X_batch, w, x0)

    return jnp.mean(jnp.square(pred - y_batch))

  d_loss_d_params = jax.grad(loss, argnums=(2, 3))

  rng, key_w, key_x0 = jax.random.split(rng, num=3)
  initial_b = jax.random.normal(key_x0, shape=(n, nY))
  initial_w = jax.random.normal(key_w, shape=(nX, nY))

  separable_opt = crayopt.separable.adam(learning_rate=1e-2, beta1_separable=None)
  separable_opt_momentum = crayopt.separable.adam(learning_rate=1e-2, beta1_separable=0.9)
  separable_opt_momentum_no_updates = crayopt.separable.adam(
    learning_rate=1e-2, beta1_separable=0.9, update_unselected=False
  )
  opt = crayopt.adam(learning_rate=1e-2)

  @jax.jit
  def step(key, data, labels, w, b, state):
    index = jax.random.randint(key, shape=(batch, ), minval=0, maxval=n)
    X, y = data[index], labels[index]
    grad_w, grad_x0 = d_loss_d_params(X, y, w, b[index])

    G = jax.tree_util.tree_map(
      lambda x, g: jnp.zeros_like(x).at[index].set(g),
      b, grad_x0
    )

    return opt((w, b), (grad_w, G), state)

  @jax.jit
  def separable_step(key, data, labels, w, b, state):
    index = jax.random.randint(key, shape=(batch,), minval=0, maxval=n)
    X, y = data[index], labels[index]
    b, state = separable_opt.advance(index, b, state)
    x0_batch = b[index]
    grad_w, grad_x0 = d_loss_d_params(X, y, w, x0_batch)

    return separable_opt(index, w, b, grad_w, grad_x0, state)

  @jax.jit
  def separable_momentum_step(key, data, labels, w, b, state):
    index = jax.random.randint(key, shape=(batch,), minval=0, maxval=n)
    X, y = data[index], labels[index]
    b, state = separable_opt_momentum.advance(index, b, state)
    x0_batch = b[index]
    grad_w, grad_x0 = d_loss_d_params(X, y, w, x0_batch)

    return separable_opt_momentum(index, w, b, grad_w, grad_x0, state)

  @jax.jit
  def separable_momentum_no_update_step(key, data, labels, w, b, state):
    index = jax.random.randint(key, shape=(batch,), minval=0, maxval=n)
    X, y = data[index], labels[index]
    b, state = separable_opt_momentum_no_updates.advance(index, b, state)
    x0_batch = b[index]
    grad_w, grad_x0 = d_loss_d_params(X, y, w, x0_batch)

    return separable_opt_momentum_no_updates(index, w, b, grad_w, grad_x0, state)

  _, rng_opt = jax.random.split(rng, num=2)

  w, b = initial_w, initial_b
  state = opt.initial_state((initial_w, initial_b))
  for i in range(1024):
    rng_opt, key = jax.random.split(rng_opt)
    (w, b), state = step(key, data, labels, w, b, state)

  w_dense, b_dense = w, b

  _, rng_opt = jax.random.split(rng, num=2)

  w, b = initial_w, initial_b
  state = separable_opt.initial_state(initial_w, initial_b)
  for i in range(1024):
    rng_opt, key = jax.random.split(rng_opt)
    w, b, state = separable_step(key, data, labels, w, b, state)

  w_sparse, b_sparse = w, separable_opt.finalize(b, state)
  assert jnp.all(b_sparse == b)

  _, rng_opt = jax.random.split(rng, num=2)
  w, b = initial_w, initial_b
  state = separable_opt_momentum.initial_state(initial_w, initial_b)
  for i in range(1024):
    rng_opt, key = jax.random.split(rng_opt)
    w, b, state = separable_momentum_step(key, data, labels, w, b, state)

  w_sparse_m, b_sparse_m = w, separable_opt_momentum.finalize(b, state)

  _, rng_opt = jax.random.split(rng, num=2)
  w, b = initial_w, initial_b
  state = separable_opt_momentum_no_updates.initial_state(initial_w, initial_b)
  for i in range(1024):
    rng_opt, key = jax.random.split(rng_opt)
    w, b, state = separable_momentum_no_update_step(key, data, labels, w, b, state)

  w_sparse_m_nu, b_sparse_m_nu = w, separable_opt_momentum_no_updates.finalize(b, state)

  print('---------')
  print(w_dense.ravel())
  print(w_sparse.ravel())
  print(w_sparse_m.ravel())
  print(w_sparse_m_nu.ravel())
  print(w_true.ravel())
  print('---------')
  print(b_dense)
  print(b_sparse)
  print(b_sparse_m)
  print(b_sparse_m_nu)
  print(b_true)

  assert jnp.max(jnp.abs(w_sparse - w_true)) < jnp.max(jnp.abs(initial_w - w_true))
  assert jnp.max(jnp.abs(w_sparse_m - w_true)) < jnp.max(jnp.abs(initial_w - w_true))
  assert jnp.max(jnp.abs(w_sparse_m_nu - w_true)) < jnp.max(jnp.abs(initial_w - w_true))

  assert jnp.max(jnp.abs(b_sparse - b_true)) < jnp.max(jnp.abs(initial_b - b_true))
  assert jnp.max(jnp.abs(b_sparse_m - b_true)) < jnp.max(jnp.abs(initial_b - b_true))
  assert jnp.max(jnp.abs(b_sparse_m_nu - b_true)) < jnp.max(jnp.abs(initial_b - b_true))