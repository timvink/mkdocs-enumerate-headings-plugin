![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-enumerate-headings-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-enumerate-headings-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-enumerate-headings-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-enumerate-headings-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-enumerate-headings-plugin)

# mkdocs-enumerate-headings-plugin

[MkDocs](https://www.mkdocs.org/) plugin to automatically enumerate the headings (h1-h6) in each markdown page. This only affects your rendered HTML and does not affect the markdown files.

# TODO

- put online on github, add all the automated github actions, badges, pypi deploy, etc
- promote on mkdocs
- add `<span>` around headings
- describe how to customize CSS
- open issue with mkdocs material to support plugin
- make sure plugin works with `mkdocs-awesome-pages`. and possibly also with `mkdocs-monorepo`; promote that on the README
- document behaviour with some examples. Add screenshot. mention use case: writing reports.
- implement some classes.
- document tocdepth is 6

## Setup

Install the plugin using `pip`:

```bash
pip3 install mkdocs-enumerate-headings-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - enumerate-headings
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

Example of multiple options set in the `mkdocs.yml` file:

```yml
plugins:
    - search
    - enumerate-headings
```
