"""
Foundry simulation engine: Emitters, Collectors, and Relativistic Assembly Lines.
"""

import math
from typing import List, Dict, Any, Optional
from .singularity import Singularity
from .payload import Payload
from .integrator import GeodesicIntegrator
from .penrose import PenroseReactor


class Emitter:
    """Spacetime payload injector launching particles into geodesics."""

    def __init__(
        self,
        emitter_id: str,
        name: str,
        x: float,
        y: float,
        launch_vx: float,
        launch_vy: float,
        interval_ticks: int = 40,
        payload_name: str = "Isotope-88",
        rest_mass: float = 1.0,
        tau_half: Optional[float] = None,
        color: str = "#38bdf8",
    ):
        self.emitter_id = emitter_id
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.launch_vx = float(launch_vx)
        self.launch_vy = float(launch_vy)
        self.interval_ticks = interval_ticks
        self.payload_name = payload_name
        self.rest_mass = rest_mass
        self.tau_half = tau_half
        self.color = color

        self.timer: int = 0
        self.total_emitted: int = 0

    def tick(self) -> Optional[Payload]:
        self.timer += 1
        if self.timer >= self.interval_ticks:
            self.timer = 0
            self.total_emitted += 1
            return Payload(
                name=f"{self.payload_name}#{self.total_emitted}",
                x=self.x,
                y=self.y,
                vx=self.launch_vx,
                vy=self.launch_vy,
                rest_mass=self.rest_mass,
                tau_half=self.tau_half,
                color=self.color,
            )
        return None


class Collector:
    """Orbital target/funnel collecting surviving payloads of target specification."""

    def __init__(
        self,
        collector_id: str,
        name: str,
        x: float,
        y: float,
        radius: float = 24.0,
        required_min_energy: float = 0.0,
        reject_decayed: bool = True,
        color: str = "#10b981",
    ):
        self.collector_id = collector_id
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.radius = float(radius)
        self.required_min_energy = required_min_energy
        self.reject_decayed = reject_decayed
        self.color = color

        self.collected_count: int = 0
        self.rejected_count: int = 0

    def check_capture(self, payload: Payload) -> bool:
        if payload.is_absorbed or payload.is_captured:
            return False

        dist = math.hypot(payload.x - self.x, payload.y - self.y)
        if dist <= self.radius:
            if self.reject_decayed and payload.is_decayed:
                self.rejected_count += 1
                payload.is_captured = True  # consumed as waste
                return False

            if payload.kinetic_energy >= self.required_min_energy:
                self.collected_count += 1
                payload.is_captured = True
                return True
            else:
                self.rejected_count += 1
                payload.is_captured = True
                return False
        return False


