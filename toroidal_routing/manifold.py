"""Toroidal coordinate mapping primitives."""

import numpy as np


class ToroidalManifold:
    """Map two-dimensional coordinates onto major and minor torus phases."""

    def __init__(self, n_scale: int = 2):
        if not isinstance(n_scale, (int, np.integer)) or n_scale < 0:
            raise ValueError("n_scale must be a non-negative integer")

        self.pi = np.pi
        self.fold_unit = 6.0 * (self.pi**5)
        self.epsilon = self.fold_unit ** (-6 * n_scale)

    def map_coordinates(self, coords: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return major (theta) and minor (phi) phases for an ``(N, 2)`` array."""
        coords = np.asarray(coords, dtype=float)
        if coords.ndim != 2 or coords.shape[1] != 2:
            raise ValueError("coords must have shape (N, 2)")
        if coords.shape[0] == 0:
            raise ValueError("coords must contain at least one point")
        if not np.all(np.isfinite(coords)):
            raise ValueError("coords must contain only finite values")

        x, y = coords[:, 0], coords[:, 1]
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)

        theta = (x - x_min) / (x_max - x_min + self.epsilon) * 2 * self.pi
        phi = (y - y_min) / (y_max - y_min + self.epsilon) * 2 * self.pi
        return theta, phi
