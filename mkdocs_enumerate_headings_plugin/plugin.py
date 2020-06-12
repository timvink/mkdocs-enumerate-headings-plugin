# coding=utf-8

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs_enumerate_headings_plugin.html_page import HTMLPage
from bs4 import BeautifulSoup


class EnumerateHeadingsPlugin(BasePlugin):
    config_scheme = (("strict", config_options.Type(bool, default=True)),)

    def on_config(self, config, **kwargs):

        # Move plugin to be last in the plugins list
        # Because some plugins alter the navigation, and we need the final navigation
        # This hack might not be necessary in future MkDocs versions, when `nav` is available on other later events as well
        plugins = config["plugins"]
        plugins.move_to_end("enumerate-headings")

        # Move plugin's on_nav event to be last to run
        # Because some plugins alter the navigation, and we need the final navigation
        # This hack might not be necessary in future MkDocs versions, when `nav` is available on other later events as well
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
            page.read_source(config)
            page.render(config, files)
            soup = BeautifulSoup(page.content, "html.parser")
            h1s = soup.find_all("h1")
            page.number_h1s = len(h1s) or 0

            # Some markdown files could be used multiple times in the same navigation
            # This would lead to unique page instances, but we'd like only use (count) the chapter
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

        # Skip enumeration if page not in navigation, or if page does not have any headings
        if not hasattr(page, "chapter"):
            return output

        # Process HTML
        htmlpage = HTMLPage(output)
        htmlpage.validate(page=page, plugin_config=self.config)

        # Set chapter and enumerate the headings
        htmlpage.set_page_chapter(page.chapter)
        return htmlpage.enumerate_headings()
