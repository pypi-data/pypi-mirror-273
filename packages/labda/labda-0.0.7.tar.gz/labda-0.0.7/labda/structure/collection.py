import logging
import secrets
from functools import partial
from pathlib import Path
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field

from ..parallel import parallel_processing
from .subject import Subject

logger = logging.getLogger("default")


def _to_parquet_with_path(subject, path, overwrite):
    subject_path = path / f"{subject.metadata.id}.parquet"
    return Subject.to_parquet(subject, path=subject_path, overwrite=overwrite)


class Collection(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: secrets.token_hex(4))
    subjects: list[Subject] = Field(default_factory=list)

    def __repr__(self):
        subjects_repr = ", ".join([p.metadata.id for p in self.subjects])  # type: ignore
        return f"Collection(id={self.id}, subjects=[{subjects_repr}])"

    def add_subject(self, subject: Subject):
        subjects_ids = [s.metadata.id for s in self.subjects]

        if subject.metadata.id in subjects_ids:
            raise ValueError(
                f"Subject with id '{subject.metadata.id}' already exists in collection."
            )

        subject.collection = self.id  # type: ignore
        self.subjects.append(subject)  # type: ignore

    def get_subject(self, id: str) -> Subject:
        for subject in self.subjects:
            if subject.metadata.id == id:
                return subject
        raise ValueError(f"Subject with id '{id}' not found.")

    @classmethod
    def from_folder(cls, path: str | Path, id: str | None = None) -> "Collection":
        if isinstance(path, str):
            path = Path(path)

        files = list(path.glob("*.parquet"))

        if not files:
            raise ValueError(f"No parquet files found in '{path}'.")

        subjects = [Subject.from_parquet(file) for file in files]
        return cls(id=id, subjects=subjects)

    def to_folder(
        self,
        path: str | Path,
        *,
        parallel: bool = True,
        n_cores: int | str = "max",
        overwrite: bool = False,
    ):
        if isinstance(path, str):
            path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        if not path.is_dir():
            raise ValueError(f"'{path}' is not a valid directory.")

        if parallel:
            self.subjects = parallel_processing(
                partial(_to_parquet_with_path, path=path, overwrite=overwrite),
                self.subjects,
                n_cores,
            )
        else:
            for subject in self.subjects:
                subject.to_parquet(
                    path / f"{subject.metadata.id}.parquet", overwrite=overwrite
                )

    def detect_trips(
        self,
        *,
        parallel: bool = True,
        n_cores: int | str = "max",
        **kwargs,
    ):
        if parallel:
            self.subjects = parallel_processing(
                Subject.detect_trips,
                self.subjects,
                n_cores,
                **kwargs,
            )
        else:
            for subject in self.subjects:
                subject.detect_trips(**kwargs)

    def detect_activity_intensity(
        self,
        *,
        parallel: bool = True,
        n_cores: int | str = "max",
        **kwargs,
    ) -> None:
        if parallel:
            self.subjects = parallel_processing(
                Subject.detect_activity_intensity,
                self.subjects,
                n_cores,
                **kwargs,
            )
        else:
            for subject in self.subjects:
                subject.detect_activity_intensity(**kwargs)

    def _check_atribute_consistency(self, metadata: pd.DataFrame, attribute):
        unique = metadata[attribute].unique()

        if len(unique) != 1:
            origin = f"{self.__class__.__name__}.check_consistency[{attribute}]"
            logger.error(
                f"{attribute}: {unique}",
                extra={"origin": origin, "object": self.id},
            )

            return True

    def consistency(self):
        # TODO: Add also check columns consistency
        attributes = ["sampling_frequency", "crs", "timezone"]

        metadata = pd.DataFrame(
            [
                s.metadata.model_dump(include=set(["id"] + attributes))
                for s in self.subjects
            ]
        )
        metadata.set_index("id", inplace=True)

        consistency_results = [
            self._check_atribute_consistency(metadata, attr) for attr in attributes
        ]

        origin = f"{__name__}.check_consistency"
        extra = {"origin": origin, "object": self.id}

        if any(consistency_results):
            message = ""
            logger.error(message, extra=extra)
        else:
            logger.info(
                "Consistency check finished.",
                extra=extra,
            )
