"""This module collects common types."""

from typing import NewType

import numpy as np
import numpy.typing as npt


Vector = NewType("Vector", npt.NDArray[np.complex64])
SamplingRate = NewType("SamplingRate", float)
Tempo = NewType("Tempo", float)  # in beats per minute

# A 1D array where the samples represent sound amplitude at subsequent time instants
Song = NewType("Song", npt.NDArray[np.complex64])
