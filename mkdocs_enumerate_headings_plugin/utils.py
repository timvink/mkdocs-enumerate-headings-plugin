from typing import List

from mkdocs.utils.meta import get_data


def read_md(path: str):
    """
    Reads markdown files
    
    Similar to Mkdocs.structure.pages.Page.read_source()
    https://github.com/mkdocs/mkdocs/blob/1ad6a91e3ff04a7f61b3bf376dbca84c5169279a/mkdocs/structure/pages.py#L122

    Args:
        path (str): path to markdown file
        
    Returns:
        List[str]: list of lines
    """
    with open(path, encoding="utf-8-sig", errors="strict") as f:
        source = f.read()

    # Strip meta data from source file
    lines, meta = get_data(source)

    return lines.splitlines()


def chapter_numbers(n_chapters_per_page: List):

    # First chapter should always be 1
    # Even if there is no heading 1
    if n_chapters_per_page[0] == 0:
        n_chapters_per_page[0] = 1

    chapters = []
    for i, c in enumerate(n_chapters_per_page):
        if i == 0:
            chapters.append(min(c, 1))
        else:
            chapters.append(min(c, 1) + sum(n_chapters_per_page[:i]))
    return chapters
