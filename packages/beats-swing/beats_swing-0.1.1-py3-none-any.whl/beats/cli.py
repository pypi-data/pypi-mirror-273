"""A simple CLI interface for the tempo estimator."""

import argparse
import dataclasses
from pathlib import Path
from typing import Tuple

import librosa

from beats.constants import SUPPORTED_FORMATS
from beats.estimators.librosa import Librosav2
from beats.shared_types import SamplingRate
from beats.shared_types import Song
from beats.shared_types import Tempo


@dataclasses.dataclass
class Args:
    """CLI arguments"""

    music_file: Path


def _parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="Path to your music file.", type=str, required=True
    )
    args = parser.parse_args()
    music_file = Path(args.file)

    if music_file.suffix not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Only '{SUPPORTED_FORMATS}' files supported. "
            f"Instead got: {music_file.suffix}"
        )

    if not music_file.exists():
        raise ValueError(
            f"Could not find the file at {music_file}. "
            f"Is the path correct relative to working directory?"
        )

    return Args(music_file=music_file)


def _song_from_file(
    audio_file: Path,
) -> Tuple[Song, SamplingRate]:
    y, fs = librosa.load(str(audio_file), sr=None)
    return Song(y), SamplingRate(fs)


def _estimate_tempo(audio_file: Path) -> Tempo:
    song, fs = _song_from_file(audio_file)
    tempo = Librosav2().tempo(song, fs)
    return tempo


def main() -> None:
    """Print the estimated tempo to stdout."""
    args = _parse_args()
    tempo = _estimate_tempo(args.music_file)
    print(int(tempo))


if __name__ == "__main__":
    main()
