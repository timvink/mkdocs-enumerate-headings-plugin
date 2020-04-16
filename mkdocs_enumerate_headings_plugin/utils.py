def flatten(nav):
    """
    Flattens mkdocs navigation to list of markdown files 
    
    See tests/test_flatten.py for example
    
    Args:
        nav (list): nested list with dicts
    
    Returns:
        list: list of markdown pages
    """
    pages = []
    for i in nav:
        item = list(i.values())[0]
        if type(item) == list:
            pages += flatten(item)
        else:
            pages.append(item)
    return pages
