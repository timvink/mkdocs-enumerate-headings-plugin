from mkdocs_add_number_plugin.utils import flatten


def test_flatten():

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
