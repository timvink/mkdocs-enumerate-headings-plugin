[![Actions Status](https://github.com/timvink/mkdocs-enumerate-headings-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-enumerate-headings-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-enumerate-headings-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-enumerate-headings-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-enumerate-headings-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-enumerate-headings-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-enumerate-headings-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-enumerate-headings-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-enumerate-headings-plugin)

# mkdocs-enumerate-headings-plugin

[MkDocs](https://www.mkdocs.org/) Plugin to enumerate the headings (h1-h6) across MkDocs pages.

> :point_right: If you're looking to add heading numbers to your site to support exporting to single-page standalone HTML or a PDF file, have a look at [mkdocs-print-site-plugin](https://timvink.github.io/mkdocs-print-site-plugin/) instead!

## Features :star2:

- Automatically number all headings and (optionally) give each page an sequential chapter number
- Great for writing (technical) reports
- Compatible with `plugins` like [awesome-pages](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) and [monorepo](https://github.com/spotify/mkdocs-monorepo-plugin)
- Compatible with `markdown_extensions` like [pymdownx.snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
- Compatible with themes like [mkdocs-material](https://github.com/squidfunk/mkdocs-material)
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

> MkDocs executes plugins in the order they are defined. If you use any other plugins that alter the navigation, make sure to define them *before* the `enumerate-headings` plugin.

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

`enumerate-headings` will increment the chapter number for each new page (in the order they appear in the navigation) and enumerate all subheadings (unless you disable in this in the options).

There is only one requirement: make sure each markdown page starts with a level 1 header (see [how to write markdown headers](https://daringfireball.net/projects/markdown/syntax#header)). Some MkDocs themes will handle this for your automatically, inserting the page title as a heading 1 if you do not specify one. If a heading 1 is still missing, you'll get a helpful error.

Pages with multiple level 1 headings are allowed and the chapter numbers will increment accordingly.

> Note this plugin does not affect your markdown files, only the rendered HTML.

### Styling

All heading numbers are wrapped in `<span class='enumerate-headings-plugins'></span>` and can be styled using CSS. See [customizing a MkDocs theme](https://www.mkdocs.org/user-guide/styling-your-docs/#customizing-a-theme) on how to add an CSS to your theme.

As an example you can make the numbering lighter than the heading title by saving the CSS snippet below to a file and adding it to your MkDocs site using the [extra_css](https://www.mkdocs.org/user-guide/configuration/#extra_css) setting in your `mkdocs.yml` file.

```css
/* Extra CSS for mkdocs-enumerate-headings-plugin */ 
.enumerate-headings-plugin {
  filter: opacity(35%);
}
```

## Options

You can customize the plugin by setting options in `mkdocs.yml`:

```yml
plugins:
    - enumerate-headings:
        toc_depth: 0
        strict: true
        increment_across_pages: true
        include:
          - "*"
        exclude:
          - index.md
          - another_page.md
        restart_increment_after:
          - second_section.md
        enumerate_nav: true
```

- **`toc_depth`** (default `0`): Up to which level the table of contents should be enumerated as well. Default is 0, which means the TOC is not enumerated at all. Max is 6 (showing all enumeration)
- **`strict`** (default `true`): Raise errors instead of warnings when first heading on a page is not a level one heading (single `#`) and your MkDocs theme has not inserted the page title as a heading 1 for you. Note that in `strict: false` mode the heading numbers might be incorrect between pages and before and after a level 1 heading.
- **`increment_across_pages`** (default `true`): Increment the chapter number for each new page (in the order they appear in the navigation). If disabled, each page will start from 1.
- **`include`** (default *`["*"]`*): Specify a list of page source paths (one per line) that should have enumeration (included in processing by this plugin). This can be useful for example to include enumeration on only one directory. The source path of a page is relative to your `docs/` folder. You can also use [globs](https://docs.python.org/3/library/glob.html) instead of source paths. For example, to include `docs/subfolder/page.md` specify in your `mkdocs.yml` a line under `include:` with `- subfolder/page.md`
- **`exclude`** (default *not specified*): Specify a list of page source paths (one per line) that should not have enumeration (excluded from processing by this plugin). This can be useful for example to remove enumeration from the front page. The source path of a page is relative to your `docs/` folder. You can also use [globs](https://docs.python.org/3/library/glob.html) instead of source paths. For example, to exclude `docs/subfolder/page.md` specify in your `mkdocs.yml` a line under `exclude:` with `- subfolder/page.md`
- **`restart_increment_after`** (default *not specified*): Specify a list of page source paths (one per line) where enumeration should be restarted. This can be useful if you have multiple reports or tutorials in one mkdocs site. Paths behave as with `exclude` (can use globs).
- **`enumerate_nav`** (default `true`): Also add numbers to pages ("chapters") in the navigation.

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before putting in any work.

Credits: This plugin was inspired by [ignorantshr/mkdocs-add-number-plugin](https://github.com/ignorantshr/mkdocs-add-number-plugin), which focuses on enumerating single selected pages.
