import re


class Line(str):
    def __init__(self, line: str):
        self.line = line
        self.is_heading = None
        self.section_numbering = [0, 0, 0, 0, 0, 0]

    def __str__(self):
        if self.is_heading is None:
            raise ReferenceError(
                "is_heading attribute has not been determined yet. Run Page._find_headings() first."
            )

        if not self.is_heading:
            return self.line

        pattern = re.compile(r"(\#+) (.*)")
        matches = pattern.match(self.line)
        return "%s %s %s" % (
            matches.group(1),
            self.section_number_string(),
            matches.group(2),
        )

    def get_section_number(self, depth: int):
        return self.section_numbering[depth - 1]

    def set_section_number(self, section_number: int, depth: int):
        self.section_numbering[depth - 1] = section_number

    def get_is_heading(self):
        if self.is_heading is None:
            raise ReferenceError(
                "is_heading attribute has not been determined yet. Run Page._find_headings() first."
            )
        return self.is_heading

    def set_is_heading(self, is_heading):
        self.is_heading = is_heading

    def heading_depth(self) -> int:
        """
        Determines the markdown heading depth from a line
        
        Examples:
        
        'a line' returns 0
        '# heading' returns 1
        '### heading' returns 3
        """
        n = 0
        while self.line[n : n + 1] == "#":
            n += 1
        return n

    def section_number_string(self):
        """
        Translate section numbering to a string
        
        Examples:
            # Basic heading
            [1, 0, 0, 0, 0, 0]
            #> "1."
            # Subheading
            [2, 1, 0, 0, 0, 0]
        """
        numbers = self.section_numbering

        # Remove any trailing zeros
        while numbers[-1] == 0:
            del numbers[-1]

        # Join to string
        heading_string = [str(x) for x in numbers]
        heading_string = ".".join(heading_string)

        # Add a trailing dot to level 1 headings
        # For example "1" should be "1."
        if "." not in heading_string:
            heading_string += "."

        return heading_string
