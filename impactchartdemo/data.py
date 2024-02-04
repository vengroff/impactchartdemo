"""Data sets for the impact chart demo."""

import itertools
from typing import List, Tuple, Dict

import censusdis.data as ced
from censusdis.datasets import ACS5

import pandas as pd


DEMOGRAPHIC_VARIABLES = {
    "B03002_003E": "Population Who Identify as Non-Hispanic or Latino White Alone",
    "B03002_004E": "Population Who Identify as Non-Hispanic or Latino Black of African American Alone",
    "B03002_005E": "Population Who Identify as Non-Hispanic or Latino American Indian and Alaska Native Alone",
    "B03002_006E": "Population Who Identify as Non-Hispanic or Latino Asian Alone",
    "B03002_007E": "Population Who Identify as Non-Hispanic or Latino Native Hawaiian and Other Pacific Islander Alone",
    "B03002_008E": "Population Who Identify as Non-Hispanic or Latino Some Other Race Alone",
    "B03002_010E": "Population Who Identify as Non-Hispanic or Latino Two Races Including Some Other Race",
    "B03002_011E": "Population Who Identify as Non-Hispanic or Latino Two Races Excluding Some Other Race, "
    "and Three or More Races",
    "B03002_012E": "Population Who Identify as Hispanic or Latino of Any Race",
}

VARIABLE_MEDIAN_HOUSEHOLD_INCOME = "B19013_001E"
VARIABLE_TOTAL_OWNER_OCCUPIED = "B25003_002E"
VARIABLE_MEDIAN_HOME_VALUE = "B25077_001E"
VARIABLE_TOTAL_POPULATION = "B03002_001E"

ADDITIONAL_VARIABLES = {
    # We will use this as a denominator to create fractional demographic features.
    VARIABLE_TOTAL_POPULATION: "Total Population",
    # This will be a feature in our model.
    VARIABLE_MEDIAN_HOUSEHOLD_INCOME: "Median Household Income",
    # We will use this as a weight in our model, so it will
    # treat areas with more owner-occupied households as more
    # important to get right.
    VARIABLE_TOTAL_OWNER_OCCUPIED: "Total Owner-Occupied Households",
    # This is the target we are trying to predict/explain.
    VARIABLE_MEDIAN_HOME_VALUE: "Median Home Value",
}

TARGET = VARIABLE_MEDIAN_HOME_VALUE
TARGET_NAME = ADDITIONAL_VARIABLES[TARGET]


def states_in_cbsa(cbsa: str):
    """Determine the states that intersect a given cbsa."""
    df_states = ced.contained_within(
        area_threshold=float("-inf"),
        metropolitan_statistical_area_micropolitan_statistical_area=cbsa,
    ).download(dataset=ACS5, vintage=2021, download_variables=["NAME"], state="*")

    return list(df_states["STATE"])


def all_cbsas():
    """Get a data frame of all CBSAs and their names."""
    return ced.download(
        dataset=ACS5,
        vintage=2021,
        download_variables=["NAME"],
        metropolitan_statistical_area_micropolitan_statistical_area="*",
    )


def home_value_demongraphics_data(cbsa: str) -> Tuple[pd.DataFrame, pd.Series, pd.Series, Dict[str, str]]:
    """Build a data set of home value, demographic, and median income data at the block group level for a given cbsa."""

    states = states_in_cbsa(cbsa)

    df_census = ced.contained_within(
        metropolitan_statistical_area_micropolitan_statistical_area=cbsa
    ).download(
        dataset=ACS5,
        vintage=2021,
        download_variables=itertools.chain(
            ["NAME"],
            DEMOGRAPHIC_VARIABLES.keys(),
            ADDITIONAL_VARIABLES.keys(),
        ),
        state=states,
        county="*",
        tract="*",
        block_group="*",
    )

    # Just in case any is missing, we'll do a simple dropna.
    df_census.dropna(inplace=True)

    # Income is capped at $250k; higher values clipped to $250.001.
    # Home values is capped at $2MM; higher values clipped to $2,000,000.
    df_census = df_census[
        (df_census[VARIABLE_MEDIAN_HOME_VALUE] <= 2_000_000) &
        (df_census[VARIABLE_MEDIAN_HOUSEHOLD_INCOME] <= 250_000)
        ]

    # Create fractional demographic features.
    feature_names = {}

    for variable, description in DEMOGRAPHIC_VARIABLES.items():
        frac_variable = f'frac_{variable}'
        df_census[frac_variable] = df_census[variable] / df_census[VARIABLE_TOTAL_POPULATION]
        feature_names[frac_variable] = f'Fraction of {description}'

    # Add the median income features.
    feature_names[VARIABLE_MEDIAN_HOUSEHOLD_INCOME] = ADDITIONAL_VARIABLES[VARIABLE_MEDIAN_HOUSEHOLD_INCOME]

    X = df_census[feature_names.keys()]

    # Target
    y = df_census[VARIABLE_MEDIAN_HOME_VALUE]

    # Weight
    w = df_census[VARIABLE_TOTAL_OWNER_OCCUPIED]

    return X, y, w, feature_names
