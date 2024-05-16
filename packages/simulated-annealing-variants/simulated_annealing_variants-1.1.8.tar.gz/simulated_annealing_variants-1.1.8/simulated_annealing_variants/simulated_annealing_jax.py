import numpy as np
import jax.numpy as jnp
import jax.lax as lax
from jax import random
from jax import jit

from typing import Tuple

from .temperature import (
    deterministic_temperature,
    sample_temperature,
    iterative_temperature,
    TEMPERATURE_SAMPLING_MODE,
)


def simulated_annealing(
    Q: np.ndarray,
    num_t_values: int | None = None,
    temperature_sampling_mode: TEMPERATURE_SAMPLING_MODE = TEMPERATURE_SAMPLING_MODE.deterministic,
    seed: int | None = None,
) -> Tuple[np.ndarray, float]:
    """Simulated annealing with a computational complexity of O(n * t),
    where t is the number of timesteps.
    This is achieved by computing only the updated values which are at most
    n per update step.

    Args:
        Q (np.ndarray): The QUBO matrix.
        num_t_values (int | None, optional): Number of update steps. Defaults to the size of the QUBO squared.
        temperature_sampling_mode (TEMPERATURE_SAMPLING_TYPE): The way of sampling the temperature start and end values. Defaults to deterministic.
        seed (int | None, optional): Random seed. Defaults to None.


    Returns:
        Tuple[np.ndarray, float]: The best solutions and its energy.
    """
    if seed is None:
        import time

        key = random.key(int(time.time()) * 10_000_000)
    else:
        key = random.key(seed)

    if num_t_values is None:
        num_t_values = n**2

    # Create the temperature parameters
    if temperature_sampling_mode == TEMPERATURE_SAMPLING_MODE.deterministic:
        t_0, t_end = deterministic_temperature(Q)
    elif temperature_sampling_mode == TEMPERATURE_SAMPLING_MODE.sample:
        t_0, t_end = sample_temperature(Q)
    elif temperature_sampling_mode == TEMPERATURE_SAMPLING_MODE.iterative:
        t_0, t_end = iterative_temperature(Q)
    epsilon = np.exp(np.log(t_end / t_0) / num_t_values)

    # Create helper matrix
    n = Q.shape[0]
    Q = jnp.array(Q)
    Q_outer = Q + Q.T
    Q_outer = jnp.fill_diagonal(Q_outer, 0, inplace=False)
    Q_outer = Q_outer.at[jnp.diag_indices_from(Q)].set(0)

    # Random initial
    x = random.randint(key, shape=(n,), minval=0, maxval=2)
    f_x = x.T @ Q @ x

    state = (key, Q, Q_outer, x, f_x, t_0, epsilon)
    lax.fori_loop(0, num_t_values, inner_computation, state)

    return x, f_x


def inner_computation(i, state):
    (key, Q, Q_outer, x, f_x, t_i, epsilon) = state

    n = Q.shape[0]

    # Random flip in x
    key, subkey = random.split(key)
    idx = random.randint(subkey, shape=(1,), minval=0, maxval=n)[0]

    # Compute the difference between the flip and the previous energy
    sign = -(2 * x[idx] - 1)
    f_difference = sign * (jnp.dot(x, Q_outer[idx]) + Q[idx, idx])
    f_y = f_x + f_difference

    # Accept the new one if better (t is inverted beforehand)
    key, subkey = random.split(key)
    U = random.uniform(subkey, shape=(1,), minval=0.0, maxval=1.0)[0]
    t_i = t_i * epsilon
    beta = 1.0 / t_i

    (x, f_x) = lax.cond(
        (f_y <= f_x or (jnp.exp(-(f_y - f_x) * beta) > U)),
        accept,
        reject,
        (x, f_x, f_y),
    )

    def accept(op):
        (x, _, f_y) = op
        x.at[idx].set(1 - x[idx])
        return (x, f_y)

    def reject(op):
        (x, f_x, _) = op
        return (x, f_x)

    return (key, Q, Q_outer, x, f_x, t_i, epsilon)


if __name__ == "__main__":
    import numpy as np

    Q = np.triu(np.random.uniform(-10, 10, (64, 64)))
    x, f_x = simulated_annealing(Q, 10_000)
    print(x, f_x)
