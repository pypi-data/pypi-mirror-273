"""Trivial baselines."""

from typing import Mapping

from beats.estimators.api import Estimator
from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


class Zero(Estimator):

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        return Tempo(0.0)

    def params(self) -> Mapping[str, str | float | int]:
        return {}
