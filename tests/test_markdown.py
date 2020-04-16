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
    
def test_enumerate_headings():

    headings = {
        1: '# Example page',
        5: '## another heading',
        9: '## Some section',
        14: '### sub heading',
        18: '### another sub heading',
        20: '## Another section' }
    assert markdown.enumerate_headings(headings) == {
        1: '# 1. Example page',
        5: '## 1.1 another heading',
        9: '## 1.2 Some section',
        14: '### 1.2.1 sub heading',
        18: '### 1.2.2 another sub heading',
        20: '## 1.3 Another section' } 
    
    headings = {
            1: '# test',
            2: '## test',
            3: '# test',
            4: '## test',
            5: '## test' }
    assert markdown.enumerate_headings(headings) == {
            1: '# 1. test',
            2: '## 1.1 test',
            3: '# 2. test',
            4: '## 2.1 test',
            5: '## 2.2 test' }
    
    # Skipping a level
    headings = {
            2: '# test',
            3: '### test' }
    assert markdown.enumerate_headings(headings) == {
            2: '# 1. test',
            3: '### 1.0.1 test' }
    
    # Missing first heading 1
    headings = {
            2: '## sub',
            3: '# head' }
    assert markdown.enumerate_headings(headings) == {
            2: '## 0.1 sub',
            3: '# 1. head' }

    headings = {
            2: '## sub1',
            3: '## sub2',
            4: '### sub3', }
    assert markdown.enumerate_headings(headings) == {
            2: '## 0.1 sub1',
            3: '## 0.2 sub2',
            4: '### 0.2.1 sub3', }

    
def test_insert_heading_number():
    line = "## Example page"
    heading = "2.2"
    new_line = markdown.insert_heading_number(line, heading)
    assert new_line == "## 2.2 Example page"


def test_heading_number():
    
    depths = [1, 2, 1, 2, 2]
    h1 = markdown.heading_number(depths, heading_depth = 1)
    assert h1 == [1,1,2,2,2]
    h2 = markdown.heading_number(depths, heading_depth = 2) 
    assert h2 == [0,1,0,1,2]
    h3 = markdown.heading_number(depths, heading_depth = 3) 
    assert h3 == [0,0,0,0,0]
    
    depths = [1, 2, 3, 3, 1, 2, 4]
    h1 = markdown.heading_number(depths, heading_depth = 1) 
    assert h1 == [1, 1, 1, 1, 2, 2, 2]
    h2 = markdown.heading_number(depths, heading_depth = 2) 
    assert h2 == [0, 1, 1, 1, 0, 1, 1]
   
    # Edge cases where h1 is missing
    assert markdown.heading_number([2], heading_depth = 2) == [1]
    assert markdown.heading_number([2], heading_depth = 1) == [0]
    # Edge cases where h1 is not first
    assert markdown.heading_number([3,2,1], heading_depth = 1) == [0,0,1]
    assert markdown.heading_number([3,2,1], heading_depth = 2) == [0,1,0]
    assert markdown.heading_number([3,2,1], heading_depth = 3) == [1,0,0]
    # Edge case where h1 is missing and a level is skipped
    assert markdown.heading_number([2,4], heading_depth = 1) == [0,0] 
    assert markdown.heading_number([2,4], heading_depth = 2) == [1,1] 
    assert markdown.heading_number([2,4], heading_depth = 4) == [0,1]
    # Edge case where a level is skipped
    assert markdown.heading_number([1,3], heading_depth = 1) == [1,1]
    assert markdown.heading_number([1,3], heading_depth = 2) == [0,0]
    assert markdown.heading_number([1,3], heading_depth = 3) == [0,1]

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