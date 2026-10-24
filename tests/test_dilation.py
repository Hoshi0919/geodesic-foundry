import pytest
from geodesic.payload import Payload
from geodesic.singularity import Singularity
from geodesic.integrator import GeodesicIntegrator


def test_payload_proper_time_decay():
    # Payload with proper half-life tau_half = 1.0s
    p = Payload("Isotope-X", x=0.0, y=0.0, vx=10.0, vy=0.0, tau_half=1.0)
    assert not p.is_decayed

    # Advance 0.5s with dilation = 1.0 (flat space)
    p.step_proper_time(dt=0.5, dilation_factor=1.0)
    assert pytest.approx(p.proper_time, rel=1e-3) == 0.5
    assert not p.is_decayed

    # Advance another 0.6s -> proper time = 1.1s > tau_half
    p.step_proper_time(dt=0.6, dilation_factor=1.0)
    assert p.proper_time >= 1.0
    assert p.is_decayed is True


def test_gravitational_dilation_preservation():
    # Two identical payloads with tau_half = 0.5s
    # p1 travels in flat space (dilation = 1.0)
    # p2 travels in high-gravity region near horizon (dilation = 0.2)
    p1 = Payload("Flat-Space-Particle", x=0.0, y=0.0, vx=10.0, vy=0.0, tau_half=0.5)
    p2 = Payload("Dilated-Particle", x=0.0, y=0.0, vx=10.0, vy=0.0, tau_half=0.5)

    # Coordinate / lab time dt = 0.8s
    dt = 0.8
    p1.step_proper_time(dt=dt, dilation_factor=1.0)
    p2.step_proper_time(dt=dt, dilation_factor=0.2)

    # In flat space, proper time = 0.8s > 0.5s -> decayed!
    assert p1.is_decayed is True
    # In gravity well, proper time = 0.8 * 0.2 = 0.16s < 0.5s -> preserved pristine!
    assert p2.is_decayed is False
    assert pytest.approx(p2.proper_time, rel=1e-3) == 0.16
