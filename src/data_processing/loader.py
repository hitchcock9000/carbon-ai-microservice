import pandas as pd
from pathlib import Path


def load_building_metadata(csv_path: str | Path = "data/raw/building_metadata.csv") -> pd.DataFrame:
    """Load the building metadata CSV.

    Parameters
    ----------
    csv_path: str | Path, optional
        Path to the CSV file. Defaults to the location used in the repository.

    Returns
    -------
    pd.DataFrame
        DataFrame with raw building metadata.
    """
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Building metadata file not found: {path}")
    df = pd.read_csv(path)
    return df


def preprocess_building_df(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning and feature engineering for building metadata.

    The function performs:
    * Missing‑value handling (numeric columns → median, categorical → mode)
    * Type casting (e.g., dates, categorical strings)
    * Simple engineered features such as building age and floor‑area‑per‑occupant.
    """
    df = df.copy()

    # Example: ensure numeric columns are proper dtype
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)

    # Example categorical handling
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        df[col] = df[col].astype(str).fillna(df[col].mode().iloc[0])

    # Feature engineering – assume columns exist; ignore if not
    if "construction_year" in df.columns:
        current_year = pd.Timestamp.now().year
        df["building_age"] = current_year - df["construction_year"].astype(int)
    if "floor_area" in df.columns and "occupants" in df.columns:
        df["area_per_occupant"] = df["floor_area"] / df["occupants"].replace({0: pd.NA})
        df["area_per_occupant"].fillna(df["area_per_occupant"].median(), inplace=True)

    # One‑hot encode categorical columns for downstream ML
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df
