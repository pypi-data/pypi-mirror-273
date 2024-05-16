import logging

import pandas as pd

from .collection import Collection
from .subject import Metadata, Subject

logger = logging.getLogger("default")


def log_merged_subjects(subject: Subject, origin: str):
    meta = subject.metadata
    n_records = len(subject.df)

    sensors = ", ".join([sensor.id for sensor in meta.sensor])

    message = f"Merged {n_records} records ({sensors})."

    logger.info(message, extra={"origin": origin, "object": meta.id})


def _check_duplicate_cols(left: Subject, right: Subject) -> None:
    duplicate_cols = set(left.df.columns) & set(right.df.columns)
    if duplicate_cols:
        message = f"Before merging, remove duplicate columns: {duplicate_cols}."
        logger.error(
            message,
            extra={
                "origin": f"{__name__}._check_duplicate_cols",
                "object": left.metadata.id,
            },
        )
        raise ValueError(message)


def _check_ids(left: Subject, right: Subject) -> str:
    if left.metadata.id != right.metadata.id:
        message = (
            f"IDs do not match (left: {left.metadata.id}, right: {right.metadata.id})."
        )
        logger.error(
            message,
            extra={
                "origin": f"{__name__}._check_ids",
                "object": f"{left.metadata.id}; {right.metadata.id}",
            },
        )
        raise ValueError(message)

    return left.metadata.id


def _check_sampling_frequency(left: Subject, right: Subject) -> float:
    if left.metadata.sampling_frequency != right.metadata.sampling_frequency:
        message = f"Sampling frequency mismatch (left: {left.metadata.sampling_frequency}s, right: {right.metadata.sampling_frequency}s)."
        logger.error(
            message,
            extra={
                "origin": f"{__name__}._check_sampling_frequency",
                "object": left.metadata.id,
            },
        )
        raise ValueError(message)

    return left.metadata.sampling_frequency


def _check_timezones(left: Subject, right: Subject) -> str | None:
    if (
        (left.metadata.timezone)
        and (right.metadata.timezone)
        and left.metadata.timezone != right.metadata.timezone
    ):
        message = f"Timezone mismatch (left: {left.metadata.timezone}, right: {right.metadata.timezone})."
        logger.error(
            message,
            extra={
                "origin": f"{__name__}._check_timezones",
                "object": left.metadata.id,
            },
        )
        raise ValueError(message)

    return left.metadata.timezone or right.metadata.timezone


def _check_crs(left: Subject, right: Subject) -> str | None:
    if (
        (left.metadata.crs)
        and (right.metadata.crs)
        and left.metadata.crs != right.metadata.crs
    ):
        message = (
            f"CRS mismatch (left: {left.metadata.crs}, right: {right.metadata.crs})."
        )
        logger.error(
            message,
            extra={
                "origin": f"{__name__}._check_crs",
                "object": left.metadata.id,
            },
        )
        raise ValueError(message)

    return left.metadata.crs or right.metadata.crs


def _get_subjects(collection: Collection) -> list[str]:
    return [subject.metadata.id for subject in collection.subjects]


def merge_subjects(
    left: Subject, right: Subject, how: str = "inner", **kwargs
) -> Subject:
    """
    This function implements a user-defined merging strategy for two sensor data sets (subjects).
    Prior to merging, it performs data integrity checks by comparing IDs, sampling frequencies, time zones, and coordinate reference systems.
    Upon successful merging, a Subject object is returned, encapsulating the combined data and sensor metadata.

    Args:
        left (Subject): The first subject to merge.
        right (Subject): The second subject to merge.
        how (str, optional): The method of merge. Defaults to 'inner'. See [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) for more information.
        **kwargs: Arbitrary keyword arguments. See [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) for more information.

    Returns:
        Subject: The merged subject.

    Raises:
        ValueError: If the subjects are not instances of the Subject class.
        ValueError: If the subjects have mismatched IDs, sampling frequencies, timezones, or CRS.
    """
    # TODO: Log not overlapping rows.
    if not isinstance(left, Subject) and not isinstance(right, Subject):
        message = f"Unsupported types: {type(left)} and {type(right)}"
        logger.error(
            message,
            extra={
                "origin": f"{__name__}.merge_subjects",
                "object": None,
            },
        )
        raise ValueError(message)

    id = _check_ids(left, right)
    sf = _check_sampling_frequency(left, right)
    tz = _check_timezones(left, right)
    crs = _check_crs(left, right)

    metadata = Metadata(
        id=id,
        sensor=left.metadata.sensor + right.metadata.sensor,
        sampling_frequency=sf,
        timezone=tz,
        crs=crs,
    )

    # FIXME: Add suffixes to columns, even if not duplicated
    if not kwargs.get("suffixes"):
        _check_duplicate_cols(left, right)
    merged = pd.merge(
        left.df,
        right.df,
        left_index=True,
        right_index=True,
        how=how,  # type: ignore
        **kwargs,
    )

    subject = Subject(metadata=metadata, df=merged)
    log_merged_subjects(subject, origin=f"{__name__}.merge_subjects")

    return subject


def merge_collections(
    left: Collection,
    right: Collection,
    id: str | None = None,
    *,
    how: str = "inner",
    # keep: bool = False,
    **kwargs,
) -> Collection:
    origin = f"{__name__}.merge_collections"

    if not isinstance(left, Collection) and not isinstance(right, Collection):
        message = f"Unsupported types: {type(left)} and {type(right)}"
        logger.error(
            message,
            extra={
                "origin": origin,
                "object": None,
            },
        )
        raise ValueError(message)

    left_ids = _get_subjects(left)
    right_ids = _get_subjects(right)
    subjects = set(left_ids + right_ids)

    collection = Collection(id=id)

    for subject in subjects:
        try:
            left_subject = left.get_subject(subject)
        except Exception:
            left_subject = None

        try:
            right_subject = right.get_subject(subject)
        except Exception:
            right_subject = None

        if left_subject and right_subject:
            merged_subject = merge_subjects(
                left_subject, right_subject, how=how, **kwargs
            )

            if not merged_subject.df.empty:
                collection.add_subject(merged_subject)
            else:
                logger.warning(
                    "Merged subject is empty and will be dropped.",
                    extra={"origin": origin, "object": left_subject.metadata.id},
                )

        else:
            subject_id = (
                left_subject.metadata.id if left_subject else right_subject.metadata.id  # type: ignore
            )  # It's not possible to have both None, so one of them be always instance of Subject.

            logger.warning(
                f"Subject {subject_id} not found in both collections, therefore it will be dropped.",
                extra={
                    "origin": origin,
                    "object": subject_id,
                },
            )

            # FIXME: Fix, it is not working
            # FIXME: Suffix to check if exists
            # FIXME: Native pd.merge function adds suffixes to columns with the same name otherwise not (no suffixes and we don't know the origin of the column)
            # TODO: This could be reworked, maybe not needed to do KEEP, just outer join.
            # TODO: Maybe completely remove the keep argument.

            # if keep:
            #     if left_subject:
            #         # suffix = kwargs.get("suffixes")
            #         # if suffix:
            #         #     left_subject.df = left_subject.df.add_suffix(suffix[0])
            #         collection.add_subject(left_subject)
            #     elif right_subject:
            #         # suffix = kwargs.get("suffixes")
            #         # if suffix:
            #         #     right_subject.df = right_subject.df.add_suffix(suffix[1])
            #         collection.add_subject(right_subject)

    logger.info(
        f"From {len(subjects)} subjects, {len(collection.subjects)} were merged.",
        extra={"origin": origin, "object": collection.id},
    )

    return collection
