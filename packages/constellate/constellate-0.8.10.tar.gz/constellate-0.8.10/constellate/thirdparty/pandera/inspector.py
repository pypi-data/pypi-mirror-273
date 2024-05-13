from typing import List, Dict

import pandas as pd
from pandera import SchemaModel, Field


def schema_columns(schema: SchemaModel = None) -> List[str]:
    return [k for k, v in dict(schema.__dict__) if isinstance(v, Field)]


def dataframe_from_schema(
    schema: SchemaModel = None,
    reset_index_kwargs: Dict = None,
    rename_kwargs: Dict = None,
    extra_columns: Dict = None,
) -> pd.DataFrame:
    """Create an empty dataframe based on a schema

    :param schema: SchemaModel:  (Default value = None)
    :param reset_index_kwargs: Dict:  (Default value = {"inplace": True})
    :param rename_kwargs: Dict:  (Default value = {})
    :param extra_columns: Dict:  (Default value = {})

    """
    reset_index_kwargs = reset_index_kwargs or {"inplace": True}
    if rename_kwargs is None:
        rename_kwargs = {}
    if extra_columns is None:
        extra_columns = {}

    # Requires: hypothesis package
    df = schema.to_schema().example(size=0)

    # Move / Rename / Add columns
    if len(reset_index_kwargs):
        df.reset_index(**reset_index_kwargs)
    if len(rename_kwargs) > 0:
        df.rename(**rename_kwargs)
    for col_name, dtype in extra_columns.items():
        df.insert(0, col_name, [], allow_duplicates=False)
        df = df.astype({col_name: dtype}, copy=False, errors="ignore")
    return df


def series_from_schema(
    schema: SchemaModel = None,
    rename_kwargs: Dict = None,
) -> pd.Series:
    """Create an empty series based on a schema

    :param schema: SchemaModel:  (Default value = None)
    :param rename_kwargs: Dict:  (Default value = {})

    """
    if rename_kwargs is None:
        rename_kwargs = {}
    # Requires: hypothesis package
    df = schema.to_schema().example(size=0)

    if len(rename_kwargs) > 0:
        df.rename(**rename_kwargs)

    return df.squeeze(axis="columns")
