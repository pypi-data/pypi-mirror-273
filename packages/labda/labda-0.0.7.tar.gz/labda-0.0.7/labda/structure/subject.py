from datetime import datetime, timedelta
from enum import StrEnum
from math import log
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import geopandas as gpd

if TYPE_CHECKING:
    # This is a workaround to avoid circular imports.
    # TODO: Is there a better way to do this?
    from .collection import Collection
import logging

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, Field
from shapely.geometry import MultiPolygon

from ..expanders import (
    add_acceleration,
    add_direction,
    add_distance,
    add_speed,
    add_timedelta,
)
from ..processing.accelerometer import detect_activity_intensity, detect_wear
from ..processing.context import detect_contexts
from ..processing.spatial import detect_transportation, detect_trips, get_timeline
from ..structure.resampling import upsample
from ..visualisation.spatial import plot
from .validation.subject import SCHEMA, Column

logger = logging.getLogger("default")


def log_message(subject: "Subject", message: str, origin: str):
    meta = subject.metadata
    logger.info(message, extra={"origin": origin, "object": meta.id})


class Vendor(StrEnum):
    ACTIGRAPH = "ActiGraph"
    XIAOMI = "Xiaomi"
    SENS = "Sens"
    GARMIN = "Garmin"
    QSTARZ = "Qstarz"
    GGIR = "GGIR"
    SENSECAP = "SenseCap"
    TRACCAR = "Traccar"


class Sensor(BaseModel):
    id: str
    serial_number: str | None = None
    model: str | None = None
    vendor: Vendor | None = None
    firmware_version: str | None = None
    extra: dict[str, Any] | None = None

    class Config:
        coerce_numbers_to_str = True


class Metadata(BaseModel):
    id: str
    sensor: list[Sensor] = Field(default_factory=list)
    sampling_frequency: float = Field(ge=0, description="Sampling frequency in seconds")
    crs: str | None = None
    timezone: str | None = None

    class Config:
        coerce_numbers_to_str = True


class Context(BaseModel):
    id: str = Field(validation_alias="context")
    start: datetime | None = None
    end: datetime | None = None
    geometry: MultiPolygon | None = None
    priority: int | None = None
    indexes: list[datetime] | None = None

    class Config:
        arbitrary_types_allowed = True


