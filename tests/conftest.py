from __future__ import annotations

from pathlib import Path

import pytest

from core.pipeline import Settings, load_matches, run_pipeline

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "matches.csv"


@pytest.fixture(scope="session")
def matches():
    return load_matches(DATA_PATH)


@pytest.fixture(scope="session")
def model(matches):
    return run_pipeline(matches, Settings(n_sims=1_000, seed=123))
