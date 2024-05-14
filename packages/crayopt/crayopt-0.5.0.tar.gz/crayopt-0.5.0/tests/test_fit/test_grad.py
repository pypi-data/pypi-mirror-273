import jax
import jax.numpy as jnp

from crayopt.utils.fit import ortho_grad

def test_ortho_grad(seed):
  rng = jax.random.PRNGKey(seed)

  def f(x, y, z):
    return 2 * x / (y + 5 * z)

  df = jax.grad(f, argnums=(0, 1, 2))

  x, y, z = jnp.array(1.0), jnp.array(2.0), jnp.array(0.5)
  gx, gy, gz = ortho_grad(f, argnums=(0, 1, 2))(rng, x, y, z)

  ax, ay, az = df(x, y, z)

  assert jnp.abs(ax - gx) < 1.0e-3
  assert jnp.abs(ay - gy) < 1.0e-3
  assert jnp.abs(az - gz) < 1.0e-3

  print(gx, gy, gz)
  print(df(x, y, z))

  g1z, g1x, g1y = ortho_grad(f, argnums=(2, 0, 1))(rng, x, y, z)

  assert jnp.abs(ax - g1x) < 1.0e-3
  assert jnp.abs(ay - g1y) < 1.0e-3
  assert jnp.abs(az - g1z) < 1.0e-3

  g2z, g2x = ortho_grad(f, argnums=(2, 0))(rng, x, y, z)
  g2y, = ortho_grad(f, argnums=(1, ))(rng, x, y, z)

  assert jnp.abs(ax - g2x) < 1.0e-3
  assert jnp.abs(ay - g2y) < 1.0e-3
  assert jnp.abs(az - g2z) < 1.0e-3

  g3y = ortho_grad(f, argnums=1)(rng, x, y, z)

  assert isinstance(g3y, jax.Array)
  assert jnp.abs(ay - g3y) < 1.0e-3


