from io import StringIO

import pytest

from app.notes_reader.notes_loader import MarkdownNotesLoader


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
def file_md():
	return StringIO("""
    # Docker

    Multiline Content
    Multiline Content

    #docker#pytest #python
    """)


def test_tags_are_normalized():
	tags = ["python", "#pytest", "#python", "Python", "  docker"]

	nl = MarkdownNotesLoader('.', tags)

	assert nl.tags == {'#python', '#pytest', '#docker'}


# TODO consider to add more test cases for tags func
def test_find_tags_in_multiline_note(note_docker):
	nl = MarkdownNotesLoader('.', [])
	found_tags = nl.find_tags(note_docker)
	assert found_tags == {"#docker", "#pytest", "#python"}


def test_check_tags():
	nl = MarkdownNotesLoader('.', ["python", "pytest"])
	assert nl.check_tags({"#pytest", "#docker"})


def test_check_tags_from_note_without_matching_tags():
	nl = MarkdownNotesLoader('.', ["python", "pytest"])
	assert not nl.check_tags({"#unit_tests", "#docker"})
