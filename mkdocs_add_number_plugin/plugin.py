# coding=utf-8
import os

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from .utils import flatten
from . import markdown as md

class AddIndexPlugin(BasePlugin):
    config_scheme = (
        ('strict_mode', config_options.Type(bool, default=False)),
        ('increment_pages', config_options.Type(bool, default=True)),
        ('excludes', config_options.Type(list, default=[])),
        ('includes', config_options.Type(list, default=[])),
        ('order', config_options.Type(int, default=1))
    )
    
    def _check_config_params(self):
        set_parameters = self.config.keys()
        allowed_parameters = dict(self.config_scheme).keys()
        if set_parameters != allowed_parameters:
            unknown_parameters = [x for x in set_parameters if x not in allowed_parameters]
            print(unknown_parameters)
            print(set_parameters)
            print(allowed_parameters)
            raise AssertionError("Unknown parameter(s) set: %s" % ", ".join(unknown_parameters))

    def on_files(self, files, config):
        """
        The files event is called after the files collection is populated from the docs_dir. 
        Use this event to add, remove, or alter files in the collection.
        
        See https://www.mkdocs.org/user-guide/plugins/#on_files
        
        Args:
            files (list): list with pages (class Page)
            config (dict): global configuration object
            
        Returns:
            files (list): list with pages (class Page)
        """
       
        self._check_config_params()
        
        # Use navigation if set, 
        # (see https://www.mkdocs.org/user-guide/configuration/#nav)
        # only these pages will be displayed. 
        nav = config.get('nav', None)
        if nav:
            pages = flatten(nav)
        # Otherwise, take all source markdown pages
        else:
            pages = [
                page.src_path for page in files if page.is_documentation_page()
            ]
    
        # Record excluded files from selection by user
        self._excludes = self.config['excludes']
        self._exclude_files = [os.path.normpath(file1) for file1 in self._excludes if not file1.endswith('\\')
                                and not file1.endswith('/')]
        self._exclude_dirs = [os.path.normpath(dir1) for dir1 in self._excludes if dir1.endswith('\\')
                                or dir1.endswith('/')]

        self._includes = self.config['includes']
        self._include_files = [os.path.normpath(file1) for file1 in self._includes if not file1.endswith('\\')
                                and not file1.endswith('/')]
        self._include_dirs = [os.path.normpath(dir1) for dir1 in self._includes if dir1.endswith('\\')
                                or dir1.endswith('/')]

        self._order = self.config['order'] - 1
        
        # Remove pages excluded from selection by user
        print(f"excluded: {self._exclude_files} and {self._exclude_dirs}\n\n")
        print(f"page urls: {[page.url for page in files]}")
        pages_to_remove = [page.file.src_path for page in files if self._is_exclude(page) and not self._is_include(page)]
        print("\npages_to_remove\n")
        print(pages_to_remove)
        self.pages = [page for page in pages if page not in pages_to_remove]
        
        return files
        
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
        
        # print(f"page.file.src_page is: {page.file.src_path}")
        # print(f"self.pages is: {self.pages}")
        
        if page.file.src_path not in self.pages:
            return markdown

        lines = markdown.split('\n')
        heading_lines = md.headings(lines)
        
        if len(heading_lines) <= self._order:
            return markdown

        tmp_lines_values = list(heading_lines.values())

        if self.config['strict_mode']:
            tmp_lines_values, _ = self._searchN(tmp_lines_values, 1, self._order, 1, [], self._searchN)
        else:
            tmp_lines_values = self._ascent(tmp_lines_values, [0], 0, [], 1, self._order)
            # tmp_lines_values = self._ascent(tmp_lines_values, [0], 1, [], 0, 0)
        
        if self.config.get('increment_pages', False):
            # Throw error if there is more than one heading at level 1
            h1_lines = [x for x in heading_lines.values() if x.startswith("# ")]
            if len(h1_lines) > 1:
                raise AssertionError("""Page %s contains more than one level 1 heading:\n\n%s
                                     Consider setting 'increment_pages' to False""" % 
                                (page.file.src_path, "\n".join(h1_lines)))
            
            # Set chapter number
            # because lists start at 0 and not 1
            chapter_number = self.pages.index(page.file.src_path) + 1
            tmp_lines_values = [
                md.update_heading_chapter(l, chapter_number)
                for l in tmp_lines_values
            ]
        
        # Add heading numbers to markdown
        n = 0
        for key in heading_lines.keys():
            lines[key] = tmp_lines_values[n]
            n += 1

        return '\n'.join(lines)

    def _ascent(self, tmp_lines, parent_nums_head, level, args, num, startrow):

        if startrow == len(tmp_lines):
            return tmp_lines
        
        nums_head = md.heading_depth(tmp_lines[startrow])
        parent_nums = parent_nums_head[len(parent_nums_head) - 1]

        if nums_head < parent_nums:
            if level != 1:
                num = args.pop()
            level -= 1
            parent_nums_head.pop()
            return self._ascent(tmp_lines, parent_nums_head, level, args, num, startrow)

        if nums_head == parent_nums:
            tmp_lines[startrow] = self._replace_line(tmp_lines[startrow], '#' * nums_head + ' ',
                                                     '.'.join(('%d.' * (level - 1)).split()) % tuple(args), num + 1)
            return self._ascent(tmp_lines, parent_nums_head, level, args, num + 1, startrow + 1)
        else:
            level += 1
            # len(args) == level - 1
            if level != 1:
                args.append(num)
            parent_nums_head.append(nums_head)
            tmp_lines[startrow] = self._replace_line(tmp_lines[startrow], '#' * nums_head + ' ',
                                                     '.'.join(('%d.' * (level - 1)).split()) % tuple(args), 1)
            return self._ascent(tmp_lines, parent_nums_head, level, args, 1, startrow + 1)

    def _replace_line(self, tmp_line, substr, prenum_str, nextnum):
        re_str = (substr + "%d. " % nextnum) if (prenum_str == '') else (substr + "%s%d " % (prenum_str, nextnum))
        tmp_line = tmp_line.replace(substr, re_str)
        return tmp_line

    def _searchN(self, tmp_lines, num, start_row, level, args, func):
        while True:
            tmp_lines, start_row, re = self._replace(tmp_lines, '#' * level + ' ',
                                                     '.'.join(('%d.' * (level - 1)).split()) % tuple(args), num,
                                                     start_row)
            if not re:
                break

            next_num = 1
            if level != 6:
                args.append(num)
                re_lines, start_row = func(tmp_lines, next_num, start_row, level + 1, args, func)
                args.pop()

            num += 1

        return tmp_lines, start_row

    def _replace(self, tmp_lines, substr, prenum_str, nextnum, start_row):
        if start_row == len(tmp_lines) or not tmp_lines[start_row].startswith(substr):
            return tmp_lines, start_row, False

        re_str = (substr + "%d. " % nextnum) if (prenum_str == '') else (substr + "%s%d " % (prenum_str, nextnum))
        tmp_lines[start_row] = tmp_lines[start_row].replace(substr, re_str)
        return tmp_lines, start_row + 1, True

    def _is_exclude(self, page):
        if len(self._excludes) == 0:
            return False

        url = os.path.normpath(page.url)

        try:
            if url in self._exclude_files or self._exclude_files.index('*') != -1:
                return True
        # no *
        except ValueError:
            return False

        for dir1 in self._exclude_dirs:
            if url.find(dir1) != -1:
                return True

        # with open('page.log', 'a') as f:
        #     f.write("title: {:s}\nabs_url: {:s}\nurl: {:s}\n\n".format(
        #             page.title.encode('utf-8'), page.abs_url.encode('utf-8'), page.url.encode('utf-8')))
        return False

    def _is_include(self, page):
        if len(self._includes) == 0:
            return False

        url = os.path.normpath(page.url)

        if url in self._include_files:
            return True

        for dir1 in self._include_dirs:
            if url.find(dir1) != -1:
                return True

        return False
