from datetime import datetime
from typing import Any, Dict, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd

from ..structure.validation.subject import Column
from ..utils import convert_to_geodataframe

# TODO: Possibility to specify if point should be INSIDE or OUTSIDE the domain. Maybe?
# TODO: Get domains


def _filter_contexts(subject_id: str, gdf: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.loc[(gdf["subject_id"] == subject_id) | (gdf["subject_id"].isna())]  # type: ignore

    if gdf.empty:
        raise ValueError("No contexts found for the given subject")

    return gdf  # type: ignore


def _get_spatial_context(df: pd.DataFrame, geometry, crs: str) -> None:
    gdf = convert_to_geodataframe(df, crs=crs)
    points = gdf.within(geometry, align=False)
    indexes = points[points].index
    mask = df.index.isin(indexes)
    df["spatial"] = mask


def _get_temporal_context(df: pd.DataFrame, start: datetime, end: datetime) -> None:
    indexes = df.index[(df.index >= start) & (df.index < end)]
    mask = df.index.isin(indexes)
    df["temporal"] = mask


def _get_context_column(df: pd.DataFrame, contexts: list[Dict[str, Any]]) -> None:
    df[Column.CONTEXT] = pd.NA

    for cnt in contexts:
        df.loc[df.index.isin(cnt["indexes"]), "context"] = cnt["context"]

    df[Column.CONTEXT] = df[Column.CONTEXT].astype("category")


def detect_contexts(
    subject_id: str,
    df: pd.DataFrame,
    contexts: gpd.GeoDataFrame,
    crs: str | None = None,
) -> Tuple[pd.DataFrame, list[dict[str, Any]]]:
    temp_df = df[[Column.LATITUDE, Column.LONGITUDE]].copy()
    contexts = _filter_contexts(subject_id, contexts)

    results = []

    for context in contexts.itertuples():
        context = context._asdict()  # type: ignore
        geometry = context.get("geometry")
        start = context.get("start")
        end = context.get("end")

        if geometry and crs:
            _get_spatial_context(temp_df, geometry, crs)

        if start or end:
            _get_temporal_context(temp_df, start, end)

        if "spatial" in temp_df.columns and "temporal" in temp_df.columns:
            mask = temp_df["spatial"] & temp_df["temporal"]
            indexes = mask[mask].index
        elif "spatial" in temp_df.columns:
            indexes = temp_df[temp_df["spatial"]].index
        elif "temporal" in temp_df.columns:
            indexes = temp_df[temp_df["temporal"]].index

        context["indexes"] = indexes
        results.append(context)

    results = sorted(results, key=lambda c: c.get("priority"))
    _get_context_column(df, results)

    return df, results
