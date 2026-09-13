"""Toroidal phase-shear route construction."""

import numpy as np

from toroidal_routing.manifold import ToroidalManifold


class ToroidalRouter:
    """Construct a nearest-phase route using prime-ratio interactions."""

    def __init__(self, n_scale: int = 2):
        self.manifold = ToroidalManifold(n_scale=n_scale)
        self.epsilon = self.manifold.epsilon

    def _generate_primes(self, count: int) -> np.ndarray:
        if count < 0:
            raise ValueError("count must be non-negative")

        primes: list[int] = []
        candidate = 2
        while len(primes) < count:
            if all(candidate % prime != 0 for prime in primes):
                primes.append(candidate)
            candidate += 1
        return np.asarray(primes, dtype=float)

    def optimize_route(self, coords: np.ndarray) -> tuple[list[int], float]:
        """Return a closed route and its phase-interaction cost."""
        coords = np.asarray(coords, dtype=float)
        if coords.ndim != 2 or coords.shape[1] != 2:
            raise ValueError("coords must have shape (N, 2)")
        if coords.shape[0] == 0:
            raise ValueError("coords must contain at least one point")

        node_count = coords.shape[0]
        primes = self._generate_primes(node_count)
        theta, _ = self.manifold.map_coordinates(coords)

        omega_ratio = primes[:, None] / primes[None, :]
        phase_matrix = np.abs(
            theta[:, None] * omega_ratio
            - theta[None, :] / omega_ratio
        )
        phase_matrix += self.epsilon * np.exp(-omega_ratio)
        np.fill_diagonal(phase_matrix, np.inf)

        current = 0
        unvisited = set(range(1, node_count))
        route = [current]
        while unvisited:
            next_node = min(unvisited, key=lambda node: phase_matrix[current, node])
            route.append(next_node)
            unvisited.remove(next_node)
            current = next_node

        route.append(route[0])
        total_cost = float(
            sum(
                phase_matrix[route[index], route[index + 1]]
                for index in range(len(route) - 1)
            )
        )
        return route, total_cost
