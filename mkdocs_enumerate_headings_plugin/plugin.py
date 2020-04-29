# coding=utf-8
import logging

from os import linesep
from collections import OrderedDict
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from .markdown_page import MarkdownPage
from .utils import read_md


class EnumerateHeadingsPlugin(BasePlugin):
    config_scheme = (("strict", config_options.Type(bool, default=True)),)

    def __init__(self):
        self.counter_page_chapter = 0
        self.pages = list()

    def on_config(self, config, **kwargs):

        # Move plugin to be last in the plugins list
        plugins = config["plugins"]
        plugins.move_to_end("enumerate-headings")

        # Move plugin's on_nav event to be last to run
        nav_events = plugins.events["nav"]

        def get_plugin_name(bound_method):
            return type(bound_method.__self__).__name__

        plugin_nav_event = [
            e for e in nav_events if get_plugin_name(e) == "EnumerateHeadingsPlugin"
        ][0]
        nav_events.append(nav_events.pop(nav_events.index(plugin_nav_event)))
        plugins.events["nav"] = nav_events

        config["plugins"] = plugins
        return config

    def on_nav(self, nav, config, **kwargs):
        """
        The nav event is called after the site navigation is created
        and can be used to alter the site navigation.

        See:
        https://www.mkdocs.org/user-guide/plugins/#on_nav
        
        Args:
            nav: global navigation object
            config: global configuration object

        Returns:
            nav: global navigation object
        """

        self.pages_in_nav = OrderedDict()

        chapter_counter = 0
        for page in nav.pages:
            src_path = page.file.abs_src_path
            if not src_path in self.pages_in_nav:

                md_page = MarkdownPage(read_md(src_path), config)
                if md_page.has_headings:
                    self.pages_in_nav.update({src_path: chapter_counter + 1})
                    chapter_counter += md_page.get_max_chapter()

        return nav

    def on_page_markdown(self, markdown, page, config, **kwargs):
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

        # Skip enumeration if page not in navigation or page does not have any headings
        if not page.file.abs_src_path in self.pages_in_nav:
            return markdown

        lines = markdown.splitlines()
        md_page = MarkdownPage(lines, config)

        if not md_page.validate():
            msg = (
                "[enumerate_headings_plugin]: The first heading on '%s' is should be level 1. Use '# <your title>'"
                % page.file.src_path
            )
            if self.config["strict"]:
                raise AssertionError(msg)
            else:
                logging.warning(msg)

        # Set page chapter number
        chapter = self.pages_in_nav[page.file.abs_src_path]
        md_page.set_page_chapter(chapter)

        lines = md_page.enumerate_headings()
        return linesep.join(lines)