class FoundryEngine:
    """The central spacetime logistics coordinator."""

    def __init__(self, width: float = 800.0, height: float = 600.0):
        self.width = width
        self.height = height
        self.singularities: List[Singularity] = []
        self.emitters: List[Emitter] = []
        self.collectors: List[Collector] = []
        self.payloads: List[Payload] = []
        self.integrator = GeodesicIntegrator(step_dt=0.03)

        self.tick_count: int = 0
        self.penrose_events: int = 0
        self.total_swallowed: int = 0

    def clear(self) -> None:
        self.singularities.clear()
        self.emitters.clear()
        self.collectors.clear()
        self.payloads.clear()
        self.tick_count = 0
        self.penrose_events = 0
        self.total_swallowed = 0

    def step(self) -> None:
        self.tick_count += 1

        # 1. Emitters spawn new payloads
        for emitter in self.emitters:
            p = emitter.tick()
            if p:
                self.payloads.append(p)

        # 2. Physics step along geodesics
        new_payloads: List[Payload] = []
        for p in self.payloads:
            if p.is_absorbed or p.is_captured:
                continue

            # Penrose fission check if near spinning Kerr singularity
            split_happened = False
            for s in self.singularities:
                if abs(s.spin) > 1e-4 and s.is_inside_ergosphere(p.x, p.y):
                    split_res = PenroseReactor.attempt_fission(p, s)
                    if split_res:
                        retro, esc = split_res
                        new_payloads.append(retro)
                        new_payloads.append(esc)
                        self.penrose_events += 1
                        split_happened = True
                        break

            if split_happened:
                continue

            # Numerical integration step
            self.integrator.step(p, self.singularities)

            # Check collectors
            for c in self.collectors:
                c.check_capture(p)

        self.payloads.extend(new_payloads)

        # 3. Cleanup out-of-bounds or swallowed payloads
        surviving: List[Payload] = []
        for p in self.payloads:
            if p.is_absorbed:
                self.total_swallowed += 1
                continue
            if p.is_captured:
                continue
            # Boundary culling (padded by 150px)
            if -150 <= p.x <= self.width + 150 and -150 <= p.y <= self.height + 150:
                surviving.append(p)
        self.payloads = surviving

    def load_scenario(self, scenario_id: str) -> None:
        """
        Loads one of the four signature spacetime logistics architectures.
        """
        self.clear()

        if scenario_id == "lensing_dispersion":
            # Scenario 1: Gravitational Lensing & Relativistic Dispersion Chute
            # Central massive Schwarzschild black hole deflects light vs heavy test masses at different angles
            bh = Singularity(
                node_id="bh-lens",
                name="Schwarzschild Lens",
                x=400.0,
                y=300.0,
                mass=120.0,
                spin=0.0
            )
            self.singularities.append(bh)

            # Emitter 1: Ultra-fast relativistic tachyon beam (speed = 70.0) -> sharp deflection
            self.emitters.append(Emitter(
                emitter_id="e-fast",
                name="Relativistic Beamer",
                x=80.0,
                y=180.0,
                launch_vx=65.0,
                launch_vy=0.0,
                interval_ticks=30,
                payload_name="Photon-Flux",
                rest_mass=0.2,
                color="#38bdf8"
            ))

            # Emitter 2: Heavy slow baryon stream (speed = 35.0) -> extreme wrap-around deflection
            self.emitters.append(Emitter(
                emitter_id="e-slow",
                name="Baryon Injector",
                x=80.0,
                y=210.0,
                launch_vx=35.0,
                launch_vy=0.0,
                interval_ticks=45,
                payload_name="Heavy-Baryon",
                rest_mass=2.0,
                color="#ec4899"
            ))

            # Collector 1: Targets fast deflected beam
            self.collectors.append(Collector(
                collector_id="c-fast",
                name="Light Cone Receiver",
                x=680.0,
                y=150.0,
                radius=32.0,
                color="#38bdf8"
            ))

            # Collector 2: Targets curved slow stream
            self.collectors.append(Collector(
                collector_id="c-slow",
                name="Heavy Nucleus Trap",
                x=550.0,
                y=520.0,
                radius=36.0,
                color="#ec4899"
            ))

        elif scenario_id == "penrose_accelerator":
            # Scenario 2: Penrose Ergosphere Superradiant Accelerator
            # Fast spinning Kerr singularity (spin=0.92) splits payloads and extracts rotational kinetic energy
            kerr = Singularity(
                node_id="kerr-prime",
                name="Kerr Singularity (a=0.92)",
                x=400.0,
                y=300.0,
                mass=140.0,
                spin=0.92
            )
            self.singularities.append(kerr)

            # Injection emitter aiming straight into the ergoregion with grazing impact
            self.emitters.append(Emitter(
                emitter_id="e-penrose",
                name="Payload Projector",
                x=120.0,
                y=245.0,
                launch_vx=45.0,
                launch_vy=3.0,
                interval_ticks=35,
                payload_name="Raw-ExoCore",
                rest_mass=2.0,
                color="#a855f7"
            ))

            # High-energy collection funnel for the superradiant escaping pulse
            self.collectors.append(Collector(
                collector_id="c-super",
                name="Superradiant Battery",
                x=700.0,
                y=420.0,
                radius=40.0,
                required_min_energy=2000.0,
                color="#f59e0b"
            ))

        elif scenario_id == "dilation_cryowell":
            # Scenario 3: Gravitational Time Dilation Cryo-Well
            # Decaying isotope with tau_half=1.8s. Traveling in flat space decays before reaching 700px!
            # Deep gravitational well dilates proper time, allowing passage to destination.
            well = Singularity(
                node_id="bh-cryo",
                name="Chrono-Gravity Well",
                x=380.0,
                y=290.0,
                mass=160.0,
                spin=0.0
            )
            self.singularities.append(well)

            # Rapidly decaying unstable isotope (half-life = 1.6s)
            self.emitters.append(Emitter(
                emitter_id="e-decay",
                name="Metastable Source",
                x=100.0,
                y=160.0,
                launch_vx=38.0,
                launch_vy=8.0,
                interval_ticks=30,
                payload_name="Unstable-Tau9",
                rest_mass=1.0,
                tau_half=1.8,
                color="#06b6d4"
            ))

            # Destination requires pristine undecayed isotope
            self.collectors.append(Collector(
                collector_id="c-pure",
                name="Pristine Cryo-Silo",
                x=680.0,
                y=320.0,
                radius=35.0,
                reject_decayed=True,
                color="#10b981"
            ))

        elif scenario_id == "freeform_sandbox":
            # Scenario 4: Binary Singularity & Dynamic Gravity Field
            s1 = Singularity("bh-alpha", "Alpha Singularity", 280.0, 300.0, 90.0, spin=0.6)
            s2 = Singularity("bh-beta", "Beta Singularity", 520.0, 300.0, 90.0, spin=-0.6)
            self.singularities.extend([s1, s2])

            self.emitters.append(Emitter(
                "e-sand-1", "North Injector", 400.0, 80.0, 0.0, 30.0,
                interval_ticks=25, payload_name="ExoMatter", color="#6366f1"
            ))
            self.collectors.append(Collector(
                "c-sand-1", "South Well", 400.0, 520.0, radius=45.0, color="#10b981"
            ))
