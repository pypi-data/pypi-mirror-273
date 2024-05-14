import jax
import jax.numpy as jnp

from crayopt.utils.rng import rand_ortho, rand_ortho_extension

def test_ortho(seed):
  rng = jax.random.PRNGKey(seed)
  n = 32
  m = 7
  for _ in range(32):
    key, rng = jax.random.split(rng, num=2)
    U = rand_ortho(rng, m, n)

    assert U.shape == (m, n)
    I_ = jnp.matmul(U, U.T)
    assert jnp.max(jnp.abs(I_ - jnp.eye(m))) < 1.0e-6

  for _ in range(32):
    key_U, key_v, rng = jax.random.split(rng, num=3)
    v = jax.random.normal(key_v, shape=(n, ))
    v = v / jnp.sqrt(jnp.sum(jnp.square(v)))

    U = rand_ortho_extension(rng, v, m)
    assert U.shape == (m, n)
    assert abs(jnp.abs(jnp.dot(U[0], v)) - 1) < 1.0e-3

    I_ = jnp.matmul(U, U.T)
    assert jnp.max(jnp.abs(I_ - jnp.eye(m))) < 1.0e-6

  key_A, key_v, rng = jax.random.split(rng, num=3)
  v = jax.random.normal(key_v, shape=(n,))
  v = v / jnp.sqrt(jnp.sum(jnp.square(v)))

  A = jnp.concatenate([
    jax.random.normal(key_A, shape=(n, m - 1)),
    v[:, None]
  ], axis=1)

  Q, R = jnp.linalg.qr(A)

  print(Q.T @ v)

  A = jnp.concatenate([
    v[:, None],
    jax.random.normal(key_A, shape=(n, m - 1)),
  ], axis=1)

  Q, R = jnp.linalg.qr(A)

  print(Q.T @ v)
