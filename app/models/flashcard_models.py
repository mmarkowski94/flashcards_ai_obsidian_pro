from dataclasses import dataclass
from enum import Enum


class DifficultyEnum(Enum):
	easy = "easy"
	medium = "medium"
	hard = "hard"


class NonEmptyString(str):
	def __new__(cls, value) -> str:
		if not value.strip():
			raise ValueError("String cannot be empty")
		return super().__new__(cls, value)


@dataclass(frozen=True, kw_only=True, slots=True)
class FlashCard:
	difficulty_level: DifficultyEnum
	tags: set[NonEmptyString]
	front_site: NonEmptyString
	back_site: NonEmptyString
	origin: NonEmptyString
