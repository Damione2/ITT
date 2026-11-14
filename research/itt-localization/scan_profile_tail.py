"""Scan smooth cross-section tails in a thin-tube Hopf trial family."""

from math import atan, exp, log, pi, sin, sqrt

from scipy.integrate import quad
from scipy.optimize import minimize_scalar


def profile_integrals(p: float) -> tuple[float, float, float, float]:
    """Return I2_transverse, I_phase, I4_transverse, I4_mixed."""

    def integrands(log_x: float) -> tuple[float, float, float, float]:
        x = exp(log_x)
        log_q = -log_x - 0.5 * (p - 1.0) * log(1.0 + x * x)
        q = exp(log_q)
        F = 2.0 * atan(q)
        sin_F = sin(F)
        Fprime = sin_F * (-1.0 / x - (p - 1.0) * x / (1.0 + x * x))
        # d²x = x dx dθ, and dx = x d(log x).
        return (
            2 * pi * x * x * (Fprime * Fprime + sin_F * sin_F / (x * x)),
            2 * pi * x * x * sin_F * sin_F,
            2 * pi * Fprime * Fprime * sin_F * sin_F,
            2 * pi * x * x * Fprime * Fprime * sin_F * sin_F,
        )

    return tuple(
        quad(lambda t, j=j: integrands(t)[j], -40.0, 40.0,
             epsabs=1e-8, epsrel=1e-8, limit=300)[0]
        for j in range(4)
    )


def minimized_values(p: float, f2: float = 1.0, kappa: float = 1.0,
                     winding: int = 1) -> tuple[float, float, float, float]:
    i2, iphase, i4, imix = profile_integrals(p)
    A, B, C, D = pi * f2 * i2, pi * kappa * i4, pi * f2 * iphase, pi * kappa * imix
    R = abs(winding) * sqrt(D / A)
    a = sqrt(R * sqrt(B / C))
    energy = 2 * abs(winding) * (sqrt(A * D) + sqrt(B * C))
    return energy, a / R, R, a


def main() -> None:
    print("p       E_min       a/R")
    for p in (1.1, 1.2, 2.0, 3.0, 5.0, 7.0):
        energy, aspect, _, _ = minimized_values(p)
        print(f"{p:3.1f}  {energy:10.4f}  {aspect:8.4f}")
    optimum = minimize_scalar(lambda p: minimized_values(p)[0],
                              bounds=(1.001, 8.0), method="bounded",
                              options={"xatol": 1e-5})
    energy, aspect, R, a = minimized_values(optimum.x)
    print(f"minimum p={optimum.x:.5f}, E={energy:.5f}, "
          f"a/R={aspect:.5f}, R={R:.5f}, a={a:.5f}")


if __name__ == "__main__":
    main()
