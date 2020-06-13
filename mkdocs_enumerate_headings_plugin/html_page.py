import re
import logging
from bs4 import BeautifulSoup

from mkdocs_enumerate_headings_plugin.heading import Heading


class HTMLPage:
    def __init__(self, content: str) -> None:

        self.soup = BeautifulSoup(content, "html.parser")
        self.headings = self._find_headings()
        self._find_section_numbering()

    def __str__(self):
        return str(self.soup)

    def enumerate_headings(self, add_span_element: bool = True):
        """
        Adds section numbering to all headings in all pages.

        Args:
            add_span_element (bool): Wrap numbering with <span class='enumerate-heading-plugin'></span>. Defaults to True.
        """
        for heading in self.headings:
            heading.enumerate(add_span_element=add_span_element)

    def enumerate_toc(self, depth: int = 0):
        links = self.soup.find_all("a", href=True)

        for heading in self.headings:
            for link in links:
                if link.get("href") == heading.anchorlink and heading.depth <= depth:
                    link.insert(0, " ")
                    link.insert(0, heading.section_number_string())

    def set_page_chapter(self, chapter: int) -> None:
        [h.set_chapter(chapter) for h in self.headings]

    def validate(self, page, plugin_config):

        # If no headings, then also valid
        if len(self.headings) == 0:
            return True

        # If first headings is level 1, all is good
        if self.headings[0].depth == 1:
            return True

        # First heading is not level 1
        msg = (
            "[enumerate_headings_plugin]: The first heading on '%s' is should be level 1. Use '# <your title>'"
            % page.file.src_path
        )
        if plugin_config["strict"]:
            raise AssertionError(msg)
        else:
            logging.warning(msg)
        return False

    def _find_headings(self):
        """
        Returns:
            List[Heading]: list of Heading class instances
        """
        return [
            Heading(x, self.soup) for x in self.soup.find_all(re.compile("^h[1-6]$"))
        ]

    def _find_section_numbering(self):
        """
        This function contains the core algorithm for determining
        the section numbering for each heading.
        
        The main trick is that we look for each heading depth separately
        at the list of lines with headings.
        """

        # Look at each heading level separately
        for depth in range(1, 7):
            for i, heading in enumerate(self.headings):
                if i == 0:
                    # First heading line. Start counting at 1 only if heading is right depth
                    heading.set_section_number(int(heading.depth == depth), depth)
                elif heading.depth < depth:
                    # The heading depth is higher than current level, restart counter
                    heading.set_section_number(0, depth)
                elif heading.depth == depth:
                    # New heading at current depth level, increment counter
                    previous_section_number = self.headings[i - 1].get_section_number(
                        depth
                    )
                    heading.set_section_number(previous_section_number + 1, depth)
                else:
                    # No change, keep previous section number
                    previous_section_number = self.headings[i - 1].get_section_number(
                        depth
                    )
                    heading.set_section_number(previous_section_number, depth)
