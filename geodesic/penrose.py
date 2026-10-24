"""
Penrose process and ergosphere superradiant fission mechanism.
"""

import math
from typing import Optional, Tuple
from .payload import Payload
from .singularity import Singularity


class PenroseReactor:
    """
    Manages tidal fission and energy extraction inside a Kerr black hole's ergosphere.
    """

    @staticmethod
    def attempt_fission(
        payload: Payload,
        kerr: Singularity,
        fission_efficiency: float = 0.35
    ) -> Optional[Tuple[Payload, Payload]]:
        """
        If the payload is inside the ergosphere and hasn't yet split:
        Split into:
        1. Negative-energy fragment falling into the horizon (absorbed).
        2. Superradiant accelerated fragment escaping to infinity with E > E_in.
        """
        if payload.energy_boosted or payload.is_absorbed or payload.is_decayed:
            return None

        if not kerr.is_inside_ergosphere(payload.x, payload.y):
            return None

        # Calculate unit tangent and normal vectors relative to Kerr center
        dx = payload.x - kerr.x
        dy = payload.y - kerr.y
        dist = math.hypot(dx, dy)
        if dist < 1e-4:
            return None

        # Inward radial unit vector
        rx = -dx / dist
        ry = -dy / dist

        # Tangential unit vector in spin direction (counter-clockwise if spin > 0)
        spin_sign = 1.0 if kerr.spin >= 0 else -1.0
        tx = -spin_sign * (dy / dist)
        ty = spin_sign * (dx / dist)

        # Original kinetic energy
        e_orig = payload.kinetic_energy
        # Extracted energy from Kerr rotational reservoir
        extracted = e_orig * fission_efficiency * abs(kerr.spin)
        kerr.extracted_energy += extracted

        # Retrograde fragment (inward plunge into horizon)
        retro_name = f"{payload.name}-Inf"
        retro = Payload(
            name=retro_name,
            x=payload.x,
            y=payload.y,
            vx=rx * 25.0 - tx * 15.0,
            vy=ry * 25.0 - ty * 15.0,
            rest_mass=payload.rest_mass * 0.4,
            tau_half=payload.tau_half,
            color="#ef4444",
        )
        retro.is_absorbed = True  # Destined for horizon

        # Superradiant escaped fragment
        esc_boost = math.sqrt(1.0 + (extracted / max(1.0, e_orig)))
        esc_name = f"{payload.name}-Hyper"
        esc = Payload(
            name=esc_name,
            x=payload.x,
            y=payload.y,
            vx=payload.vx * esc_boost + tx * 20.0,
            vy=payload.vy * esc_boost + ty * 20.0,
            rest_mass=payload.rest_mass * 0.6,
            tau_half=payload.tau_half * 1.5 if payload.tau_half else None,
            color="#f59e0b",
        )
        esc.energy_boosted = True

        # Mark original payload as processed
        payload.is_absorbed = True
        kerr.absorbed_count += 1

        return retro, esc
