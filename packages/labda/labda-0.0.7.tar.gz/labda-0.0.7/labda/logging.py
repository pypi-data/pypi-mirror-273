import logging
import sys

import colorlog

from .structure.subject import Subject


def log_successfully_parsed_subject(subject: Subject, origin: str, source: str):
    logger = logging.getLogger("default")
    meta = subject.metadata

    sampling_frequency = (
        f"SF: {meta.sampling_frequency}s" if meta.sampling_frequency else ""
    )  # type: ignore
    timezone = f", TZ: {meta.timezone}" if meta.timezone else ""
    crs = f", CRS: {meta.crs}" if meta.crs else ""
    n_records = len(subject.df)

    vendor = meta.sensor[0].vendor if meta.sensor else ""

    message = f"Parsed {n_records} records ({sampling_frequency}{timezone}{crs}) from: {source} ({vendor})."

    logger.info(message, extra={"origin": origin, "object": meta.id})


def get_logger():
    logger = logging.getLogger("default")
    fmt = colorlog.ColoredFormatter(
        "%(white)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(white)s%(origin)s%(reset)s | %(blue)s%(object)s%(reset)s | %(log_color)s%(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stdout = colorlog.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(fmt)

    logger.addHandler(stdout)
    logger.setLevel(logging.INFO)

    return logger
