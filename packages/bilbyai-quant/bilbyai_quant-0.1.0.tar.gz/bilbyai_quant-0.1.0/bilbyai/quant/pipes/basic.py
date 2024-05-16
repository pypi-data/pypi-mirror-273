import logging

import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__name__)


def add_week_range(
    df: DataFrame, *, week_range_col: str = "week_range", date_col: str = "date"
) -> DataFrame:
    df[week_range_col] = df[date_col].dt.to_period("W")
    return df


def filter_by_text(df: DataFrame, *, text_col: str = "bodyZh", text: str) -> DataFrame:
    return df[df[text_col].str.contains(text)].copy()


def filter_to_week(df: DataFrame, week: str, *, week_range_col: str = "week_range") -> DataFrame:
    logger.debug(week)
    return df[df[week_range_col] == week]


def convert_dates(df: DataFrame, date_col: str = "date") -> DataFrame:
    df[date_col] = pd.to_datetime(df[date_col])
    return df
