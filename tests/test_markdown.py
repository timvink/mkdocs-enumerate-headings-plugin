from mkdocs_add_number_plugin import markdown

page1 = """
# Example page

some content

## another heading

more content

## Some section

bla bla
bla

### sub heading

bla

### another sub heading

## Another section
"""

def test_headings():
    lines = page1.split('\n')
    assert markdown.headings(lines) == {
        1: '# Example page',
        5: '## another heading',
        9: '## Some section',
        14: '### sub heading',
        18: '### another sub heading',
        20: '## Another section'}
    
def test_heading_depth():
    lines = page1.split('\n')
    heading_lines = markdown.headings(lines).values()
    assert [markdown.heading_depth(x) for x in heading_lines] == [
        1,2,2,3,3,2
    ]
    
def test_update_heading_chapter():
    line = "## 1.2.1 heading"
    assert markdown.update_heading_chapter(line, 4) == '## 4.2.1 heading'
    
    line = "#### 1.4.2.3 Another chapter!!1!"
    assert markdown.update_heading_chapter(line, 24) == '#### 24.4.2.3 Another chapter!!1!'