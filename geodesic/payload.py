"""
Payload and test particle models in Geodesic Foundry.
"""

import math
import uuid
from typing import List, Dict, Any, Optional


class Payload:
    """
    A test particle payload traveling along geodesics through curved spacetime.
    Can possess an intrinsic proper decay half-life (tau_half), demonstrating
    gravitational time dilation when transiting near high-mass nodes.
    """

    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        vx: float,
        vy: float,
        rest_mass: float = 1.0,
        tau_half: Optional[float] = None,  # Proper half-life in seconds (None = stable)
        color: str = "#38bdf8",
        payload_id: Optional[str] = None,
    ):
        self.payload_id = payload_id or f"p-{uuid.uuid4().hex[:6]}"
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.rest_mass = float(rest_mass)
        self.tau_half = tau_half  # None means infinite / stable
        self.color = color

        # Relativistic tracking
        self.proper_time: float = 0.0      # Accumulated proper time tau
        self.lab_time: float = 0.0         # Accumulated laboratory / coordinate time t
        self.last_dilation: float = 1.0    # Recent dtau / dt factor
        self.is_decayed: bool = False
        self.is_absorbed: bool = False     # Swallowed by event horizon
        self.is_captured: bool = False     # Successfully captured by destination target
        self.energy_boosted: bool = False  # Underwent Penrose acceleration

        # Historical trajectory trail for rendering
        self.trail: List[List[float]] = [[self.x, self.y]]
        self.max_trail: int = 50

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vy)

    @property
    def kinetic_energy(self) -> float:
        """Classical/relativistic proxy 0.5 * m * v^2 for display."""
        return 0.5 * self.rest_mass * (self.speed ** 2)

    @property
    def decay_ratio(self) -> float:
        """Normalized decay progress from 0.0 (fresh) to 1.0 (decayed)."""
        if self.tau_half is None or self.tau_half <= 0:
            return 0.0
        return min(1.0, self.proper_time / self.tau_half)

    def step_proper_time(self, dt: float, dilation_factor: float) -> None:
        """
        Advance lab time by dt and proper time by dt * dilation_factor.
        Triggers radioactive decay when proper_time exceeds tau_half.
        """
        if self.is_decayed or self.is_absorbed or self.is_captured:
            return

        self.lab_time += dt
        self.last_dilation = max(0.0, min(1.0, dilation_factor))
        dtau = dt * self.last_dilation
        self.proper_time += dtau

        if self.tau_half is not None and self.proper_time >= self.tau_half:
            self.is_decayed = True

    def record_pos(self) -> None:
        self.trail.append([self.x, self.y])
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_id": self.payload_id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "speed": self.speed,
            "rest_mass": self.rest_mass,
            "tau_half": self.tau_half,
            "proper_time": self.proper_time,
            "lab_time": self.lab_time,
            "decay_ratio": self.decay_ratio,
            "dilation": self.last_dilation,
            "is_decayed": self.is_decayed,
            "is_absorbed": self.is_absorbed,
            "is_captured": self.is_captured,
            "energy_boosted": self.energy_boosted,
            "color": self.color,
        }
