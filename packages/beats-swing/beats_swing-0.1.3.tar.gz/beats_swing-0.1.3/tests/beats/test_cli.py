"""Simple tests for the CLI utility."""

from pathlib import Path

from beats.cli import estimate_tempo


TEST_FILE = Path(__file__).parent / "data" / "sample_168.mp3"


def test_estimator__is_not_smoking() -> None:
    true_tempo = 168
    tol = 5
    assert abs(estimate_tempo(TEST_FILE) - true_tempo) < tol
