"""
Modules test that builds with different setting succeed.

Note that pytest offers a `tmp_path`. 
You can reproduce locally with

```python
%load_ext autoreload
%autoreload 2
import os
import tempfile
import shutil
from pathlib import Path
tmp_path = Path(tempfile.gettempdir()) / 'pytest-table-builder'
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
os.mkdir(tmp_path)
```
"""

import re
import os
import shutil
import logging
import pytest
import sys
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """

    testproject_path = output_path / "testproject"

    # Create empty 'testproject' folder
    if os.path.exists(str(testproject_path)):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(str(testproject_path))

    # Copy correct mkdocs.yml file and our test 'docs/'
    yml_dir = os.path.dirname(mkdocs_yml_path)
    shutil.copytree(yml_dir, str(testproject_path))
    shutil.copyfile(mkdocs_yml_path, str(testproject_path / "mkdocs.yml"))

    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """

    cwd = os.getcwd()
    os.chdir(str(testproject_path))

    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise


def check_build(tmp_path, project_mkdocs, exit_code=0):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/%s" % project_mkdocs, tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == exit_code, result
    return tmp_proj


def check_text_in_page(tmp_proj, page_path, text):
    page = tmp_proj / "site" / page_path
    assert page.exists(), "%s does not exist" % page_path
    contents = page.read_text(encoding="utf-8")
    assert re.search(text, contents)


#### Tests ####


def test_simple_build(tmp_path):
    check_build(tmp_path, "simple/mkdocs.yml", exit_code=1)


def test_simple_notstrict(tmp_path):

    tmp_proj = check_build(tmp_path, "simple/mkdocs_notstrict.yml")

    check_text_in_page(tmp_proj, "index.html", r"1.</span> Homepage")
    check_text_in_page(tmp_proj, "index.html", r"1.2.1</span> sub heading three deep")

    # 'a_third_page.md` is first alphabetical, but second due to index.md
    check_text_in_page(tmp_proj, "a_third_page.html", r"2.</span> Normal")

    # A page with zero h1 but has headings should be treated as a chapter as well (in non strict mode)
    check_text_in_page(tmp_proj, "zero_h1.html", r"5.0.0.1</span> Zero h1")


def test_simple_with_nav(tmp_path):

    tmp_proj = check_build(tmp_path, "simple/mkdocs_with_nav.yml")

    # index.html is always first page, so should have chapter 1
    check_text_in_page(tmp_proj, "index.html", r"1.</span> Homepage")
    check_text_in_page(tmp_proj, "index.html", r"1.2.1</span> sub heading three deep")

    # 'second_page' is 2+1 = third.
    check_text_in_page(tmp_proj, "two_h1.html", r"2.</span> Two h1")
    check_text_in_page(tmp_proj, "two_h1.html", r"3.</span> Second level 1 heading")

    # 'a_third_page.md`
    check_text_in_page(tmp_proj, "a_third_page.html", r"4.</span> Normal")


class TestTOCDepth:
    def test_depth_1(self, tmp_path):

        tmp_proj = check_build(tmp_path, "simple/mkdocs_notstrict_depth1.yml")
        check_text_in_page(
            tmp_proj, "index.html", r"""href="#homepage">1. Homepage</a>"""
        )
        check_text_in_page(
            tmp_proj, "index.html", r"""href="#another-heading">another heading</a>"""
        )

    def test_depth_7(self, tmp_path):
        check_build(tmp_path, "simple/mkdocs_notstrict_depth7.yml", 1)


