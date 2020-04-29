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
