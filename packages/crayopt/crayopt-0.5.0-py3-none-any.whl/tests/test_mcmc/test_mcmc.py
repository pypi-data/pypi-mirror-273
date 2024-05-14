import os
import time

import pytest

import jax
import jax.numpy as jnp
import numpy as np

import crayopt

import matplotlib.pyplot as plt

def test_switch(seed):
  rng = jax.random.PRNGKey(seed)

  key_x, key_y, key_s = jax.random.split(rng, num=3)

  x = jax.random.normal(key_x, shape=(1024, 64))
  y = jax.random.normal(key_y, shape=(1024, 64))
  s = jax.random.normal(key_s, shape=(1024, ))

  @jax.jit
  def switch_where(a, b, switch):
    switch = switch < 0
    return jnp.where(
      jnp.expand_dims(switch, axis=range(switch.ndim, a.ndim)),
      a, b
    )

  @jax.jit
  def switch_mul(a, b, switch):
    switch = switch < 0
    switch = jnp.expand_dims(switch, axis=range(switch.ndim, a.ndim))
    return a * switch + (1 - switch) * b

  _ = switch_where(x, y, s)
  _ = switch_mul(x, y, s)

  n = 4 * 1024

  t_0 = time.perf_counter_ns()
  for _ in range(n):
    switch_where(x, y, s)
  t_n = time.perf_counter_ns()
  switch_speed = n / (t_n - t_0) * 1.0e+9
  print('Switch where: {:.1f} iter per sec'.format(switch_speed))

  t_0 = time.perf_counter_ns()
  for _ in range(n):
    switch_mul(x, y, s)
  t_n = time.perf_counter_ns()
  mul_speed = n / (t_n - t_0) * 1.0e+9
  print('Switch multiply: {:.1f} iter per sec'.format(mul_speed))

def test_stability(seed, plot_root):
  rng = jax.random.PRNGKey(seed)

  ndim = 2

  @jax.jit
  def normal_log_p(xs):
    return -0.5 * jnp.sum(jnp.square(xs), axis=-1)

  grad_normal_log_p = jax.vmap(jax.value_and_grad(normal_log_p), in_axes=(0, ), out_axes=0)

  zero_order_algorithms = dict(
    MH=crayopt.MetropolisHastings(alpha=1.0e-1),
    PS=crayopt.PriorSampling(mean=0.0, sigma=1),
    MMH=crayopt.MixedMetropolisHastings(alpha=1.0e-2, mean=0.0, sigma=1, p_prior=0.1),
  )

  first_order_algorithms = dict(
    Langevin=crayopt.MALA(alpha=1.0e-2, rejection_sampling=False),
    MALA=crayopt.MALA(alpha=1.0e-2, rejection_sampling=True),
    AdaLangevin=crayopt.AdaLangevin(alpha=1.0e-2, rho=0.9),
  )

  approximate_algorithms = {'AdaLangevin', }

  n_samples = 128
  n_steps = 8 * 1024

  rng, key_x0 = jax.random.split(rng, num=2)
  initial_guess = jax.random.normal(key_x0, shape=(n_samples, ndim))

  samples = dict()

  for name, algo in zero_order_algorithms.items():
    @jax.jit
    def step(k, state):
      key_proposal, key_step = jax.random.split(k, num=2)
      proposal = algo.propose(key_proposal, state)
      log_p = normal_log_p(proposal)
      return algo(key_step, proposal, log_p, state)

    state = algo.initial_state(initial_guess, normal_log_p(initial_guess))
    for _ in range(n_steps):
      rng, key = jax.random.split(rng, num=2)
      state = step(key, state)

    samples[name] = algo.finalize(state)

  for name, algo in first_order_algorithms.items():
    @jax.jit
    def step(k, state):
      key_proposal, key_step = jax.random.split(k, num=2)
      proposal = algo.propose(key_proposal, state)
      log_p, grad_log_p = grad_normal_log_p(proposal)
      return algo(key_step, proposal, log_p, grad_log_p, state)

    state = algo.initial_state(initial_guess, *grad_normal_log_p(initial_guess))
    for _ in range(n_steps):
      rng, key = jax.random.split(rng, num=2)
      state = step(key, state)

    samples[name] = algo.finalize(state)

  expected = jnp.eye(ndim)

  import scipy.stats as sps

  for name, X in samples.items():
    print(f'{name}:')
    res = sps.normaltest(X, axis=0)
    print(f'  p-values: {res.pvalue}')

    mean = jnp.mean(X, axis=0)
    print(f'  means: {mean} / {mean * jnp.sqrt(n_samples)})')
    cov = jnp.matmul(X.T, X) / n_samples
    print(f'  covariance:\n{cov}')

    if name not in approximate_algorithms:
      if jnp.any(res.pvalue < 0.01):
        fig = plt.figure()
        axes = fig.subplots()
        axes.scatter(X[:, 0], X[:, 1], label=name)
        fig.savefig(os.path.join(plot_root, f'{name}.png'))

        raise Exception(name)

      ### 5 sigma
      assert jnp.all(jnp.abs(mean) < 5 / jnp.sqrt(n_samples))
      assert jnp.max(jnp.abs(cov - expected)) < 10.0 / jnp.sqrt(n_samples), f'{name}: {cov}'

