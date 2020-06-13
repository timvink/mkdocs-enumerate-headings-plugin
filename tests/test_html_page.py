import pytest
import markdown
import logging
from mkdocs_enumerate_headings_plugin.html_page import HTMLPage
from bs4 import BeautifulSoup


def load_page(path="tests/fixtures/pages/simple.md"):
    try:
        with open(path, "r", encoding="utf-8-sig", errors="strict") as f:
            source = f.read()
    except OSError:
        logging.error("File not found: {}".format(path))
        raise
    except ValueError:
        logging.error("Encoding error reading file: {}".format(path))
        raise

    # lines = open("tests/fixtures/pages/simple.md").readlines()
    md = markdown.Markdown(extensions=["extra"])
    html = md.convert(source)
    return html


class dummyPage:
    """
    In order to mock the mkdocs.structure.Page class
    """

    def __init__(self, filename):
        self.filename = filename

    @property
    def file(self):
        return self

    @property
    def src_path(self):
        return self.filename


@pytest.mark.parametrize(
    "pagename,valid",
    [
        ("simple", True),
        ("skip-heading-1", True),
        ("multiple-heading-1", True),
        ("skip-heading-1", True),
        ("with_codeblock", True),
        ("edge-cases", False),
        ("missing-heading-1", False),
        ("no-headings", True),
        ("empty", True),
        ("only_yaml", True),
    ],
)
def test_enumeration(pagename, valid, caplog):
    caplog.set_level(logging.WARNING)

    page = load_page("tests/fixtures/pages/%s.md" % pagename)
    html_page = HTMLPage(page)

    # Validation
    page = dummyPage(pagename)
    if valid:
        assert html_page.validate(page, {"strict": True})
    else:
        # Raises error on strict mode
        with pytest.raises(AssertionError):
            html_page.validate(page, {"strict": True})
        # Raises warning on non-strict mode
        with caplog.at_level(logging.WARNING):
            html_page.validate(page, {"strict": False})
        assert len(caplog.records) > 0
        for record in caplog.records:
            assert record.levelname == "WARNING"

    # Correct enumeration
    html_page.enumerate_headings(add_span_element=False)
    reference_html_page = load_page("tests/fixtures/pages/%s-enumerated.md" % pagename)
    soup = BeautifulSoup(reference_html_page, "html.parser")
    assert str(html_page) == str(soup)
