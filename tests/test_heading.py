import pytest
import markdown

# from mkdocs_enumerate_headings_plugin.heading import Heading


@pytest.fixture
def simple_page():
    lines = open("tests/fixtures/pages/simple.md").readlines()
    md = markdown.Markdown()
    html = md.convert(lines)
    return html


# from bs4 import BeautifulSoup
# import bs4


# def test_heading_depth():
#     with pytest.raises(AssertionError):
#         Heading("no heading").heading_depth() == 0

#     Heading("<h1>heading 1</h1>").depth == 1
#     Heading("<h2>heading 2</h2>").depth == 2
#     Heading("<h3>heading 3</h3>").depth == 3
#     Heading("<h4>heading 4</h4>").depth == 4
#     Heading("<h5>heading 5</h5>").depth == 5
#     Heading("<h6>heading 6</h6>").depth == 6

#     with pytest.raises(AssertionError):
#         Heading("<h7>heading 7</h7>").depth == 7


# def test_section_number_string():

#     line = Line("<h1>dummy test</h1>")

#     line.section_numbering = [1, 0, 0, 0, 0, 0]
#     assert line.section_number_string() == "1."
#     assert line.enumerate() == "# 1. dummy test"

#     line = Line("## API")
#     line.is_heading = True
#     line.section_numbering = [2, 1, 0, 0, 0, 0]
#     assert line.section_number_string() == "2.1"
#     assert line.enumerate() == "## 2.1 API"

#     line.section_numbering = [0, 1, 0, 0, 0, 0]
#     assert line.section_number_string() == "0.1"
#     assert line.enumerate() == "## 0.1 API"

#     line = Line("### dummy test")
#     line.is_heading = True
#     line.section_numbering = [2, 0, 1, 0, 0, 0]
#     assert line.section_number_string() == "2.0.1"
#     assert line.enumerate() == "### 2.0.1 dummy test"

#     line = Line("### _dummy_test")
#     line.is_heading = True
#     line.section_numbering = [2, 0, 1, 0, 0, 0]
#     assert line.section_number_string() == "2.0.1"
#     assert line.enumerate() == "### 2.0.1 _dummy_test"


# def test_span_addition():

#     line = Line("## dummy test")
#     line.is_heading = True

#     line.section_numbering = [2, 0, 0, 0, 0, 0]
#     assert line.section_number_string() == "2."
#     assert (
#         line.enumerate(add_span_element=True)
#         == "## <span class='enumerate-heading-plugin'>2.</span> dummy test"
#     )


# def test_reference_error1():
#     line = Line("# dummy test")
#     with pytest.raises(ReferenceError):
#         line.enumerate()


# def test_reference_error2():
#     line = Line("# dummy test")
#     with pytest.raises(ReferenceError):
#         line.get_is_heading()
