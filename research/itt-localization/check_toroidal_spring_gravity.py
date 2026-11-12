"""Weak-gravity perturbation of a two-scale toroidal-spring trial model.

The softened line ring is a diagnostic, not an electron or GR solution.
"""

from math import exp, log, pi, sqrt

from scipy.constants import G, c, electron_mass, hbar
from scipy.optimize import minimize
from scipy.special import ellipk


def field_energy(R, a, T0, V, K, D):
    return 2 * pi * R * (T0 + V * a * a + K / (a * a)) + pi * D / R


def gravity_energy(R, a, beta):
    """Softened Newtonian ring: beta = G M²/(2π), ellipk uses parameter m."""
    scale = sqrt(4 * R * R + a * a)
    return -2 * beta * ellipk(4 * R * R / (scale * scale)) / scale


def main():
    # Illustrative dimensionless coefficients; no fit to particle observables.
    T0, V, K, D, beta = 1.0, 1.0, 1.0, 400.0, 1.0
    a0 = (K / V) ** 0.25
    R0 = sqrt(D / (2 * (T0 + 2 * sqrt(K * V))))

    def total(log_sizes):
        a, R = map(exp, log_sizes)
        if a >= R:
            return float("inf")
        return field_energy(R, a, T0, V, K, D) + gravity_energy(R, a, beta)

    solution = minimize(total, [log(a0), log(R0)], method="BFGS")
    assert solution.success, solution.message
    a, R = map(exp, solution.x)
    exact_a, exact_R = (a - a0) / a0, (R - R0) / R0
    leading_a = -beta / (16 * pi * V * a0 * a0 * R0 * R0)
    leading_R = -beta * (log(8 * R0 / a0) - 1) / (2 * pi * D)
    assert exact_a < 0 and exact_R < 0
    assert abs(exact_a - leading_a) < 5e-6
    assert abs(exact_R - leading_R) < 5e-6

    compton = hbar / (electron_mass * c)
    compactness = G * electron_mass / (compton * c * c)
    aspect = 0.1  # a/R; only an illustration, not a measured electron core.
    L = log(8 / aspect)
    gravity_fraction = compactness * L / (2 * pi)
    radius_shift = -compactness * (L - 1) / (2 * pi)

    print(f"dimensionless a0={a0:.9f}, R0={R0:.9f}")
    print(f"exact shifts da/a={exact_a:.9e}, dR/R={exact_R:.9e}")
    print(f"leading shifts da/a={leading_a:.9e}, dR/R={leading_R:.9e}")
    print(f"electron benchmark compactness={compactness:.9e}")
    print(f"at a/R={aspect}: |Ug|/(m_e c²)≈{gravity_fraction:.9e}, "
          f"dR/R≈{radius_shift:.9e}")


if __name__ == "__main__":
    main()