### scipy one does not handle float32 well
def rf_js(x_obs: jax.Array, x_true: jax.Array, cv: int=5, eps: float=1e-6):
  from sklearn.ensemble import RandomForestClassifier
  from sklearn.model_selection import cross_val_predict

  clf = RandomForestClassifier(n_estimators=32, min_samples_leaf=32)
  X = np.concatenate([x_obs, x_true], axis=0)
  y = np.concatenate([np.zeros(x_obs.shape[0]), np.ones(x_true.shape[0])], axis=0)

  p = cross_val_predict(clf, X, y, cv=cv, method='predict_proba')[:, 1]
  ce = -jnp.mean(y * jnp.log(p + eps) + (1 - y) * jnp.log(1 - p + eps))
  return jnp.maximum(jnp.log(2) - ce, 0.0)

def calibrate_kde(x, grid, log_p):
  from sklearn.neighbors import KernelDensity
  from scipy.optimize import minimize_scalar
  ndim = grid.shape[-1]
  ps = jnp.exp(log_p)

  grid_ = grid.reshape((-1, ndim))

  area = jnp.prod(jnp.max(grid_, axis=0) - jnp.min(grid_, axis=0))
  ### ndim - 0.5 to make the total area -> inf while w -> 0 when n -> inf;
  w_0 = float(jnp.power(area / x.shape[0], 1 / ndim))

  def kl(w):
    log_kd = KernelDensity(bandwidth=float(w)).fit(x).score_samples(grid_).reshape(grid.shape[:-1])

    return jnp.sum(ps * log_p - ps * log_kd)

  result = minimize_scalar(kl, bounds=(0.1 * w_0, 10.0 * w_0), method='bounded')

  return result.x

def kde_kl(x_obs, grid, log_p, w):
  from sklearn.neighbors import KernelDensity
  ndim = grid.shape[-1]
  ps = jnp.exp(log_p)
  grid_ = grid.reshape((-1, ndim))
  log_kd = KernelDensity(bandwidth=float(w)).fit(x_obs).score_samples(grid_).reshape(grid.shape[:-1])

  return log_kd, jnp.sum(ps * log_p - ps * log_kd)

def ensemble(key, task, initial, n_steps):
  from emcee import EnsembleSampler
  log_prob_fn = jax.jit(task.log_p)
  sampler = EnsembleSampler(nwalkers=initial.shape[0], ndim=initial.shape[1], log_prob_fn=log_prob_fn)
  sampler.run_mcmc(initial, n_steps)
  sample, *_ = sampler.get_last_sample()
  return sample

def nuts(learning_rate):
  def mcmc(key, task, initial, n_steps):
    import blackjax

    chain = blackjax.nuts(
      task.log_p,
      step_size=learning_rate,
      inverse_mass_matrix=jnp.ones(shape=(initial.shape[-1], ))
    )

    @jax.jit
    def step(key, state):
      return jax.vmap(chain.step, in_axes=(0, 0))(jax.random.split(key, num=state.position.shape[0]), state)

    key_init, key = jax.random.split(key, num=2)
    state = jax.vmap(chain.init, in_axes=(0, 0))(initial, jax.random.split(key_init, num=initial.shape[0]))

    for _ in range(n_steps):
      key_step, key = jax.random.split(key, num=2)
      state, _ = step(key_step, state)

    return state.position

  return mcmc


tasks = [
  crayopt.utils.distributions.gaussian(),
  crayopt.utils.distributions.gaussian_circle(),
  crayopt.utils.distributions.gaussian_disjoint(),
  crayopt.utils.distributions.hat(),
  crayopt.utils.distributions.himmelblau(),
  crayopt.utils.distributions.rosenbrock_log1p()
]

