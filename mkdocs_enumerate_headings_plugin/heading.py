class Heading:
    def __init__(self, element, soup) -> None:
        """
        Args:
            element (bs4.element.Tag): BeautifulSoup Tag
            soup: BeautifulSoup class instance 
        """
        self.heading = element
        self.soup = soup

        # Placeholder for h1-h6 section numbers that will be filled later
        self.section_numbering = [0, 0, 0, 0, 0, 0]

    @property
    def depth(self):
        """
        Translates h1-h6 strings to integer
        """
        assert self.heading.name in ["h1", "h2", "h3", "h4", "h5", "h6"]
        return int(self.heading.name[1])

    @property
    def anchorlink(self) -> str:
        """Returns HTML anchorlink
        
        F.e. a tag with <h1 id="the-homepage">The Homepage</h1>
        would have anchor link "#the-homepage"

        Returns:
            str: anchorlink
        """
        if self.heading.get("id"):
            return "#" + self.heading.get("id")
        else:
            return None

    def set_section_number(self, section_number: int, depth: int):
        self.section_numbering[depth - 1] = section_number

    def get_section_number(self, depth: int):
        return self.section_numbering[depth - 1]

    def set_chapter(self, chapter):
        # Chapter is the h1 section number.
        # Note that chapter numbers should always start at either 0 or 1
        # And then increment.
        line_chapter = self.section_numbering[0]
        if line_chapter == 0:
            new_chapter = chapter
        else:
            new_chapter = line_chapter - 1 + chapter

        self.section_numbering[0] = new_chapter

    def section_number_string(self, start_level: int = 1):
        """
        Translate section numbering to a string

        Args:
            start_level: First heading depth (1-6) to include in the visible label;
                tiers before this are omitted (e.g. 2 omits the H1 tier).

        Examples:
            # Basic heading
            [1, 0, 0, 0, 0, 0]
            #> "1."
            # Subheading
            [2, 1, 0, 0, 0, 0]
        """
        if self.section_numbering == [0, 0, 0, 0, 0, 0]:
            raise AssertionError(
                "[enumerate-heading-plugin] Heading '%s' has not been assigned any section numbering"
                % self.heading.string
            )

        if start_level < 1 or start_level > 6:
            raise ValueError("start_level must be between 1 and 6")

        numbers = list(self.section_numbering[start_level - 1 :])

        # Remove any trailing zeros (copy only — never mutate section_numbering)
        while numbers and numbers[-1] == 0:
            numbers.pop()

        if not numbers:
            raise AssertionError(
                "[enumerate-heading-plugin] Heading '%s' has not been assigned any section numbering"
                % self.heading.string
            )

        # Join to string
        heading_string = [str(x) for x in numbers]
        heading_string = ".".join(heading_string)

        # Add a trailing dot to level 1 headings
        # For example "1" should be "1."
        if "." not in heading_string:
            heading_string += "."

        return heading_string

    def enumerate(self, add_span_element=False, start_level: int = 1):
        section_string = self.section_number_string(start_level=start_level)
        self.heading.insert(0, " ")

        # Note we add both enumerate-headings-plugin and enumerate-heading-plugin
        # This is for backward compatibility
        # https://github.com/timvink/mkdocs-enumerate-headings-plugin/issues/24
        if add_span_element:
            span = self.soup.new_tag("span", **{"class": "enumerate-headings-plugin enumerate-heading-plugin"})
            span.string = section_string
            self.heading.insert(0, span)
        else:
            self.heading.insert(0, section_string)
