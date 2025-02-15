from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=False, kw_only=True, slots=True)
class Note:
    title: str
    content: str
    tags: set[str]
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError(f"Title must be a non-empty string.")

        if not self.content:
            raise ValueError(f"Content must be a non-empty string.")

        self.tags = {tag.strip().lower() for tag in self.tags if tag.strip()}
        if not self.tags:
            raise ValueError(f"Tags: {self.tags!r} must be a non-empty set.")
