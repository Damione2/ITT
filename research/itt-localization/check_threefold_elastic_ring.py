"""Variational checks for a framed ring with three twists and three lobes.

The rod is an analogy, not a model derived from ITT.  The planar three-lobe
check fixes the total length before comparing bending energies.
"""

from __future__ import annotations

import json
from math import pi, sqrt

import numpy as np
from scipy.integrate import quad


def radial_curve_data(angle: float, amplitude: float, mode: int = 3) -> tuple[float, float]:
    radius = 1 + amplitude * np.cos(mode * angle)
    first = -amplitude * mode * np.sin(mode * angle)
    second = -amplitude * mode * mode * np.cos(mode * angle)
    ds_dangle = sqrt(radius * radius + first * first)
    curvature = (radius * radius + 2 * first * first - radius * second) / ds_dangle**3
    return ds_dangle, curvature * curvature * ds_dangle


def fixed_length_bending_ratio(amplitude: float, mode: int = 3) -> float:
    length = quad(lambda t: radial_curve_data(t, amplitude, mode)[0], 0, 2 * pi, epsabs=1e-12)[0]
    bending_integral = quad(
        lambda t: radial_curve_data(t, amplitude, mode)[1], 0, 2 * pi, epsabs=1e-12
    )[0]
    # Scale the deformed curve so its length is 2*pi; under scale s, integral kappa^2 ds -> integral/s.
    scale = 2 * pi / length
    return bending_integral / scale / (2 * pi)


def minimum_radius_and_energy(tension: float, bending: float, twisting: float, turns: int) -> tuple[float, float]:
    radius = sqrt((bending + twisting * turns * turns) / (2 * tension))
    energy = 2 * pi * tension * radius + pi * (bending + twisting * turns * turns) / radius
    return radius, energy


def main() -> None:
    zero_radius, zero_energy = minimum_radius_and_energy(1, 1, 1, 0)
    three_radius, three_energy = minimum_radius_and_energy(1, 1, 1, 3)
    coefficients = {
        str(amplitude): (fixed_length_bending_ratio(amplitude) - 1) / amplitude**2
        for amplitude in (0.02, 0.01, 0.005, 0.0025)
    }
    assert abs(zero_radius - 1 / sqrt(2)) < 1e-12
    assert abs(three_radius - sqrt(5)) < 1e-12
    assert abs(three_energy / zero_energy - sqrt(10)) < 1e-12
    assert abs(coefficients[str(0.0025)] - 32) < 1e-3
    print(
        json.dumps(
            {
                "units": "T=B=C=1",
                "untwisted_optimal_radius": zero_radius,
                "three_twists_optimal_radius": three_radius,
                "three_to_zero_minimum_energy_ratio": three_energy / zero_energy,
                "three_lobe_quadratic_bending_coefficient": coefficients,
                "coefficient_asymptote": 32,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
