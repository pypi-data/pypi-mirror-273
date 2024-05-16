"""This module defines the estimator API."""

import abc
from typing import Mapping

from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


class Estimator(abc.ABC):
    """This is the interface for an estimator."""

    @abc.abstractmethod
    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        """Estimate the tempo for the specified song."""

    @abc.abstractmethod
    def params(self) -> Mapping[str, str | float | int]:
        """Parameters you'd like to associate with the estimator instance."""
