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

    testproject_path = output_path / 'testproject'
    
    # Create empty 'testproject' folder    
    if os.path.exists(testproject_path):
        logging.warning("""This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once""")
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'        
    shutil.copytree('tests/dummy_project/docs', testproject_path / 'docs')
    shutil.copyfile(mkdocs_yml_path, testproject_path / 'mkdocs.yml')
    
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
    os.chdir(testproject_path)
    
    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise

def test_basic_build(tmp_path):
    
    tmp_proj = setup_clean_mkdocs_folder('tests/dummy_project/mkdocs.yml', tmp_path)
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"
    
    index_file = tmp_proj / 'site/index.html'
    assert index_file.exists(),  f"{index_file} does not exist"
    
    # index.html is always first page, so should have chapter 1
    contents = index_file.read_text()
    assert re.search(r"1. Test page", contents)
    assert re.search(r"1.2.1 sub heading three deep", contents)
    
    # 'a_third_page.md` is first alphabetical, but second due to index.md
    third_page = tmp_proj / 'site/a_third_page.html'
    contents = third_page.read_text()
    assert re.search(r"2. A Third page", contents)
   
    # 'second_page' is fourth in alphabetical order 
    second_page = tmp_proj / 'site/second_page.html'
    contents = second_page.read_text()
    assert re.search(r"4. Second Test page", contents) 
    
def test_build_with_nav(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder('tests/dummy_project/mkdocs_with_nav.yml', tmp_path)
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"
    
    index_file = tmp_proj / 'site/index.html'
    assert index_file.exists(),  f"{index_file} does not exist"
    
    # index.html is always first page, so should have chapter 1
    contents = index_file.read_text()
    assert re.search(r"1. Test page", contents)
    assert re.search(r"1.2.1 sub heading three deep", contents)
    
    # 'a_third_page.md` is .. you guessed it.. fourth :)
    third_page = tmp_proj / 'site/a_third_page.html'
    contents = third_page.read_text()
    assert re.search(r"4. A Third page", contents)
   
    # 'second_page' is 2+1 = third.
    second_page = tmp_proj / 'site/second_page.html'
    contents = second_page.read_text()
    assert re.search(r"3. Second Test page", contents)
    
def test_build_with_excludes(tmp_path):
    """
    currently not working, 
    see https://github.com/ignorantshr/mkdocs-add-number-plugin/issues/8
    
    """

    tmp_proj = setup_clean_mkdocs_folder('tests/dummy_project/mkdocs_with_excludes.yml', tmp_path)
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"
    
    index_file = tmp_proj / 'site/index.html'
    assert index_file.exists(),  f"{index_file} does not exist"

    # DISABLED for now.
    # second_page = tmp_proj / 'site/second_page.html'
    # assert not second_page.exists(),  f"{second_page} should have been excluded"
    
def test_build_with_strict(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder('tests/dummy_project/mkdocs_with_strict.yml', tmp_path)
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"
    
    index_file = tmp_proj / 'site/index.html'
    assert index_file.exists(),  f"{index_file} does not exist"