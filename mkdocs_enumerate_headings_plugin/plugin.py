# coding=utf-8
import os
import logging

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from .markdown_page import MarkdownPage
from .utils import flatten, read_md, chapter_numbers


class EnumerateHeadingsPlugin(BasePlugin):
    config_scheme = (("strict", config_options.Type(bool, default=True)),)

    def __init__(self):
        self.counter_page_chapter = 0
        self.pages = list()

    def on_nav(self, nav, config, files):

        # TODO
        # check that this plugin is defined *after* plugins that also use on_nav(), like monorepo and awesomepages

        # Find ordering of pages displayed in site
        if config.get("nav"):
            pages = flatten(config["nav"])
        else:
            pages = [f.src_path for f in files.documentation_pages()]

        # Find number of chapters per page
        pages_n_chapters = []
        for page in pages:
            abs_path = os.path.join(config["docs_dir"], page)
            markdown_page = MarkdownPage(read_md(abs_path))
            n_chapters = markdown_page.get_max_chapter()
            pages_n_chapters.append(n_chapters)

        # Determine sequential chapter numbers
        page_chapter_numbers = chapter_numbers(pages_n_chapters)
        self.page_chapter_number = dict(zip(pages, page_chapter_numbers))

        return nav

    def on_page_markdown(self, markdown, page, config, files):
        """
        The page_markdown event is called after the page's markdown is loaded 
        from file and can be used to alter the Markdown source text. 
        The meta- data has been stripped off and is available as page.meta 
        at this point.
        
        See:
        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown
        
        Args:
            markdown (str): Markdown source text of page as string
            page (Page): mkdocs.nav.Page instance
            config (dict): global configuration object
            files (list): global files collection
        
        Returns:
            markdown (str): Markdown source text of page as string
        """

        if not page.file.src_path in self.page_chapter_number.keys():
            return markdown

        lines = markdown.splitlines()
        md_page = MarkdownPage(lines)

        if not md_page.first_heading_is_level1():
            msg = (
                "[enumerate_headings_plugin]: The first heading on '%s' is should be level 1. Use '# <your title>'"
                % page.file.src_path
            )
            if self.config["strict"]:
                raise AssertionError(msg)
            else:
                logging.warning(msg)

        # Set page chapter number
        page_chapter = self.page_chapter_number[page.file.src_path]
        md_page.set_page_chapter(page_chapter)

        lines = md_page.enumerate_headings()
        return "\n".join(lines)
