"""A little pipeline to score runs to a local MLflow."""

import dataclasses
import hashlib
from pathlib import Path
from typing import Sequence
from typing import Tuple

import librosa
import mlflow
import mlflow.tracking.fluent as mltrack
import numpy as np
import plotly.express as px

from beats.estimators.api import Estimator
from beats.estimators.librosa import Librosav1
from beats.estimators.librosa import Librosav2
from beats.estimators.trivial import Zero
from beats.estimators.utils import Metrics
from beats.estimators.utils import score
from beats.types import SamplingRate
from beats.types import Song
from beats.types import Tempo
from beats.types import Vector


def song_from_file(
    audio_file: Path,
) -> Tuple[Song, SamplingRate, Tempo]:  # TODO: cache?
    y, fs = librosa.load(str(audio_file), sr=None)
    # tempo should be encoded as the first 3 characters of the file name;
    # 50 is encoded as 050
    ground_truth_tempo = int(audio_file.name[0:3])
    return Song(y), SamplingRate(fs), Tempo(ground_truth_tempo)


MLFLOW_DIR = Path(__file__).parent.parent / "mlflow"
MP3_DIR = Path(__file__).parent.parent / "data"

ESTIMATORS: Sequence[Estimator] = [
    Zero(),
    Librosav1(),
    Librosav2(),
]
DATASET = [f for f in MP3_DIR.iterdir() if f.suffix in [".mp3", ".m4a"]]
SONGS: Sequence[Tuple[Song, SamplingRate, Tempo]] = [song_from_file(d) for d in DATASET]


def store(metrics: Metrics, estimator: Estimator, dataset: Sequence[Path]) -> None:
    for k, v in dataclasses.asdict(metrics).items():
        if isinstance(v, (int, float)):
            mltrack.log_metric(k, v)

    mltrack.set_tags(
        {
            "dataset_hash": hashlib.sha256(
                "".join([str(d) for d in dataset]).encode()
            ).hexdigest()
        }
    )

    for k, v in estimator.params().items():
        mltrack.log_param(k, v)

    df = metrics.all_df
    df["name"] = [d.name for d in dataset]
    mltrack.log_table(metrics.all_df, "details.json")

    mltrack.log_figure(
        px.scatter(df, x="true", y="pred", hover_data="name"), "true_vs_pred.html"
    )


def pipeline() -> None:
    mlflow.set_tracking_uri(f"file://{MLFLOW_DIR}")
    # unclear why MyPy doesn't see this
    mltrack.set_experiment("tempo-tracking")

    for est in ESTIMATORS:
        with mltrack.start_run(run_name=est.__class__.__name__):
            predictions = Vector(
                np.array([est.tempo(song, fs) for song, fs, _ in SONGS])
            )
            ground_truth = Vector(np.array([true_tempo for _, _, true_tempo in SONGS]))
            res = score(predictions, ground_truth)
            store(res, est, DATASET)


if __name__ == "__main__":
    pipeline()
