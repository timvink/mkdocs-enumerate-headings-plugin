from typing import List

from mkdocs_enumerate_headings_plugin.line import Line


class MarkdownPage:
    def __init__(self, lines: List[str]):
        """
        Args:
            lines (List[str]): Lines from a markdown file
        """

        self.lines = [Line(l) for l in lines]
        self._find_headings()
        self._find_section_numbering()

    def enumerate_headings(self):
        return [str(l) for l in self.lines]

    def _find_headings(self):
        """
        Finds lines that are markdown headings
        """
        is_block = False
        for line in self.lines:
            if line.startswith("```"):
                is_block = not is_block
            if not is_block and line.startswith("#"):
                line.set_is_heading(True)
            else:
                line.set_is_heading(False)

    def _find_section_numbering(self):
        """
        This function contains the core algorithm for determining
        the section numbering for each heading.
        
        The main trick is that we look for each heading depth separately
        at the list of lines with headings.
        """

        # Only consider heading lines
        lines = [l for l in self.lines if l.get_is_heading()]

        # Look at each heading level separately
        for depth in [1, 2, 3, 4, 5, 6]:
            for i, line in enumerate(lines):
                line_depth = line.heading_depth()
                if i == 0:
                    # First heading line. Start counting at 1 only if heading is right depth
                    line.set_section_number(int(line_depth == depth), depth)
                elif line_depth < depth:
                    # The heading depth is higher than current level, restart counter
                    line.set_section_number(0, depth)
                elif line_depth == depth:
                    # New heading at current depth level, increment counter
                    previous_section_number = lines[i - 1].get_section_number(depth)
                    line.set_section_number(previous_section_number + 1, depth)
                else:
                    # No change, keep previous section number
                    previous_section_number = lines[i - 1].get_section_number(depth)
                    line.set_section_number(previous_section_number, depth)
