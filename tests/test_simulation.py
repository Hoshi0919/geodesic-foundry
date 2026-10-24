import pytest
from geodesic.engine import FoundryEngine, Emitter, Collector
from geodesic.singularity import Singularity
from geodesic.payload import Payload


def test_engine_initialization_and_clear():
    engine = FoundryEngine(width=800, height=600)
    assert len(engine.singularities) == 0
    assert len(engine.payloads) == 0

    engine.load_scenario("lensing_dispersion")
    assert len(engine.singularities) == 1
    assert len(engine.emitters) == 2
    assert len(engine.collectors) == 2

    engine.clear()
    assert len(engine.singularities) == 0
    assert len(engine.emitters) == 0


def test_scenario_lensing_simulation():
    engine = FoundryEngine(width=800, height=600)
    engine.load_scenario("lensing_dispersion")

    # Run for 120 ticks
    for _ in range(120):
        engine.step()

    # Verify emitters generated payloads and payloads traversed spacetime
    assert engine.tick_count == 120
    assert engine.emitters[0].total_emitted > 0
    assert engine.emitters[1].total_emitted > 0


def test_scenario_penrose_simulation():
    engine = FoundryEngine(width=800, height=600)
    engine.load_scenario("penrose_accelerator")

    # Run for 150 ticks
    for _ in range(150):
        engine.step()

    assert engine.tick_count == 150
    assert len(engine.singularities) == 1
    assert engine.singularities[0].spin == 0.92


def test_scenario_dilation_cryowell():
    engine = FoundryEngine(width=800, height=600)
    engine.load_scenario("dilation_cryowell")

    for _ in range(100):
        engine.step()

    assert engine.tick_count == 100
    assert len(engine.emitters) == 1
    assert engine.emitters[0].tau_half == 1.8


def test_scenario_freeform_sandbox():
    engine = FoundryEngine(width=800, height=600)
    engine.load_scenario("freeform_sandbox")

    for _ in range(80):
        engine.step()

    assert engine.tick_count == 80
    assert len(engine.singularities) == 2
