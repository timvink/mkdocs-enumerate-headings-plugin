# coding=utf-8


import logging

from collections import OrderedDict
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import ConfigurationError
from mkdocs_enumerate_headings_plugin.html_page import HTMLPage
from mkdocs_enumerate_headings_plugin.exclude import exclude
from bs4 import BeautifulSoup

logger = logging.getLogger("mkdocs.plugins")


class EnumerateHeadingsPlugin(BasePlugin):
    config_scheme = (
        ("strict", config_options.Type(bool, default=True)),
        ("toc_depth", config_options.Type(int, default=0)),
        ("increment_across_pages", config_options.Type(bool, default=True)),
        ("restart_increment_after", config_options.Type(list, default=[])),
        ("exclude", config_options.Type(list, default=[])),
    )

    def on_pre_build(self, config, **kwargs):
        """Validates plugin user configuration input

        Args:
            config (dict): plugin configuration
        """
        if self.config.get("toc_depth", 0) > 6:
            raise ConfigurationError(
                "toc_depth is set to %s, but max is 6. Update plugin settings in mkdocs.yml."
                % self.config.get("toc_depth")
            )

    def on_config(self, config, **kwargs):

        # This plugin needs the navigation
        # But some plugins alter the navigation
        # MkDocs executes plugins in order they are defined
        # So we can do some checks on other plugins defined.

        plugins = [*OrderedDict(config["plugins"])]

        def check_position(plugin, plugins):
            if plugin in plugins:
                if plugins.index("enumerate-headings") < plugins.index(plugin):
                    raise ConfigurationError(
                        "[enumerate-headings-plugin] enumerate-headings should be defined after the %s plugin in your mkdocs.yml file"
                        % plugin
                    )

        # Check list of plugins that alter the navigation
        # To make sure they are not defined after the enumerate-heading plugin
        # taken from https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins#navigation--page-building
        check_plugins = [
            "monorepo",
            "exclude",
            "select-files",
            "awesome-pages",
            "mkdocs-nav-enhancements",
            "navtitles",
            "encryptcontent",
            "awesome-list",
            "toc-sidebar",
            "mkdocs-simple-hooks",
            "mkdocstrings"
        ]
        for p in check_plugins:
            check_position(p, plugins)

        return config

    def on_nav(self, nav, config, files, **kwargs):
        """
        The nav event is called after the site navigation is created
        and can be used to alter the site navigation.
        
        See:
        https://www.mkdocs.org/user-guide/plugins/#on_nav        
        
        We use this event to determine and save the chapter number of a page in the navigation.
        Pages are not build in the same order as they appear in the navigation
        We need to know upfront both the order and how many heading 1's they contain (could be more than 1).

        Args:
            nav: global navigation object
            config: global configuration object
            files: global files collection
        
        """
        chapter_counter = 0
        markdown_files_processed = {}

        for page in nav.pages:

            # Exclude pages specified in config
            excluded_pages = self.config.get("exclude", [])
            if exclude(page.file.src_path, excluded_pages):
                continue

            # We need to build the pages in order to find out
            # if there are more than one heading 1's in the page
            page.read_source(config)
            page.render(config, files)
            soup = BeautifulSoup(page.content, "html.parser")
            h1s = soup.find_all("h1")

            # We assume here a page always has a heading 1, even if empty
            # MkDocs will determine the title based on a simple heuristic
            # (see https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)
            # and some themes will insert the page title as a heading 1, if heading 1 is missing
            page.number_h1s = max(len(h1s), 1)

            # Optionally do not increment counter across pages.
            if self.config.get('increment_across_pages') is False:
                chapter_counter = 0

            # Optionally reset the counter for this page
            restarting_pages = self.config.get("restart_increment_after", [])
            if exclude(page.file.src_path, restarting_pages):
                chapter_counter = 0

            # Some markdown files could be used multiple times in the same navigation
            # This would lead to unique page instances, but we'd like to only use (count) the chapter
            # of the first occurence.
            if page.file.abs_src_path not in markdown_files_processed:
                chapter = chapter_counter + 1
                markdown_files_processed[page.file.abs_src_path] = chapter
                chapter_counter += page.number_h1s
            else:
                chapter = markdown_files_processed[page.file.abs_src_path]

            page.chapter = chapter

    def on_post_page(self, output, page, config, **kwargs):
        """
        The post_page event is called after the template is rendered, 
        but before it is written to disc and can be used to alter the output of the page. 
        If an empty string is returned, the page is skipped and nothing is written to disc.
        
        Note that the order in which pages are built does NOT correspond with the order of pages in the navigation (nav)

        See:
        https://www.mkdocs.org/user-guide/plugins/#on_post_page
        
        Args:
            output (str): output of rendered template as string
            page (Page): mkdocs.nav.Page instance
            config (dict): global configuration object

        Returns:
            output (str): output of rendered template as string
        """

        # Exclude pages specified in config
        excluded_pages = self.config.get("exclude", [])
        if exclude(page.file.src_path, excluded_pages):
            return

        # Skip enumeration if page not in navigation, or if page does not have any headings
        if not hasattr(page, "chapter"):
            return output

        if str(page.file.abs_src_path).endswith("ipynb"):
            logger.warning(
                "[enumerate-headings-plugin] Skipping enumeration of %s"
                % page.file.src_path
            )
            return output

        # Process HTML
        htmlpage = HTMLPage(output)
        htmlpage.validate(page=page, plugin_config=self.config)

        # Set chapter and enumerate the headings
        htmlpage.set_page_chapter(page.chapter)

        htmlpage.enumerate_headings()
        htmlpage.enumerate_toc(depth=self.config.get("toc_depth"))
        return str(htmlpage)
