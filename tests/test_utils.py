from mkdocs_enumerate_headings_plugin.utils import chapter_numbers


def test_chapter_numbers():

    assert chapter_numbers([1, 1, 1]) == [1, 2, 3]
    assert chapter_numbers([1, 2, 1]) == [1, 2, 4]
    assert chapter_numbers([2, 2, 2]) == [1, 3, 5]

    # In non-strict mode, we can also have pages with no heading at all
    # We'll always start with a chapter 1 though
    assert chapter_numbers([1, 0, 0]) == [1, 1, 1]
    assert chapter_numbers([0, 0, 0]) == [1, 1, 1]
    assert chapter_numbers([0, 1, 0]) == [1, 2, 2]
    assert chapter_numbers([0, 1, 2]) == [1, 2, 3]