class Subject(BaseModel):
    metadata: Metadata
    collection: Optional["Collection"] = None
    df: pd.DataFrame
    timeline: pd.DataFrame | None = None
    contexts: list[Context] = Field(default_factory=list)

    # TODO: Add check for not empty dataframe.

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return str(f"{self.metadata}\n{self.df}")

    @property
    def domains(self):
        # TODO: Implement this property.
        raise NotImplementedError("This method is not implemented yet.")

    def to_parquet(
        self,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Writes the subject's data to a Parquet file. The metadata is stored in the file's schema.

        Before saving, the subject's DataFrame is validated to ensure it conforms to the schema LABDA standard format.

        Args:
            path (str | Path): The path to write the Parquet file to.
            overwrite (bool, optional): Whether to overwrite an existing file at the path. Defaults to `False`.

        Raises:
            FileExistsError: If a file already exists at the path and `overwrite` is `False`.
        """
        if isinstance(path, str):
            path = Path(path)

        if path.exists() and not overwrite:
            raise FileExistsError(
                f"The file '{path}' already exists. If you want to overwrite it, set the 'overwrite' argument to 'True'."
            )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        custom_metadata = {"labda".encode(): self.metadata.model_dump_json().encode()}
        self.validate()
        table = pa.Table.from_pandas(self.df)

        existing_metadata = table.schema.metadata
        combined_meta = {**custom_metadata, **existing_metadata}

        table = table.replace_schema_metadata(combined_meta)
        pq.write_table(table, path)
        log_message(self, f"Subject exported: {path}", origin=f"{__name__}.to_parquet")

    @classmethod
    def from_parquet(cls, path: str | Path) -> "Subject":
        """
        Loads a subject from a Parquet file. While loading, subject's data is validated to ensure it conforms to the schema LABDA standard format.

        Args:
            path (str | Path): The path to read the Parquet file from.

        Returns:
            Subject: A new Subject instance with the data read from the Parquet file.

        Raises:
            FileNotFoundError: If no file exists at the path.
        """
        if isinstance(path, str):
            path = Path(path)

        table = pq.read_table(path)
        df = table.to_pandas()
        custom_metadata = Metadata.model_validate_json(
            table.schema.metadata["labda".encode()]
        )
        cls = cls(metadata=custom_metadata, df=df)
        cls.validate()
        log_message(cls, f"Subject imported: {path}", origin=f"{__name__}.from_parquet")

        return cls

    def validate(
        self,
        *,
        extra_columns: bool = False,
    ):
        if self.df.empty:
            raise ValueError("DataFrame is empty.")

        self.df = SCHEMA.validate(self.df)

        # Order columns as defined in Column
        records_columns = [col.value for col in Column]
        ordered_columns = [col for col in records_columns if col in self.df.columns]

        # Append extra columns that are not in Column at the end, alphabetically
        if extra_columns:
            extra = sorted(set(self.df.columns) - set(records_columns))
            ordered_columns.extend(extra)

        self.df = self.df[ordered_columns]

    def add_timedelta(
        self,
        *,
        name: str = Column.TIMEDELTA,
        overwrite: bool = False,
    ):
        """
        Adds a timedelta column to the subject's DataFrame.

        This function calculates the time difference between each row and the previous row in the
        subject's DataFrame. The calculated timedelta is added as a new column to the DataFrame.

        Args:
            name (str, optional): The name of the new timedelta column. Defaults to Column.TIMEDELTA.
            overwrite (bool, optional): Whether to overwrite the existing timedelta column if it exists. Defaults to False.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_timedelta(self.df, name=name, overwrite=overwrite)
        log_message(self, "Timedelta column added.", origin=f"{__name__}.add_timedelta")

    def add_distance(
        self,
        *,
        name: str = Column.DISTANCE,
        overwrite: bool = False,
    ):
        """
        Adds a distance column to the subject's DataFrame.

        This function calculates the distance between each row and the previous row in the
        subject's DataFrame. The calculated distance is added as a new column to the DataFrame.
        Units are based on the CRS.

        Args:
            name (str, optional): The name of the new distance column. Defaults to Column.DISTANCE.
            overwrite (bool, optional): Whether to overwrite the existing distance column if it exists. Defaults to False.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_distance(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )
        log_message(self, "Distance column added.", origin=f"{__name__}.add_distance")

    def add_speed(
        self,
        *,
        name: str = Column.SPEED,
        overwrite: bool = False,
    ):
        """
        Adds a speed column to the subject's DataFrame.

        This function calculates the speed for each row in the subject's DataFrame based on the distance and time
        difference to the previous row. The calculated speed is added as a new column to the DataFrame.
        Units are based on the CRS. If units are in metres, the speed is converted to km/h.

        Args:
            name (str, optional): The name of the new speed column. Defaults to Column.SPEED.
            overwrite (bool, optional): Whether to overwrite the existing speed column if it exists. Defaults to False.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_speed(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )
        log_message(self, "Speed column added.", origin=f"{__name__}.add_speed")

    def add_acceleration(
        self,
        *,
        name: str = Column.ACCELERATION,
        overwrite: bool = False,
    ):
        self.df = add_acceleration(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )

    def add_direction(
        self,
        *,
        name: str = Column.DIRECTION,
        overwrite: bool = False,
    ):
        """
        Adds a direction column to the subject's DataFrame.

        This function calculates the direction of movement for each row in the
        subject's DataFrame. The calculated direction is added as a new column to the DataFrame.
        The direction value is a bearing in degrees.

        Args:
            name (str, optional): The name of the new direction column. Defaults to Column.DIRECTION.
            overwrite (bool, optional): Whether to overwrite the existing direction column if it exists. Defaults to False.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_direction(self.df, name=name, overwrite=overwrite)
        log_message(self, "Direction column added.", origin=f"{__name__}.add_direction")

    def detect_trips(
        self,
        cut_points: dict[str, Any] | None = None,
        *,
        gap_duration: timedelta,
        stop_radius: int | float,
        stop_duration: timedelta,
        window: int | None = None,
        pause_fill: str | None = None,
        activity: bool = False,
        pause_radius: int | float | None = None,
        pause_duration: timedelta | None = None,
        min_duration: timedelta | None = None,
        min_length: int | float | None = None,
        min_distance: int | float | None = None,
        max_speed: int | float | None = None,
        indoor_limit: float | None = None,
        overwrite: bool = False,
    ) -> None:
        if not self.metadata.crs:
            raise ValueError("Records object does not have a CRS defined.")

        self.df = detect_trips(
            self.df,
            crs=self.metadata.crs,
            sampling_frequency=self.metadata.sampling_frequency,
            overwrite=overwrite,
            gap_duration=gap_duration,
            stop_radius=stop_radius,
            stop_duration=stop_duration,
            pause_radius=pause_radius,
            pause_duration=pause_duration,
            min_duration=min_duration,
            min_length=min_length,
            min_distance=min_distance,
            max_speed=max_speed,
            indoor_limit=indoor_limit,
        )

        if cut_points:
            self.df = detect_transportation(
                self.df,
                self.metadata.crs,
                cut_points,
                window=window,
                pause_fill=pause_fill,
                activity=activity,
                overwrite=overwrite,
            )

        if not overwrite and self.timeline:
            raise ValueError("Timeline already exists. Set 'overwrite' to 'True'.")
        else:
            self.timeline = get_timeline(self.df, crs=self.metadata.crs)

    def detect_contexts(
        self,
        contexts: gpd.GeoDataFrame,
    ) -> None:
        self.df, contexts_dicts = detect_contexts(
            self.metadata.id, self.df, contexts, self.metadata.crs
        )
        self.contexts = [Context(**context) for context in contexts_dicts]

    def detect_activity_intensity(
        self,
        cut_points: dict[str, Any],
        *,
        overwrite: bool = False,
    ) -> None:
        self.df = detect_activity_intensity(
            self.df,
            cut_points,
            self.metadata.sampling_frequency,
            overwrite=overwrite,
        )

    def detect_wear(
        self,
        min_duration: timedelta,
        interruption_duration: timedelta,
        *,
        overwrite: bool = False,
    ) -> None:
        self.df = detect_wear(
            self.df,
            self.metadata.sampling_frequency,
            min_duration,
            interruption_duration=interruption_duration,
            overwrite=overwrite,
        )

    def upsample(
        self,
        sampling_frequency: float,
        *,
        mapper: list[dict[str, Any]] | None = None,
    ) -> None:
        """
        Upsamples the subject's data to the specified sampling frequency.

        This function upsamples the data in the DataFrame from the original sampling frequency to a new sampling frequency.
        The upsampling is done using the methods specified in the mapper for each column. If no mapper is provided, a default
        mapper is used. Columns not included in the mapper are dropped from the DataFrame.

        Args:
            sampling_frequency (float): The new sampling frequency to upsample to in seconds.
            mapper (list[dict[str, Any]], optional): A list of dictionaries that map the columns in the DataFrame to the
                methods used to upsample the data in those columns. Each dictionary should have a 'column' key that specifies
                the column and a 'method' key that specifies the method. Methods are based on the pandas resample method. If not provided, a default mapper is used.

        Returns:
            pd.DataFrame: The upsampled DataFrame.

        Raises:
            ValueError: If the new sampling frequency is less than the original sampling frequency.
        """
        self.df = upsample(
            self.metadata.id,
            self.df,
            self.metadata.sampling_frequency,
            sampling_frequency,
            mapper,
        )
        self.metadata.sampling_frequency = sampling_frequency

    def plot(self, kind: str) -> Any:
        match kind:
            case "timeline":
                if isinstance(self.timeline, pd.DataFrame):
                    df = self.timeline
                else:
                    raise ValueError("Timeline does not exist. Run 'detect_trips'.")
            case "gps":
                df = self.df
            case _:
                raise ValueError(f"Kind '{kind}' not supported.")

        return plot(df, kind, crs=self.metadata.crs)
