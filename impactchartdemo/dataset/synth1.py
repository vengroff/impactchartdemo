"""A synthetic data set for demonstration purposes."""

from typing import Tuple, Union, Callable

import numpy as np
import pandas as pd


FeatureType = Union[int, float, pd.Series, np.array]


def t0(X: pd.DataFrame) -> pd.Series:
    return X["x_0"]


def t1(X: pd.DataFrame) -> pd.Series:
    x1 = X["x_1"]
    return 100.0 * (1.0 - 2.0 * (x1 / 100.0) * (x1 / 100.0))


def t2(X: pd.DataFrame) -> pd.Series:
    x2 = X["x_2"]
    return 100.0 * np.sin(2.0 * np.pi * (x2 / 100.0))


def t3(X: pd.DataFrame) -> pd.Series:
    x3 = X["x_3"]
    k = 7
    return 200.0 * np.exp(k * ((x3 / 100.0) - 1.0))


def t4(X: pd.DataFrame) -> pd.Series:
    return pd.Series(np.zeros(len(X)), index=X.index)


def term(x_col: str) -> Callable[[FeatureType], FeatureType]:
    if x_col == "x_0":
        return t0
    if x_col == "x_1":
        return t1
    if x_col == "x_2":
        return t2
    if x_col == "x_3":
        return t3
    if x_col == "x_4":
        return t4

    raise ValueError(f"Unknown feature: {x_col}")


def f(X: pd.DataFrame) -> pd.Series:
    return (
        t0(X)
        + t1(X)
        + t2(X)
        + t3(X)
        + t4(X)
        + np.random.normal(0, 10.0, size=len(X.index))
    )


def get_data(n: int = 1_000, seed: int = 17) -> Tuple[pd.DataFrame, pd.Series]:
    """Generate synthetic data."""
    np.random.seed(seed)
    X = pd.DataFrame(
        np.random.uniform(low=-100.0, high=100.0, size=(n, 5)),
        columns=["x_0", "x_1", "x_2", "x_3", "x_4"],
    )
    y = f(X)
    y.name = "y"

    return X, y
