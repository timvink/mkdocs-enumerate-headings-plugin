from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-enumerate-headings-plugin",
    version="0.4.1",
    description="MkDocs Plugin to enumerate the headings (h1-h6) across site pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs enumerate headings plugin",
    url="https://github.com/timvink/mkdocs-enumerate-headings-plugin.git",
    author="timvink",
    author_email="vinktim@gmail.com",
    license="MIT",
    python_requires=">=3.5",
    install_requires=["mkdocs>=1.0.4", "beautifulsoup4>=4.9.0"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "enumerate-headings=mkdocs_enumerate_headings_plugin.plugin:EnumerateHeadingsPlugin",
        ]
    },
)
