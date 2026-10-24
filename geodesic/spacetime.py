"""
Spacetime metrics, constants, and relativistic equations.
"""

import math
from typing import Tuple

# Dimensionless physical constants tuned for stable macroscopic interactive scales
G: float = 1000.0   # Gravitational constant
C: float = 100.0    # Speed of light in vacuum (c)
C_SQ: float = C * C


class SpacetimeMetrics:
    """Analytical calculations for Schwarzschild and Kerr metrics."""

    @staticmethod
    def schwarzschild_radius(mass: float) -> float:
        """rs = 2 * G * M / c^2"""
        if mass <= 0:
            return 0.0
        return 2.0 * G * mass / C_SQ

    @staticmethod
    def photon_sphere_radius(mass: float) -> float:
        """r_ph = 3 * G * M / c^2 = 1.5 * rs"""
        if mass <= 0:
            return 0.0
        return 3.0 * G * mass / C_SQ

    @staticmethod
    def isco_radius(mass: float, prograde: bool = True, spin: float = 0.0) -> float:
        """
        Innermost Stable Circular Orbit (ISCO).
        For Schwarzschild (spin=0): r_isco = 6 * G * M / c^2 = 3 * rs.
        For Kerr prograde/retrograde, incorporates spin parameter a in [-1, 1].
        """
        if mass <= 0:
            return 0.0
        base = G * mass / C_SQ  # M in geometric units
        if abs(spin) < 1e-5:
            return 6.0 * base

        a = max(-1.0, min(1.0, spin if prograde else -spin))
        z1 = 1.0 + (1.0 - a**2)**(1/3) * ((1.0 + a)**(1/3) + (1.0 - a)**(1/3))
        z2 = math.sqrt(3.0 * a**2 + z1**2)
        r_isco = base * (3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2)))
        return float(r_isco)

    @staticmethod
    def ergosphere_radius(mass: float, spin: float, theta: float = math.pi / 2) -> float:
        """
        Kerr ergosphere outer boundary (static limit):
        r_E(theta) = M + sqrt(M^2 - a^2 * cos^2(theta)) in geometric units G=c=1.
        In scaled units: (G*M / c^2) * (1 + sqrt(1 - (spin * cos(theta))^2))
        """
        if mass <= 0:
            return 0.0
        m_geom = G * mass / C_SQ
        spin_clamped = max(-1.0, min(1.0, spin))
        cos_th = math.cos(theta)
        disc = 1.0 - (spin_clamped * cos_th)**2
        return m_geom * (1.0 + math.sqrt(max(0.0, disc)))

    @staticmethod
    def time_dilation_factor(mass: float, r: float, velocity: float) -> float:
        """
        dtau / dt = sqrt(1 - 2GM/(r*c^2) - v^2/c^2)
        Returns proper time increment per coordinate time unit.
        Returns 0.0 if inside event horizon or exceeding light speed.
        """
        if r <= 0:
            return 0.0
        grav_pot = 2.0 * G * mass / (r * C_SQ)
        kin_term = (velocity * velocity) / C_SQ
        metric_term = 1.0 - grav_pot - kin_term
        if metric_term <= 0.0:
            return 0.0
        return math.sqrt(metric_term)

    @staticmethod
    def gravitational_deflection(mass: float, impact_param: float, velocity: float) -> float:
        """
        Calculates asymptotic deflection angle delta_phi.
        Ultra-relativistic limit (v -> c): 4GM / (c^2 * b)
        Non-relativistic limit: 2GM / (v^2 * b)
        Generalized interpolation: (2 + 2*(v/c)^2) * GM / (v^2 * b)
        """
        if impact_param <= 1e-4 or velocity <= 1e-4:
            return 0.0
        beta = min(0.9999, velocity / C)
        geom = G * mass / (impact_param * (velocity**2))
        return (2.0 + 2.0 * (beta**2)) * geom
