import pytest
from geodesic.singularity import Singularity
from geodesic.payload import Payload
from geodesic.penrose import PenroseReactor


def test_penrose_fission_inside_ergosphere():
    kerr = Singularity("kerr-1", "Kerr Black Hole", x=200.0, y=200.0, mass=100.0, spin=0.8)
    # Kerr mass=100: rs=20.0, m_geom=10.0.
    # r_+ = 10 * (1 + sqrt(1 - 0.64)) = 10 * 1.6 = 16.0
    # r_ergo = 20.0
    # Place particle inside ergoregion at r=18.0 (x=218.0, y=200.0)
    p = Payload("Test-Core", x=218.0, y=200.0, vx=0.0, vy=30.0, rest_mass=2.0)

    assert kerr.is_inside_ergosphere(p.x, p.y)

    res = PenroseReactor.attempt_fission(p, kerr, fission_efficiency=0.4)
    assert res is not None
    retro, esc = res

    # Original payload consumed
    assert p.is_absorbed is True
    # Infalling fragment marked for absorption
    assert retro.is_absorbed is True
    # Escaping fragment boosted
    assert esc.energy_boosted is True
    assert esc.kinetic_energy > p.kinetic_energy
    assert kerr.extracted_energy > 0.0


def test_penrose_rejected_outside_ergosphere():
    kerr = Singularity("kerr-1", "Kerr Black Hole", x=200.0, y=200.0, mass=100.0, spin=0.8)
    # Outside at r = 50.0
    p = Payload("Far-Core", x=250.0, y=200.0, vx=0.0, vy=30.0)
    assert not kerr.is_inside_ergosphere(p.x, p.y)

    res = PenroseReactor.attempt_fission(p, kerr)
    assert res is None