def test_debug(seed, plot_root):
  task = crayopt.utils.distributions.gaussian()
  test_mh_like(task, seed, plot_root)

@pytest.mark.parametrize('task', tasks, ids=[task.name() for task in tasks])
def test_mh_like(task, seed, plot_root):
  rng = jax.random.PRNGKey(seed)

  zero_order_algorithms = dict(
    # MH=crayopt.MetropolisHastings(alpha=1.0e-1),
    # # TauMH=crayopt.CMetropolisHastings(alpha=1.0e-2),
    # PS=crayopt.PriorSampling(mean=0.0, sigma=2),
    # MMH=crayopt.MixedMetropolisHastings(alpha=1.0e-1, mean=0.0, sigma=2, p_prior=0.1),
  )

  first_order_algorithms = dict(
    Langevin=crayopt.MALA(alpha=1.0e-2, rejection_sampling=False),
    MALA=crayopt.MALA(alpha=1.0e-2, rejection_sampling=True),
    AdaLangevin=crayopt.AdaLangevin(alpha=1.0e-2, rho=0.9),
  )

  foreign = dict(
    # ensemble=ensemble,
    # nuts=nuts(learning_rate=1.0e-2)
    # tau_langevin=tau_langevin,
  )

  xs, grid = task.grid(101)
  log_p = task.log_p(grid)

  get_grad_log_p = jax.vmap(
    jax.value_and_grad(task.log_p, argnums=0),
    in_axes=(0,),
    out_axes=0
  )

  n_steps = 8 * 1024
  n_samples = 1024

  rng, key_x0, key_sample = jax.random.split(rng, num=3)
  initial_guess = task.initial_guess(key_x0, batch=(n_samples, ))
  prior_samples = task.sample(key_x0, batch=(n_samples,))

  w = calibrate_kde(prior_samples, grid, log_p)

  samples = dict()
  divergence = dict()
  kl = dict()
  kde = dict()

  _, kl['initial'] = kde_kl(initial_guess, grid, log_p, w)
  kde['prior'], kl['prior'] = kde_kl(prior_samples, grid, log_p, w)
  divergence['initial'] = rf_js(initial_guess, prior_samples)

  for name, algo in zero_order_algorithms.items():
    @jax.jit
    def step(k, state):
      key_proposal, key_step = jax.random.split(k, num=2)
      proposal = algo.propose(key_proposal, state)
      log_p = task.log_p(proposal)
      return algo(key_step, proposal, log_p, state)

    state = algo.initial_state(initial_guess, task.log_p(initial_guess))
    for _ in range(n_steps):
      rng, key = jax.random.split(rng, num=2)
      state = step(key, state)

    samples[name] = algo.finalize(state)

    divergence[name] = rf_js(samples[name], prior_samples)
    kde[name], kl[name] = kde_kl(samples[name], grid, log_p, w)

  for name, algo in first_order_algorithms.items():
    @jax.jit
    def step(k, state):
      key_proposal, key_step = jax.random.split(k, num=2)
      proposal = algo.propose(key_proposal, state)
      log_p, grad_log_p = get_grad_log_p(proposal)
      return algo(key_step, proposal, log_p, grad_log_p, state)

    state = algo.initial_state(initial_guess, *get_grad_log_p(initial_guess))
    for _ in range(n_steps):
      rng, key = jax.random.split(rng, num=2)
      state = step(key, state)

    samples[name] = algo.finalize(state)

    divergence[name] = rf_js(samples[name], prior_samples)
    kde[name], kl[name] = kde_kl(samples[name], grid, log_p, w)

  for name, algo in foreign.items():
    rng, key = jax.random.split(rng, num=2)
    samples[name] = algo(key, task, initial_guess, n_steps)

    divergence[name] = rf_js(samples[name], prior_samples)
    kde[name], kl[name] = kde_kl(samples[name], grid, log_p, w)


  if prior_samples.shape[-1] == 2:
    fig = plt.figure(figsize=(9, 9 * (len(samples) + 1)))
    axes: plt.Axes = fig.subplots(nrows=len(samples) + 1, ncols=1)

    axes[0].contour(
      *xs, log_p.T,
      levels=jnp.linspace(jnp.min(log_p), jnp.max(log_p), num=21)
    )

    for name, sample in samples.items():
      axes[0].scatter(
        sample[:, 0], sample[:, 1],
        label=f'{name} ($\\mathrm{{JS}}$ = {divergence[name]:.2f}, $\\mathrm{{KL}}$ = {kl[name]:.2f})',
        s=5
      )
    axes[0].scatter(
      prior_samples[:, 0], prior_samples[:, 1],
      color='black', s=5,
      label=f'prior, $\\mathrm{{KL}}$ = {kl["prior"]:.2f}'
    )

    axes[0].scatter(
      initial_guess[:, 0], initial_guess[:, 1],
      alpha=0.25, s=5, color='black',
      label=f'initial, ($\\mathrm{{JS}}$ = {divergence["initial"]:.2f}, $\\mathrm{{KL}}$ = {kl["initial"]:.2f})',
    )

    axes[0].set_xlim(task.support()[:, 0])
    axes[0].set_ylim(task.support()[:, 1])
    axes[0].legend()

    for i, name in enumerate(samples):
      axes[i + 1].contour(
        *xs, log_p.T,
        levels=jnp.linspace(jnp.min(log_p), jnp.max(log_p), num=21)
      )
      axes[i + 1].scatter(
        samples[name][:, 0], samples[name][:, 1],
        label=f'{name} ($\\mathrm{{JS}}$ = {divergence[name]:.2f}, $\\mathrm{{KL}}$ = {kl[name]:.2f})',
        s=5
      )

      axes[i + 1].scatter(
        prior_samples[:, 0], prior_samples[:, 1],
        color='black', s=5,
        label=f'prior, $\\mathrm{{KL}}$ = {kl["prior"]:.2f}'
      )

      axes[i + 1].set_xlim(task.support()[:, 0])
      axes[i + 1].set_ylim(task.support()[:, 1])
      axes[i + 1].legend()

    fig.tight_layout()
    fig.savefig(os.path.join(plot_root, f'{task.name()}.png'))
    plt.close(fig)

    ### density
    fig = plt.figure(figsize=(9, 9 * len(kde)))
    axes = fig.subplots(nrows=len(kde) + 1, ncols=1)

    min_log_p, max_log_p = jnp.min(log_p), jnp.max(log_p)
    levels = jnp.linspace(min_log_p, max_log_p, num=21)
    axes[0].set_title('ground-truth')
    axes[0].contour(*xs, log_p.T, levels=levels)

    for i, name in enumerate(kde):
      axes[i + 1].set_title(name)
      axes[i + 1].contour(*xs, kde[name].T, levels=levels)
      axes[i + 1].contour(*xs, log_p.T, levels=levels, colors=['black'])
    fig.tight_layout()
    fig.savefig(os.path.join(plot_root, f'{task.name()}-kde.png'))
    plt.close(fig)

    fig = plt.figure(figsize=(10, 9 * len(kde)))
    axes = fig.subplots(nrows=len(kde) + 1, ncols=1)

    ### difference
    min_log_p, max_log_p = jnp.min(log_p), jnp.max(log_p)
    delta = max_log_p - min_log_p
    levels = jnp.linspace(-delta, delta, num=21)
    axes[0].set_title('target distribution')
    contour = axes[0].contourf(*xs, log_p.T, levels=jnp.linspace(min_log_p, max_log_p, num=21))
    fig.colorbar(contour, ax=axes[0])

    for i, name in enumerate(kde):
      axes[i + 1].set_title(name)
      contour = axes[i + 1].contourf(*xs, jnp.exp(log_p.T) * (log_p.T - kde[name].T), levels=levels)
      fig.colorbar(contour, ax=axes[i + 1])
    fig.tight_layout()
    fig.savefig(os.path.join(plot_root, f'{task.name()}-diff.png'))
    plt.close(fig)

    ### level plot
    center_ps = crayopt.utils.density.center_mean(jnp.exp(log_p))
    area = crayopt.utils.density.area(*xs)

    fig = plt.figure(figsize=(10, 9))
    axes = fig.subplots()
    axes.set_title(f'{task.name()}, total = {jnp.sum(area * center_ps):.2f}')
    mappable = axes.matshow(center_ps.T, origin='lower', vmin=0.0, vmax=jnp.max(center_ps))
    fig.colorbar(mappable, ax=axes)
    fig.tight_layout()
    fig.savefig(os.path.join(plot_root, f'{task.name()}-levels.png'))
    plt.close(fig)