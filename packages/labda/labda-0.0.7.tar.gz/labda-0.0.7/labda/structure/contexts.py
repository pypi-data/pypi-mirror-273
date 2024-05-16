from pathlib import Path
from typing import Tuple

import geopandas as gpd
import pandas as pd
from shapely import wkt

from ..utils import DEFAULT_CRS_SENSOR
from .validation.context import SCHEMA

# TODO: Check datetime overlap.


def _drop_duplicates(gdf: gpd.GeoDataFrame) -> None:
    gdf = gdf.drop_duplicates(
        subset=["subject_id", "context"], keep="first", inplace=True
    )  # type: ignore


def _fix_crs(
    gdf: gpd.GeoDataFrame,
    crs: str | None | Tuple[str, str] = None,
) -> pd.DataFrame:
    if (
        isinstance(crs, tuple)
        and len(crs) == 2
        and all(isinstance(c, str) for c in crs)
    ):
        source_crs = crs[0]
        target_crs = crs[1]
        gdf.set_crs(source_crs, inplace=True)
        gdf.to_crs(target_crs, inplace=True)
    elif isinstance(crs, str):
        gdf.set_crs(DEFAULT_CRS_SENSOR, inplace=True)
        gdf.to_crs(crs, inplace=True)
    elif not crs:
        gdf.set_crs(DEFAULT_CRS_SENSOR, inplace=True)
        crs = gdf.estimate_utm_crs()
        gdf.to_crs(crs, inplace=True)
    else:
        raise ValueError(f"Invalid value for crs: {crs}")

    return gdf


def from_csv(
    path: str | Path,
    crs: str | None | Tuple[str, str] = None,
) -> gpd.GeoDataFrame:
    if isinstance(path, str):
        path = Path(path)

    df = pd.read_csv(
        path,
        dtype={
            "subject_id": "string",
            "context": "string",
        },
        delimiter=";",
        parse_dates=["start", "end"],
        date_format="%Y-%m-%d %H:%M:%S",
    )

    if "geometry" in df.columns:
        df["geometry"] = df["geometry"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, geometry="geometry")  # type: ignore
        gdf = _fix_crs(gdf, crs)
    else:
        gdf = gpd.GeoDataFrame(df)

    _drop_duplicates(gdf)  # type: ignore

    return SCHEMA.validate(gdf)  # type: ignore


def from_geojson(
    path: str | Path,
    crs: str | None | Tuple[str, str] = None,
) -> gpd.GeoDataFrame:
    if isinstance(path, str):
        path = Path(path)

    gdf = gpd.read_file(path)

    if "geometry" in gdf.columns:
        gdf = _fix_crs(gdf, crs)

    _drop_duplicates(gdf)  # type: ignore

    return SCHEMA.validate(gdf)  # type: ignore


def from_parquet(
    path: str | Path,
    crs: str | None | Tuple[str, str] = None,
) -> gpd.GeoDataFrame:
    if isinstance(path, str):
        path = Path(path)

    gdf = gpd.read_parquet(path)

    if "geometry" in gdf.columns:
        gdf = _fix_crs(gdf, crs)

    _drop_duplicates(gdf)  # type: ignore

    return SCHEMA.validate(gdf)  # type: ignore
