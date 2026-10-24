import pytest
import math
from geodesic.spacetime import SpacetimeMetrics, G, C, C_SQ


def test_constants_and_scaling():
    assert G == 1000.0
    assert C == 100.0
    assert C_SQ == 10000.0


def test_schwarzschild_radius():
    # rs = 2 * G * M / c^2 = 2 * 1000 * 100 / 10000 = 20.0
    rs = SpacetimeMetrics.schwarzschild_radius(100.0)
    assert pytest.approx(rs, rel=1e-5) == 20.0

    # Negative or zero mass
    assert SpacetimeMetrics.schwarzschild_radius(0.0) == 0.0
    assert SpacetimeMetrics.schwarzschild_radius(-50.0) == 0.0


def test_photon_sphere_and_isco():
    mass = 120.0
    rs = SpacetimeMetrics.schwarzschild_radius(mass)
    r_ph = SpacetimeMetrics.photon_sphere_radius(mass)
    r_isco = SpacetimeMetrics.isco_radius(mass, spin=0.0)

    # In Schwarzschild geometry, r_ph = 1.5 * rs, r_isco = 3.0 * rs
    assert pytest.approx(r_ph, rel=1e-5) == 1.5 * rs
    assert pytest.approx(r_isco, rel=1e-5) == 3.0 * rs


def test_kerr_ergosphere():
    mass = 100.0
    # In equator theta = pi/2, outer boundary is 2M = rs
    r_ergo = SpacetimeMetrics.ergosphere_radius(mass, spin=0.9, theta=math.pi / 2)
    rs_static = SpacetimeMetrics.schwarzschild_radius(mass)
    assert pytest.approx(r_ergo, rel=1e-5) == rs_static


def test_time_dilation_factor():
    mass = 100.0
    # Far away at rest: dtau / dt -> 1.0
    dil_far = SpacetimeMetrics.time_dilation_factor(mass, r=100000.0, velocity=0.0)
    assert pytest.approx(dil_far, rel=1e-3) == 1.0

    # Near ISCO (r = 60.0): 2GM / (r*c^2) = 20/60 = 1/3
    # at rest: dtau/dt = sqrt(1 - 1/3) = sqrt(2/3) ~ 0.8165
    dil_isco = SpacetimeMetrics.time_dilation_factor(mass, r=60.0, velocity=0.0)
    assert pytest.approx(dil_isco, rel=1e-3) == math.sqrt(2.0 / 3.0)

    # Inside horizon (r = 15.0 < rs=20.0): dilation should be 0.0
    dil_inside = SpacetimeMetrics.time_dilation_factor(mass, r=15.0, velocity=0.0)
    assert dil_inside == 0.0


def test_gravitational_deflection():
    mass = 100.0
    b = 50.0
    # Ultra-relativistic limit
    defl_fast = SpacetimeMetrics.gravitational_deflection(mass, impact_param=b, velocity=C)
    # 4GM / (c^2 * b) = 4 * 1000 * 100 / (10000 * 50) = 400000 / 500000 = 0.8 rad
    assert pytest.approx(defl_fast, rel=1e-3) == 0.8


def test_exotic_negative_mass_repulsion():
    # Negative mass node produces repulsive gravitational deflection
    neg_mass = -80.0
    defl = SpacetimeMetrics.gravitational_deflection(neg_mass, impact_param=40.0, velocity=50.0)
    assert defl < 0.0
    assert SpacetimeMetrics.schwarzschild_radius(neg_mass) == 0.0
