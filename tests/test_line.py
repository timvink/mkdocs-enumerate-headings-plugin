import pytest
from mkdocs_enumerate_headings_plugin.line import Line


@pytest.fixture
def simple_page():
    return open("tests/fixtures/pages/simple.md").readlines()


def test_line(simple_page):
    lines = [Line(l).heading_depth() for l in simple_page]
    assert lines == [1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 2]


def test_heading_depth():
    Line("no heading").heading_depth() == 0
    Line("# heading 1").heading_depth() == 1
    Line("## heading 2").heading_depth() == 2
    Line("### heading 3").heading_depth() == 3
    Line("#### heading 4").heading_depth() == 4
    Line("##### heading 5").heading_depth() == 5
    Line("###### heading 6").heading_depth() == 6


def test_section_number_string():

    line = Line("# dummy test")
    line.is_heading = True

    line.section_numbering = [1, 0, 0, 0, 0, 0]
    assert line.section_number_string() == "1."
    assert line.enumerate() == "# 1. dummy test"

    line.section_numbering = [2, 1, 0, 0, 0, 0]
    assert line.section_number_string() == "2.1"
    assert line.enumerate() == "# 2.1 dummy test"

    line.section_numbering = [2, 0, 1, 0, 0, 0]
    assert line.section_number_string() == "2.0.1"
    assert line.enumerate() == "# 2.0.1 dummy test"

    line.section_numbering = [0, 1, 0, 0, 0, 0]
    assert line.section_number_string() == "0.1"
    assert line.enumerate() == "# 0.1 dummy test"


def test_reference_error1():
    line = Line("# dummy test")
    with pytest.raises(ReferenceError):
        line.enumerate()


def test_reference_error2():
    line = Line("# dummy test")
    with pytest.raises(ReferenceError):
        line.get_is_heading()
