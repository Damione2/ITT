"""Check a unit-winding SU(2) map whose Hopf projection has flat gauge energy.

This is a mathematical diagnostic for the ITT SU(2) -> S^2 proposal, not an
electron solution.  The exact flatness follows from the Maurer--Cartan identity;
finite differences below independently check the chosen signs and conventions.
"""

from __future__ import annotations

import json
from math import pi

import numpy as np
from scipy.integrate import quad


IDENTITY = np.eye(2, dtype=complex)
PAULI = np.array(
    [
        [[0, 1], [1, 0]],
        [[0, -1j], [1j, 0]],
        [[1, 0], [0, -1]],
    ],
    dtype=complex,
)


def hedgehog(x: np.ndarray, radius: float) -> np.ndarray:
    """U=(r^2-R^2+2iR x.sigma)/(r^2+R^2), degree +1 by convention."""
    r2 = float(x @ x)
    return ((r2 - radius**2) * IDENTITY + 2j * radius * np.einsum("i,ijk->jk", x, PAULI)) / (
        r2 + radius**2
    )


def derivative_hedgehog(x: np.ndarray, radius: float, axis: int) -> np.ndarray:
    r2 = float(x @ x)
    denominator = r2 + radius**2
    da = 4 * radius**2 * x[axis] / denominator**2
    db = 2 * radius * np.eye(3)[axis] / denominator - 4 * radius * x[axis] * x / denominator**2
    return da * IDENTITY + 1j * np.einsum("i,ijk->jk", db, PAULI)


def connection(x: np.ndarray, radius: float, coupling: float, axis: int) -> np.ndarray:
    u = hedgehog(x, radius)
    return -derivative_hedgehog(x, radius, axis) @ u.conj().T / coupling


def color_direction(x: np.ndarray, radius: float) -> np.ndarray:
    u = hedgehog(x, radius)
    return u @ PAULI[2] @ u.conj().T


def components(matrix: np.ndarray) -> np.ndarray:
    return np.array([float(np.real(np.trace(sigma @ matrix)) / 2) for sigma in PAULI])


def ordinary_direction_gradient(x: np.ndarray, radius: float) -> np.ndarray:
    u = hedgehog(x, radius)
    return np.array(
        [
            components(
                derivative_hedgehog(x, radius, axis) @ PAULI[2] @ u.conj().T
                + u @ PAULI[2] @ derivative_hedgehog(x, radius, axis).conj().T
            )
            for axis in range(3)
        ]
    )


def covariant_direction_derivative(x: np.ndarray, radius: float, coupling: float, axis: int) -> np.ndarray:
    u = hedgehog(x, radius)
    du = derivative_hedgehog(x, radius, axis)
    n = color_direction(x, radius)
    ordinary = du @ PAULI[2] @ u.conj().T + u @ PAULI[2] @ du.conj().T
    gauge = connection(x, radius, coupling, axis)
    return ordinary + coupling * (gauge @ n - n @ gauge)


def curvature_finite_difference(
    x: np.ndarray, radius: float, coupling: float, i: int, j: int, step: float
) -> np.ndarray:
    ei = np.eye(3)[i] * step
    ej = np.eye(3)[j] * step
    derivative_i_aj = (connection(x + ei, radius, coupling, j) - connection(x - ei, radius, coupling, j)) / (
        2 * step
    )
    derivative_j_ai = (connection(x + ej, radius, coupling, i) - connection(x - ej, radius, coupling, i)) / (
        2 * step
    )
    ai = connection(x, radius, coupling, i)
    aj = connection(x, radius, coupling, j)
    return derivative_i_aj - derivative_j_ai + coupling * (ai @ aj - aj @ ai)


def unit_winding(radius: float) -> tuple[float, float]:
    # F(r)=2 atan(R/r); sin F=2Rr/(r^2+R^2), F'=-2R/(r^2+R^2).
    def density(r: float) -> float:
        denominator = r * r + radius * radius
        sin_f = 2 * radius * r / denominator
        f_prime = -2 * radius / denominator
        return -2 * sin_f * sin_f * f_prime / pi

    return quad(density, 0, np.inf, epsabs=2e-12, epsrel=2e-12)


def main() -> None:
    x = np.array([0.23, -0.41, 0.52])
    radius = 1.3
    coupling = 0.7
    windings = {str(r): unit_winding(r)[0] for r in (0.7, 1.3, 2.4)}
    u = hedgehog(x, radius)
    n = color_direction(x, radius)
    n_vector = components(n)
    gradient = ordinary_direction_gradient(x, radius)
    gradient_squared = float(np.sum(gradient**2))
    hopf_curvature_squared = sum(
        float(np.dot(n_vector, np.cross(gradient[i], gradient[j]))) ** 2
        for i, j in ((0, 1), (0, 2), (1, 2))
    )
    denominator = float(x @ x) + radius**2
    predicted_gradient_squared = 32 * radius**2 / denominator**2
    predicted_hopf_curvature_squared = 256 * radius**4 / denominator**4
    integrated_gradient_squared = quad(
        lambda r: 4 * pi * r * r * 32 * radius**2 / (r * r + radius**2) ** 2,
        0,
        np.inf,
        epsabs=1e-10,
    )[0]
    integrated_hopf_curvature_squared = quad(
        lambda r: 4 * pi * r * r * 256 * radius**4 / (r * r + radius**2) ** 4,
        0,
        np.inf,
        epsabs=1e-10,
    )[0]
    unitarity = float(np.linalg.norm(u @ u.conj().T - IDENTITY))
    n_squared = float(np.linalg.norm(n @ n - IDENTITY))
    dn = max(
        float(np.linalg.norm(covariant_direction_derivative(x, radius, coupling, axis)))
        for axis in range(3)
    )
    curvature = {
        str(step): max(
            float(np.linalg.norm(curvature_finite_difference(x, radius, coupling, i, j, step)))
            for i, j in ((0, 1), (0, 2), (1, 2))
        )
        for step in (1e-3, 5e-4, 2.5e-4)
    }
    assert max(abs(w - 1) for w in windings.values()) < 1e-10
    assert unitarity < 1e-12 and n_squared < 1e-12 and dn < 1e-12
    assert abs(gradient_squared - predicted_gradient_squared) < 1e-12
    assert abs(hopf_curvature_squared - predicted_hopf_curvature_squared) < 1e-12
    assert abs(integrated_gradient_squared - 32 * pi**2 * radius) < 1e-9
    assert abs(integrated_hopf_curvature_squared - 32 * pi**2 / radius) < 1e-9
    assert curvature[str(2.5e-4)] < 1e-6
    assert curvature[str(2.5e-4)] < curvature[str(1e-3)]
    print(
        json.dumps(
            {
                "winding_equals_hopf_charge": windings,
                "unitarity_residual": unitarity,
                "unit_direction_residual": n_squared,
                "covariant_direction_derivative_residual": dn,
                "spatial_gradient_squared": gradient_squared,
                "spatial_gradient_squared_formula": predicted_gradient_squared,
                "hopf_curvature_squared": hopf_curvature_squared,
                "hopf_curvature_squared_formula": predicted_hopf_curvature_squared,
                "integrated_gradient_squared": integrated_gradient_squared,
                "integrated_gradient_squared_formula": 32 * pi**2 * radius,
                "integrated_hopf_curvature_squared": integrated_hopf_curvature_squared,
                "integrated_hopf_curvature_squared_formula": 32 * pi**2 / radius,
                "trial_energy_f_equals_kappa_equals_one_at_R_one": 32 * pi**2,
                "flat_curvature_finite_difference_residual": curvature,
                "exact_curvature": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
