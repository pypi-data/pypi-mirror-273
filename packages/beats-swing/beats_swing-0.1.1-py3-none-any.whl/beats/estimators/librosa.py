"""Librosa-based tempo estimators."""

from typing import Mapping

import librosa

from beats.estimators.api import Estimator
from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


class Librosav1(Estimator):
    """Tempo estimator using `librosa.beat.beat_track`."""

    def __init__(self, start_bpm: float = 120.0, tightness: float = 100.0):
        self._start_bpm = start_bpm
        self._tightness = tightness

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        tempo, _ = librosa.beat.beat_track(
            y=song, sr=fs, start_bpm=self._start_bpm, tightness=self._tightness
        )
        return Tempo(float(tempo))

    def params(self) -> Mapping[str, str | float | int]:
        return {
            "start_bpm": self._start_bpm,
            "tightness": self._tightness,
        }


class Librosav2(Estimator):
    """Tempo estimator using `librosa.beat.beat_track`.
    It takes the initial guess of the tempo and seeds another search with it.
    We retain the higher guess out of the two.

    This approach seems to be surprisingly good at picking out harmonics.
    """

    def __init__(self, start_bpm: float = 120.0, tightness: float = 100.0):
        self._start_bpm = start_bpm
        self._tightness = tightness

    def tempo(self, song: Song, fs: SamplingRate) -> Tempo:
        tempo, _ = librosa.beat.beat_track(
            y=song, sr=fs, start_bpm=self._start_bpm, tightness=self._tightness
        )
        tempo2, _ = librosa.beat.beat_track(
            y=song, sr=fs, start_bpm=float(tempo) * 2, tightness=self._tightness
        )
        if tempo2 >= 1.8 * tempo:
            return Tempo(float(tempo2))
        else:
            return Tempo(float(tempo))

    def params(self) -> Mapping[str, str | float | int]:
        return {
            "start_bpm": self._start_bpm,
            "tightness": self._tightness,
        }