def test_simple_no_h1_start(tmp_path):

    # non-strict build
    tmp_proj = check_build(tmp_path, "simple_no_h1_start/mkdocs.yml")
    check_text_in_page(tmp_proj, "index.html", r"1.</span> Homepage")
    check_text_in_page(tmp_proj, "a.html", r"2.1</span> l2 before h1")
    check_text_in_page(tmp_proj, "a.html", r"2.1.1</span> l3 before h1")
    check_text_in_page(tmp_proj, "a.html", r"2.</span> page a")
    check_text_in_page(tmp_proj, "a.html", r"2.1</span> l2 after h1")
    check_text_in_page(tmp_proj, "a.html", r"2.1.1</span> l3 after h1")


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Don't test windows, as monorepo doesnt run their unit test on windows either",
)
class TestMonorepoPlugin:
    def test_compatibility_monorepo_plugin1(self, tmp_path):
        tmp_proj = setup_clean_mkdocs_folder(
            "tests/fixtures/projects/monorepo_ok/mkdocs.yml", tmp_path
        )
        result = build_docs_setup(tmp_proj)
        assert result.exit_code == 0, "'mkdocs build' command failed"

        page = tmp_proj / "site/test/index.html"
        contents = page.read_text(encoding="utf-8")
        assert re.search(r"2.</span> Hello world!", contents)

    def test_compatibility_monorepo_plugin2(self, tmp_path):
        tmp_proj = setup_clean_mkdocs_folder(
            "tests/fixtures/projects/monorepo_ok/mkdocs_enum_first.yml", tmp_path
        )
        result = build_docs_setup(tmp_proj)
        assert result.exit_code == 0, "'mkdocs build' command failed"

        page = tmp_proj / "site/test/index.html"
        contents = page.read_text(encoding="utf-8")
        assert re.search(r"2.</span> Hello world!", contents)

    def test_compatibility_monorepo_plugin3(self, tmp_path):
        tmp_proj = setup_clean_mkdocs_folder(
            "tests/fixtures/projects/monorepo_sample_docs/mkdocs.yml", tmp_path
        )
        result = build_docs_setup(tmp_proj)
        assert result.exit_code == 0, "'mkdocs build' command failed"

        page = tmp_proj / "site/versions/v2/changelog/index.html"
        contents = page.read_text(encoding="utf-8")
        assert re.search(r"7.</span> Changelog", contents)

    def test_compatibility_monorepo_plugin4(self, tmp_path):
        tmp_proj = setup_clean_mkdocs_folder(
            "tests/fixtures/projects/monorepo_sample_docs/mkdocs_enum_first.yml",
            tmp_path,
        )
        result = build_docs_setup(tmp_proj)
        assert result.exit_code == 0, "'mkdocs build' command failed"

        page = tmp_proj / "site/versions/v2/changelog/index.html"
        contents = page.read_text(encoding="utf-8")
        assert re.search(r"7.</span> Changelog", contents)


def test_compatibility_awesomepages_plugin1(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/awesome_pages/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page = tmp_proj / "site/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"5.</span> Homepage", contents)

    page = tmp_proj / "site/section2/page4/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"1.</span> Page 4", contents)


def test_compatibility_awesomepages_plugin2(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/awesome_pages/mkdocs_enum_first.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page = tmp_proj / "site/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"5.</span> Homepage", contents)

    page = tmp_proj / "site/section2/page4/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"1.</span> Page 4", contents)


def test_compatibility_material(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/material/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page = tmp_proj / "site/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"1.</span> Heading 1", contents)

    page = tmp_proj / "site/01.Introduction/Empty-File/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"2.</span> Empty File", contents)

    page = tmp_proj / "site/01.Introduction/Missing-Heading-1/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"3.</span> Missing Heading 1", contents)

    page = tmp_proj / "site/01.Introduction/My-Page-Name/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"4.</span> YAML Title", contents)


def test_compatibility_pymarkx_snippets1(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/pymarkx_snippet/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page = tmp_proj / "site/index.html"
    contents = page.read_text(encoding="utf-8")
    assert re.search(r"1.</span> Homepage", contents)

    page = tmp_proj / "site/snippet.html"
    contents = page.read_text(encoding="utf-8")
    # First check if content was inserted
    assert re.search(r"Extra page</h1>", contents)
    # Then check if enumeration was done
    assert re.search(r"3.</span> Extra page", contents)


def test_compatibility_pymarkx_snippets2(tmp_path):

    tmp_proj = check_build(tmp_path, "pymarkx_snippet/mkdocs_with_nav.yml")
    check_text_in_page(tmp_proj, "index.html", r"1.</span> Homepage")
    # First check if content was inserted
    check_text_in_page(tmp_proj, "snippet.html", r"Extra page</h1>")
    # Then check if enumeration was done
    check_text_in_page(tmp_proj, "snippet.html", r"2.</span> Extra page")


def test_simple_with_empty_pages(tmp_path):
    tmp_proj = check_build(tmp_path, "simple_with_empty_pages/mkdocs.yml")

    check_text_in_page(tmp_proj, "b.html", r"2.</span> heading")
    check_text_in_page(tmp_proj, "d.html", r"4.</span> heading")
    check_text_in_page(tmp_proj, "f.html", r"6.</span> heading")
