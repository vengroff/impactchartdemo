"""A synthetic data set for demonstration purposes."""
from typing import Tuple, Union

import numpy as np
import pandas as pd


FeatureType = Union[int, float, pd.Series, np.array]


def t0(X: pd.DataFrame) -> pd.Series:
    return X['x_0']


def t1(X: pd.DataFrame) -> pd.Series:
    x1 = X['x_1']
    return 100.0 * (1.0 - 2.0 * (x1 / 100.0) * (x1 / 100.0))


def t2(X: pd.DataFrame) -> pd.Series:
    x2 = X['x_2']
    return 100.0 * np.sin(np.pi * (x2 / 100.0))


def t3(X: pd.DataFrame) -> pd.Series:
    return pd.Series(np.zeros(len(X)), index=X.index)


def t4(X: pd.DataFrame) -> pd.Series:
    x4 = X['x_4']
    k = 7
    return 200.0 * np.exp(k * ((x4 / 100.0) - 1.0))


def f(X: pd.DataFrame) -> pd.Series:
    return t0(X) + t1(X) + t2(X) + t3(X) + t4(X) + np.random.normal(0, 10.0, size=len(X.index))


def get_data(n: int = 1_000) -> Tuple[pd.DataFrame, pd.Series]:
    """Generate synthetic data."""
    np.random.seed(17)
    X = pd.DataFrame(
        np.random.uniform(low=-100.0, high=100.0, size=(n, 5)),
        columns=['x_0', 'x_1', 'x_2', 'x_3', 'x_4']
    )
    y = f(X)

    return X, y


