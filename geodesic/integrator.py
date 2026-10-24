"""
Geodesic numerical integrator with post-Newtonian relativistic corrections.
"""

import math
from typing import List
from .spacetime import SpacetimeMetrics, G, C, C_SQ
from .singularity import Singularity
from .payload import Payload


class GeodesicIntegrator:
    """
    Numerically marches test particle payloads through curved multi-body spacetime.
    Implements 1PN relativistic corrections, Kerr frame-dragging, and proper time dilation.
    """

    def __init__(self, step_dt: float = 0.016):
        self.dt = step_dt

    def compute_acceleration(
        self,
        px: float,
        py: float,
        vx: float,
        vy: float,
        singularities: List[Singularity]
    ) -> tuple[float, float, float]:
        """
        Returns (ax, ay, combined_dilation_factor).
        """
        ax = 0.0
        ay = 0.0
        sum_potential = 0.0
        v_sq = vx * vx + vy * vy

        for s in singularities:
            dx = s.x - px
            dy = s.y - py
            r_sq = dx * dx + dy * dy
            r = math.sqrt(r_sq)

            if r < 1.0:
                continue

            # Newtonian acceleration magnitude
            # Note: dx, dy point towards singularity s
            a_mag = (G * s.mass) / (r_sq + 4.0)

            # Direction unit vector towards singularity
            ux = dx / r
            uy = dy / r

            # Post-Newtonian (1PN) relativistic correction factor:
            # - Enhances gravity for fast-moving particles (causes light bending = 2x Newtonian)
            # - Incorporates Schwarzschild perihelion precession term
            v_dot_u = (vx * ux + vy * uy)
            relativistic_factor = 1.0 + (3.0 * v_sq / C_SQ) - (4.0 * G * s.mass / (C_SQ * r))
            
            # Radial acceleration
            ax += a_mag * ux * relativistic_factor
            ay += a_mag * uy * relativistic_factor

            # Velocity-dependent velocity-damping/beaming term from GR
            vel_term = (4.0 * a_mag * v_dot_u / C_SQ)
            ax -= vel_term * vx
            ay -= vel_term * vy

            # Kerr frame-dragging (Lense-Thirring effect) for spinning singularities
            if abs(s.spin) > 1e-4 and s.mass > 0:
                # Frame-dragging azimuthal acceleration ~ 2 * G * J / (c^2 * r^3)
                # Tangential direction in spinning frame
                tx = -uy * (1.0 if s.spin > 0 else -1.0)
                ty = ux * (1.0 if s.spin > 0 else -1.0)
                drag_mag = (2.0 * G * s.mass * abs(s.spin) * C) / (r**3 + 10.0)
                ax += drag_mag * tx
                ay += drag_mag * ty

            # Accumulate gravitational potential for time dilation
            if s.mass > 0:
                sum_potential += (2.0 * G * s.mass) / (r * C_SQ)

        # Compute proper time dilation factor dtau / dt
        metric_term = 1.0 - sum_potential - (v_sq / C_SQ)
        dilation = math.sqrt(max(0.001, metric_term))

        return ax, ay, dilation

    def step(
        self,
        payload: Payload,
        singularities: List[Singularity],
        substeps: int = 2
    ) -> None:
        """
        Symplectic velocity-Verlet numerical integration step.
        """
        if payload.is_absorbed or payload.is_captured or payload.is_decayed:
            return

        sub_dt = self.dt / substeps
        for _ in range(substeps):
            # Horizon check first
            for s in singularities:
                if s.mass > 0 and s.is_inside_horizon(payload.x, payload.y):
                    payload.is_absorbed = True
                    s.absorbed_count += 1
                    return

            ax1, ay1, dilation = self.compute_acceleration(
                payload.x, payload.y, payload.vx, payload.vy, singularities
            )

            # Half-step velocity
            vx_half = payload.vx + 0.5 * ax1 * sub_dt
            vy_half = payload.vy + 0.5 * ay1 * sub_dt

            # Full-step position
            payload.x += vx_half * sub_dt
            payload.y += vy_half * sub_dt

            # Acceleration at new position
            ax2, ay2, _ = self.compute_acceleration(
                payload.x, payload.y, vx_half, vy_half, singularities
            )

            # Full-step velocity
            payload.vx = vx_half + 0.5 * ax2 * sub_dt
            payload.vy = vy_half + 0.5 * ay2 * sub_dt

            # Relativistic time advancement
            payload.step_proper_time(sub_dt, dilation)

        payload.record_pos()
