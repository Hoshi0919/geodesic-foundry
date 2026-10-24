"""
Geodesic Foundry: Relativistic Spacetime & Gravitational Logistics Simulation.

Core mechanics:
- Schwarzschild & Kerr metric geodesic integration
- Gravitational & kinematic time dilation for decaying payloads
- Penrose ergosphere superradiant energy extraction
- Gravitational lensing & relativistic dispersion chute sorting
"""

__version__ = "1.0.0"
__author__ = "Hoshi <hoshi0919@outlook.com>"

from .spacetime import SpacetimeMetrics, G, C
from .singularity import Singularity
from .payload import Payload
from .penrose import PenroseReactor
from .integrator import GeodesicIntegrator
from .engine import FoundryEngine, Emitter, Collector

__all__ = [
    "SpacetimeMetrics",
    "G",
    "C",
    "Singularity",
    "Payload",
    "PenroseReactor",
    "GeodesicIntegrator",
    "FoundryEngine",
    "Emitter",
    "Collector",
]
