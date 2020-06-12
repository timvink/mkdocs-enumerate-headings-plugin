[![Actions Status](https://github.com/timvink/mkdocs-enumerate-headings-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-enumerate-headings-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-enumerate-headings-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-enumerate-headings-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-enumerate-headings-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-enumerate-headings-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-enumerate-headings-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-enumerate-headings-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-enumerate-headings-plugin)

# mkdocs-enumerate-headings-plugin

[MkDocs](https://www.mkdocs.org/) Plugin to enumerate the headings (h1-h6) across site pages

## Features :star2:

- Automatically number all headings and give each page an sequential chapter number
- Compatible with `plugins` like [awesome-pages](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) and [monorepo](https://github.com/spotify/mkdocs-monorepo-plugin)
- Compatible with `markdown_extensions` like [pymdownx.snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
- Easy to customize styling through CSS

![demo screencast](demo_screencast.gif)

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

There is only one requirement: make sure each markdown page starts with a level 1 header (`#`).
Pages with no headings and pages with multiple level 1 headings are allowed.

> Note this plugin only affects your rendered HTML and does not affect the markdown files.

### Styling

All heading numbers are wrapped in `<span class='enumerate-headings-plugins'></span>` and can be styled using CSS. See MkDocs documentation for [customizing a theme](https://www.mkdocs.org/user-guide/styling-your-docs/#customizing-a-theme) on how to add an CSS to your theme.

As an example you can make the numbering lighter than the heading title by saving the CSS snippet below to a file and adding it to your MkDocs site using the [extra_css](https://www.mkdocs.org/user-guide/configuration/#extra_css) setting in your `mkdocs.yml` file.

```css
/* Extra CSS for mkdocs-enumerate-headings-plugin */ 
.enumerate-headings-plugins {
  /* 100% is baseline so 250% is a lot lighter */
  filter: brightness(250%);
}
```

## Options

You can customize the plugin by setting options in `mkdocs.yml`:

```yml
plugins:
    - enumerate-headings:
        strict: true
```

- **`strict`** (default `true`): Raise errors instead of warnings when first heading on a page is not a level one heading (single `#`). Note that in `strict: false` mode the heading numbers might be incorrect between pages and before and after a level 1 heading.

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before putting in any work.

This plugin was inspired by [ignorantshr/mkdocs-add-number-plugin](https://github.com/ignorantshr/mkdocs-add-number-plugin), which focuses on enumerating single selected pages.
