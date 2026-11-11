"""Check the sign and scale of a Gaussian vacuum response to a Hopf trial map.

This is an auxiliary effective-field calculation, not a quantum-gravity model.
"""

from __future__ import annotations

import json
from math import pi, sqrt

from scipy.integrate import quad


def trial_integrals(radius: float) -> dict[str, float]:
    def x_density(r: float) -> float:
        return 32 * radius**2 / (r * r + radius**2) ** 2

    def hopf_pair_density(r: float) -> float:
        return 256 * radius**4 / (r * r + radius**2) ** 4

    measure = lambda r: 4 * pi * r * r
    return {
        "X": quad(lambda r: measure(r) * x_density(r), 0, float("inf"), epsabs=1e-10)[0],
        "X_squared": quad(lambda r: measure(r) * x_density(r) ** 2, 0, float("inf"), epsabs=1e-10)[0],
        "H_pair_squared": quad(
            lambda r: measure(r) * hopf_pair_density(r), 0, float("inf"), epsabs=1e-10
        )[0],
    }


def effective_energy(radius: float, f: float, kappa: float, stiffness: float, coupling: float) -> float:
    integrals = trial_integrals(radius)
    return (
        f * f * integrals["X"] / 2
        + kappa * integrals["H_pair_squared"] / 2
        - coupling * coupling * integrals["X_squared"] / (2 * stiffness)
    )


def main() -> None:
    errors = {}
    for radius in (0.7, 1.0, 1.5):
        values = trial_integrals(radius)
        expected = {
            "X": 32 * pi**2 * radius,
            "X_squared": 128 * pi**2 / radius,
            "H_pair_squared": 32 * pi**2 / radius,
        }
        errors[str(radius)] = {key: values[key] - expected[key] for key in expected}
        assert max(abs(value) for value in errors[str(radius)].values()) < 1e-9

    f = kappa = stiffness = 1.0
    coupling = 0.2
    effective_kappa = kappa - 4 * coupling**2 / stiffness
    radius_star = sqrt(effective_kappa) / f
    trial_minimum = effective_energy(radius_star, f, kappa, stiffness, coupling)
    expected_minimum = 32 * pi**2 * f * sqrt(effective_kappa)
    assert abs(trial_minimum - expected_minimum) < 1e-9
    assert effective_kappa < kappa and radius_star < sqrt(kappa) / f
    first_stiffness = 1.5
    second_stiffness = 0.8
    field_ratio = -first_stiffness / (first_stiffness + second_stiffness)
    hopf_norm = trial_integrals(1.0)["H_pair_squared"]
    connection_minimum = (
        first_stiffness * (field_ratio + 1) ** 2 + second_stiffness * field_ratio**2
    ) * hopf_norm / 2
    connection_formula = first_stiffness * second_stiffness / (2 * (first_stiffness + second_stiffness)) * hopf_norm
    assert abs(connection_minimum - connection_formula) < 1e-10
    print(
        json.dumps(
            {
                "integral_residuals": errors,
                "parameters": {"f": f, "kappa": kappa, "K": stiffness, "lambda": coupling},
                "kappa_effective": effective_kappa,
                "radius_trial_minimum": radius_star,
                "energy_trial_minimum": trial_minimum,
                "formula_energy_trial_minimum": expected_minimum,
                "zero_response_energy_trial_minimum": 32 * pi**2 * f * sqrt(kappa),
                "two_stiffness_connection": {
                    "a": first_stiffness,
                    "b": second_stiffness,
                    "optimal_F_over_H": field_ratio,
                    "energy_at_radius_one": connection_minimum,
                    "energy_formula": connection_formula,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
