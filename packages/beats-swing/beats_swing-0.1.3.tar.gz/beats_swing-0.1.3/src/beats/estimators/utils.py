"""This module contains various utilities for estimators."""

import dataclasses

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from beats.shared_types import Vector


@dataclasses.dataclass
class Metrics:
    """A container with various performance metrics."""

    mean_squared_error: float
    root_mean_squared_error: float
    mean_absolute_error: float
    r_squared: float

    all_df: pd.DataFrame


def score(predictions: Vector, ground_truth: Vector) -> Metrics:
    df = pd.DataFrame({"pred": predictions, "true": ground_truth})

    df["error"] = df["pred"] - df["true"]
    mse = float(np.square(df["error"].values).mean())
    return Metrics(
        mean_squared_error=mse,
        root_mean_squared_error=float(np.sqrt(mse)),
        mean_absolute_error=float(abs(df["error"].mean())),
        r_squared=r2_score(df["pred"], df["true"]),
        all_df=df,
    )
