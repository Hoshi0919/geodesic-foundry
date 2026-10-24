"""
Singularity and gravitating node models in Geodesic Foundry.
"""

import math
from typing import Tuple, Dict, Any
from .spacetime import SpacetimeMetrics, G, C, C_SQ


class Singularity:
    """
    A localized mass concentration altering spacetime curvature.
    Can represent a Schwarzschild black hole (spin=0), Kerr black hole (spin!=0),
    or negative-mass exotic matter core (mass<0) acting as a repulsive cosmic lens.
    """

    def __init__(
        self,
        node_id: str,
        name: str,
        x: float,
        y: float,
        mass: float = 100.0,
        spin: float = 0.0,
        fixed: bool = True
    ):
        self.node_id = node_id
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.mass = float(mass)
        self.spin = max(-1.0, min(1.0, float(spin)))
        self.fixed = fixed
        self.absorbed_count: int = 0
        self.extracted_energy: float = 0.0

    @property
    def rs(self) -> float:
        """Event horizon radius (Schwarzschild radius)."""
        return SpacetimeMetrics.schwarzschild_radius(self.mass)

    @property
    def r_photon(self) -> float:
        """Photon sphere radius."""
        return SpacetimeMetrics.photon_sphere_radius(self.mass)

    @property
    def r_isco(self) -> float:
        """Innermost stable circular orbit radius."""
        return SpacetimeMetrics.isco_radius(self.mass, spin=self.spin)

    @property
    def r_ergo_equator(self) -> float:
        """Ergosphere boundary on the 2D orbital plane (theta = pi/2)."""
        return SpacetimeMetrics.ergosphere_radius(self.mass, self.spin, theta=math.pi / 2)

    def distance_to(self, px: float, py: float) -> float:
        dx = px - self.x
        dy = py - self.y
        return math.hypot(dx, dy)

    def is_inside_horizon(self, px: float, py: float) -> bool:
        if self.mass <= 0:
            return False
        return self.distance_to(px, py) <= self.rs

    def is_inside_ergosphere(self, px: float, py: float) -> bool:
        """Returns True if within static limit but outside event horizon."""
        if self.mass <= 0 or abs(self.spin) < 1e-4:
            return False
        r = self.distance_to(px, py)
        # In 2D plane with spin axis perpendicular to the plane (z-axis),
        # the equator theta = pi/2 has r_ergo = 2 * GM / c^2 (same as rs of non-spinning)
        # while the spinning event horizon is r_+ = M + sqrt(M^2 - a^2).
        # Thus the ergoregion exists between r_+ and 2M.
        m_geom = G * self.mass / C_SQ
        r_plus = m_geom * (1.0 + math.sqrt(max(0.0, 1.0 - self.spin**2)))
        r_ergo = 2.0 * m_geom
        return r_plus < r <= r_ergo

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "mass": self.mass,
            "spin": self.spin,
            "rs": self.rs,
            "r_isco": self.r_isco,
            "absorbed_count": self.absorbed_count,
            "extracted_energy": self.extracted_energy,
        }
