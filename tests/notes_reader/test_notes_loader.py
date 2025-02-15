import builtins
import os
from datetime import datetime
from io import StringIO

import pytest

from app.notes_reader.notes_loader import MarkdownNotesLoader


@pytest.fixture()
def notes_loader():
	return MarkdownNotesLoader("./mock", ["python", "pytest"])


@pytest.fixture(scope="session")
def folder_dir():
	# TODO: change this
	return ""


@pytest.fixture(scope="session")
def note_docker():
	return """
	    # Docker

	    Multiline Content
	    Multiline Content

	    #docker#pytest #python
	    """


@pytest.fixture(scope="session")
def note_without_tags():
	return """
	    This note has no tags

	    Multiline Content with no tags
	    Multiline Content with no tags

	    """


@pytest.fixture(scope="session")
def file_md():
	return StringIO("""
	    # Docker

	    Multiline Content
	    Multiline Content

	    #docker#pytest #python
	    """)


def test_tags_are_normalized():
	tags = ["python", "#pytest", "#python", "Python", "  docker"]

	nl = MarkdownNotesLoader(".", tags)

	assert nl.tags == {"#python", "#pytest", "#docker"}


# TODO consider to add more test cases for tags func
def test_find_tags_in_multiline_note(note_docker):
	nl = MarkdownNotesLoader(".", [])
	found_tags = nl.find_tags(note_docker)
	assert found_tags == {"#docker", "#pytest", "#python"}


def test_find_tags_in_note_without_tags(note_without_tags):
	nl = MarkdownNotesLoader(".", [])
	found_tags = nl.find_tags(note_without_tags)
	assert found_tags == set()


def test_check_tags():
	nl = MarkdownNotesLoader(".", ["python", "pytest"])
	assert nl.check_tags({"#pytest", "#docker"})


def test_check_tags_from_note_without_matching_tags():
	nl = MarkdownNotesLoader(".", ["python", "pytest"])
	assert not nl.check_tags({"#unit_tests", "#docker"})


def test_get_file_list_return_markdown_files(monkeypatch, notes_loader):
	def stub_listdir(*args):
		return ["file1.md", "file2.txt", "file3.md", "script.py"]

	monkeypatch.setattr(os, "listdir", stub_listdir)

	result = notes_loader.get_file_list()

	assert result == ["file1.md", "file3.md"]


def test_get_file_list_with_no_files(monkeypatch, notes_loader):
	def stub_listdir(*args):
		return []

	monkeypatch.setattr(os, "listdir", stub_listdir)

	with pytest.raises(FileNotFoundError):
		_ = notes_loader.get_file_list()


def test_get_file_list_with_no_files_with_md_extensions(monkeypatch, notes_loader):
	def stub_listdir(*args):
		return ["file.txt", "file.html"]

	monkeypatch.setattr(os, "listdir", stub_listdir)

	with pytest.raises(FileNotFoundError):
		_ = notes_loader.get_file_list()


def test_load_file(monkeypatch, file_md, note_docker):
	def fake_open(file, mode="r", encoding=None):
		assert mode == "r"
		assert encoding == "utf-8"
		return file_md

	monkeypatch.setattr(builtins, "open", fake_open)

	result = MarkdownNotesLoader.load_file("file1.md")
	assert result == note_docker


def test_load_file_not_utf8(monkeypatch):
	def fake_open_raise(*args, **kwargs):
		raise UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid start byte")

	monkeypatch.setattr(builtins, "open", fake_open_raise)

	with pytest.raises(UnicodeDecodeError):
		MarkdownNotesLoader.load_file("file1.md")


def test_load_file_not_found():
	nl = MarkdownNotesLoader(".", ["python", "pytest"])

	with pytest.raises(FileNotFoundError):
		nl.load_file("non_existent_file.md")


class DummyNoteLoader(MarkdownNotesLoader):
	def get_file_list(self):
		return ["note1.md"]

	def load_file(self, file):
		return """
			# Docker
		
			Multiline Content
			Multiline Content
		
			#docker#pytest #python
		"""

	def find_tags(self, content):
		return {"docker", "pytest"}

	def check_tags(self, fle_tags):
		return True


def test_load_one_note(monkeypatch):
	loader = DummyNoteLoader(".mock", ["python", "pytest"])

	fixed_timestamp = 10000000
	monkeypatch.setattr(os.path, "getmtime", lambda path: fixed_timestamp)

	notes = loader.load()
	note = notes[0]

	assert len(notes) == 1

	assert note.title == "note1"
	assert note.content == """
			# Docker
		
			Multiline Content
			Multiline Content
		
			#docker#pytest #python
		"""

	assert note.tags == {"docker", "pytest"}
	assert note.updated_at == datetime.fromtimestamp(fixed_timestamp)
