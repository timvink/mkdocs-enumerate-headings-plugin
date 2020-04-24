from mkdocs_enumerate_headings_plugin.utils import flatten, chapter_numbers


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


def test_flatten1():

    nav = [
        {"Home": "index.md"},
        {"Page One": "page_one.md"},
        {"Page Two": "page_two.md"},
        {"Model Class": "model_class.md"},
        {
            "TMD": [
                {"Use Case": "TMD/1_use_case.md"},
                {"Raw Data": "TMD/2_raw_data.md"},
                {"Features": "TMD/3_features.md"},
                {"Modelling": "TMD/4_modelling.md"},
                {"Limitations": "TMD/5_limitations.md"},
            ]
        },
        {
            "Review Process": [
                {"Early reflection": "review_process/early.md"},
                {"Mature reflection": "review_process/mature.md"},
                {"External reflection": "review_process/final.md"},
            ]
        },
        {"Approvals": "approvals.md"},
        {"Appendix": "appendix.md"},
        {
            "Cookbook": [
                {"Markdown demos": "cookbook/markdown_demos.md"},
                {
                    "Correlation between features": "cookbook/correlation_between_features.md"
                },
            ]
        },
    ]

    assert flatten(nav) == [
        "index.md",
        "page_one.md",
        "page_two.md",
        "model_class.md",
        "TMD/1_use_case.md",
        "TMD/2_raw_data.md",
        "TMD/3_features.md",
        "TMD/4_modelling.md",
        "TMD/5_limitations.md",
        "review_process/early.md",
        "review_process/mature.md",
        "review_process/final.md",
        "approvals.md",
        "appendix.md",
        "cookbook/markdown_demos.md",
        "cookbook/correlation_between_features.md",
    ]


def test_flatten2():
    nav = [
        {"Intro": "index.md"},
        {"Authentication": "authentication.md"},
        {
            "API": [
                {
                    "v1": [
                        {"Reference": "versions/v1/reference.md"},
                        {"Changelog": "versions/v1/changelog.md"},
                    ]
                },
                {
                    "v2": [
                        {"Migrating to v2": "versions/v2/migrating.md"},
                        {"Reference": "versions/v2/reference.md"},
                        {"Changelog": "versions/v2/changelog.md"},
                    ]
                },
            ]
        },
    ]

    assert flatten(nav) == [
        "index.md",
        "authentication.md",
        "versions/v1/reference.md",
        "versions/v1/changelog.md",
        "versions/v2/migrating.md",
        "versions/v2/reference.md",
        "versions/v2/changelog.md",
    ]
