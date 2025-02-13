import os
import re
from collections.abc import Iterable
from datetime import datetime
from typing import override

from app.models.note_models import Note
from app.notes_reader.notes_loader_abc import NotesLoaderABC
from app.tools.auto_repr import auto_repr


@auto_repr
class MarkdownNotesLoader(NotesLoaderABC):
	def __init__(self, folder_path: str, tags: Iterable[str]) -> None:
		self.folder_path: str = folder_path
		self.tags: set[str] = set(tags)

	@override
	@property
	def folder_path(self) -> str:
		return self._folder_path

	@folder_path.setter
	def folder_path(self, folder_path: str) -> None:
		# TODO add path validation, think about Path class
		self._folder_path = folder_path

	@override
	@property
	def tags(self) -> Iterable[str]:
		return self._tags

	@tags.setter
	def tags(self, tags: Iterable[str]) -> None:
		tags_normalized = set()

		for tag in tags:
			tag_ = tag.lower().strip()
			if not tag_.startswith("#"):
				tag_ = "#" + tag_
			tags_normalized.add(tag_)

		self._tags = tags_normalized

	@staticmethod
	def find_tags(content: str) -> set[str]:
		# TODO consider function
		return set(re.findall(r"#\w+", content))

	def check_tags(self, file_tags: set[str]) -> bool:
		return any(user_tag in file_tags for user_tag in self.tags)

	def get_file_list(self) -> list[str]:
		file_list: list[str] = []

		for filename in os.listdir(self.folder_path):
			if filename.endswith(".md"):
				file_list.append(filename)
		return file_list

	@staticmethod
	def load_file(file_path: str) -> str:
		with open(file_path, "r", encoding="utf-8") as file:
			return file.read()

	@override
	def load(self) -> list[Note]:
		notes = []

		for filename in self.get_file_list():
			file_path = os.path.join(self.folder_path, filename)
			content = self.load_file(file_path)
			file_tags = self.find_tags(content)
			if self.check_tags(file_tags):
				note = Note(
					title=filename[:-3],
					content=content,
					tags=file_tags,
					updated_at=datetime.fromtimestamp(os.path.getmtime(file_path)),
				)
				notes.append(note)
		return notes

	def __str__(self) -> str:
		return f"Directory {self.folder_path}, Tags: {', '.join(self.tags)}."


