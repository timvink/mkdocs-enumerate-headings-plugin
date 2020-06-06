# import pytest
# from mkdocs_enumerate_headings_plugin.markdown_page import MarkdownPage
# from mkdocs_enumerate_headings_plugin.utils import read_md


# @pytest.fixture
# def simple_page():
#     return read_md("tests/fixtures/pages/simple.md")


# def simple_enumerated_page():
#     return read_md("tests/fixtures/pages/simple-enumerated.md")


# @pytest.fixture
# def page_with_codeblock():
#     return read_md("tests/fixtures/pages/with_codeblock.md")


# def test_page(simple_page):
#     page = MarkdownPage(simple_page)
#     assert [int(l.get_is_heading()) for l in page.lines] == [
#         1,
#         0,
#         0,
#         0,
#         1,
#         0,
#         0,
#         0,
#         1,
#         0,
#         0,
#         0,
#         0,
#         1,
#         0,
#         0,
#         0,
#         1,
#         0,
#         1,
#     ]


# def test_section_numbering(simple_page):
#     page = MarkdownPage(simple_page)
#     assert page.lines[0].section_numbering == [1, 0, 0, 0, 0, 0]
#     assert page.lines[4].section_numbering == [1, 1, 0, 0, 0, 0]


# def test_page_headings(page_with_codeblock):
#     page = MarkdownPage(page_with_codeblock)
#     assert [int(l.get_is_heading()) for l in page.lines] == [
#         1,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         1,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         1,
#         0,
#         1,
#     ]


# @pytest.mark.parametrize(
#     "pagename,valid",
#     [
#         ("simple", True),
#         ("skip-heading-1", True),
#         ("multiple-heading-1", True),
#         ("skip-heading-1", True),
#         ("with_codeblock", True),
#         ("edge-cases", False),
#         ("missing-heading-1", False),
#         ("no-headings", True),
#         ("empty", True),
#         ("only_yaml", True),
#     ],
# )
# def test_enumeration(pagename, valid):
#     page = read_md("tests/fixtures/pages/%s.md" % pagename)
#     page = MarkdownPage(page)
#     assert page.validate() == valid
#     page_enumerated = read_md("tests/fixtures/pages/%s-enumerated.md" % pagename)
#     assert page.enumerate_headings(add_span_element=False) == page_enumerated
