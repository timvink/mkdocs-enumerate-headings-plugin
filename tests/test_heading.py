import re
import pytest

from bs4 import BeautifulSoup

from mkdocs_enumerate_headings_plugin.heading import Heading


def get_heading_class(content: str):
    soup = BeautifulSoup(content, "html.parser")
    heading_tags = soup.find_all(re.compile("^h[1-6]$"))
    return Heading(heading_tags[0], soup)


def test_heading_depth():
    assert get_heading_class("<h1>heading</h1>").depth == 1
    assert get_heading_class("<h6>heading</h6>").depth == 6


def test_enumeration():

    heading = get_heading_class("<h1>heading</h1>")
    heading.section_numbering = [1, 0, 0, 0, 0, 0]
    heading.enumerate()
    assert str(heading.heading) == "<h1>1. heading</h1>"

    heading = get_heading_class("<h2>API</h2>")
    heading.section_numbering = [2, 1, 0, 0, 0, 0]
    heading.enumerate()
    assert str(heading.heading) == "<h2>2.1 API</h2>"

    heading = get_heading_class("<h2>API</h2>")
    heading.section_numbering = [0, 1, 0, 0, 0, 0]
    heading.enumerate()
    assert str(heading.heading) == "<h2>0.1 API</h2>"

    heading = get_heading_class("<h2>dummy test</h2>")
    heading.section_numbering = [2, 0, 1, 0, 0, 0]
    heading.enumerate()
    assert str(heading.heading) == "<h2>2.0.1 dummy test</h2>"

    heading = get_heading_class("<h2>_dummy_test</h2>")
    heading.section_numbering = [2, 0, 1, 0, 0, 0]
    heading.enumerate()
    assert str(heading.heading) == "<h2>2.0.1 _dummy_test</h2>"


def test_span_addition():

    heading = get_heading_class("<h2>_dummy_test</h2>")
    heading.section_numbering = [2, 0, 1, 0, 0, 0]
    heading.enumerate(add_span_element=True)
    assert (
        str(heading.heading)
        == '<h2><span class="enumerate-headings-plugin enumerate-heading-plugin">2.0.1</span> _dummy_test</h2>'
    )


def test_reference_error1():
    heading = get_heading_class("<h1>dummy test</h1>")
    with pytest.raises(AssertionError):
        heading.enumerate()


def test_section_number_string_start_level():
    heading = get_heading_class("<h2>API</h2>")
    heading.section_numbering = [1, 1, 0, 0, 0, 0]
    assert heading.section_number_string(start_level=2) == "1."

    heading.section_numbering = [1, 2, 1, 0, 0, 0]
    assert heading.section_number_string(start_level=2) == "2.1"

    heading = get_heading_class("<h2>API</h2>")
    heading.section_numbering = [2, 1, 0, 0, 0, 0]
    heading.enumerate(start_level=2)
    assert str(heading.heading) == "<h2>1. API</h2>"


def test_section_numbering_not_mutated_by_section_number_string():
    heading = get_heading_class("<h1>x</h1>")
    heading.section_numbering = [1, 2, 3, 0, 0, 0]
    before = list(heading.section_numbering)
    heading.section_number_string(start_level=1)
    assert heading.section_numbering == before
