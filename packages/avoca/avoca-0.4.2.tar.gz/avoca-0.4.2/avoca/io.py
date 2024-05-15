from pathlib import Path

import pandas as pd


def to_csv(df: pd.DataFrame, path: Path):
    """Export a dataframe to a csv file."""
    df.to_csv(path, index=False)


def from_csv(path: Path) -> pd.DataFrame:
    """Read a csv file to a dataframe."""
    df = pd.read_csv(path, header=[0, 1])
    parse_dates = [("-", "datetime")]
    # Convert the datetime column to a datetime object
    for col in parse_dates:
        if col not in df.columns:
            continue
        df[col] = pd.to_datetime(df[col])
    return df
