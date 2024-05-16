from enum import StrEnum

import pandera as pr


class Column(StrEnum):
    SUBJECT_ID = "subject_id"
    CONTEXT = "context"
    PRIORITY = "priority"
    START = "start"
    END = "end"
    GEOMETRY = "geometry"


SCHEMA = pr.DataFrameSchema(
    columns={
        Column.SUBJECT_ID: pr.Column(
            dtype="string",
            description="Unique ID of the dataframe (subject)",
            required=False,
            nullable=True,
        ),
        Column.CONTEXT: pr.Column(
            dtype="string",
            description="Name of the context",
        ),
        Column.PRIORITY: pr.Column(
            dtype="Int64",
            description="Priority of the context",
            required=False,
            nullable=True,
        ),
        Column.START: pr.Column(
            dtype="datetime64[ns]",
            description="Start time of the context",
            required=False,
            nullable=True,
        ),
        Column.END: pr.Column(
            dtype="datetime64[ns]",
            description="End time of the context",
            required=False,
            nullable=True,
        ),
        Column.GEOMETRY: pr.Column(
            dtype="geometry",
            description="Geometry of the context",
            required=False,
            nullable=True,
        ),
    },
    coerce=True,
)
