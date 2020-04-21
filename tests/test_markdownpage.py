import pytest
from mkdocs_enumerate_headings_plugin.markdown_page import MarkdownPage


@pytest.fixture
def simple_page():
    p = open("tests/fixtures/pages/simple.md").readlines()
    return [line.rstrip("\n") for line in p]


def simple_enumerated_page():
    p = open("tests/fixtures/pages/simple-enumerated.md").readlines()
    return [line.rstrip("\n") for line in p]


@pytest.fixture
def page_with_codeblock():
    p = open("tests/fixtures/pages/with_codeblock.md").readlines()
    return [line.rstrip("\n") for line in p]


def test_page(simple_page):
    page = MarkdownPage(simple_page)
    assert [int(l.get_is_heading()) for l in page.lines] == [
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
    ]


def test_section_numbering(simple_page):
    page = MarkdownPage(simple_page)
    assert page.lines[0].section_numbering == [1, 0, 0, 0, 0, 0]
    assert page.lines[4].section_numbering == [1, 1, 0, 0, 0, 0]


def test_page_headings(page_with_codeblock):
    page = MarkdownPage(page_with_codeblock)
    assert [int(l.get_is_heading()) for l in page.lines] == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
    ]


def test_enumeration(simple_page):
    page = MarkdownPage(simple_page)
    page_enumerated = simple_enumerated_page()
    assert page.enumerate_headings() == page_enumerated
