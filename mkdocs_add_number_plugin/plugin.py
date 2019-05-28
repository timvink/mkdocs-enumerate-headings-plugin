# coding=utf-8
import os

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class AddIndexPlugin(BasePlugin):
    config_scheme = (
        ('strict_mode', config_options.Type(bool, default=False)),
        ('excludes', config_options.Type(list, default=[])),
        ('includes', config_options.Type(list, default=[])),
        ('order', config_options.Type(int, default=1))
    )

    def __init__(self):
        self.enabled = True
        self._has_load_conf = False
        self._oder = None

    def _init(self):
        if not self._has_load_conf:
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
            # with open('excludes.log', 'a') as f:
            #     f.write("_excludes: {:s}\n_exclude_files: {:s}\n_exclude_files: {:s}\n\n".format(
            #         self._excludes, self._exclude_files, self._exclude_files))
            self._has_load_conf = True

    def on_page_markdown(self, markdown, page, config, files):
        self._init()

        if self._is_exclude(page) and not self._is_include(page):
            return markdown

        lines = markdown.split('\n')
        line_length = len(lines)
        tmp_lines = {}
        n = 0
        is_block = False

        while n < line_length:
            if lines[n].startswith('```'):
                is_block = not is_block

            if not is_block and lines[n].startswith('#'):
                tmp_lines[n] = lines[n]
            n += 1

        if len(tmp_lines) <= self._order:
            return markdown

        keys = sorted(tmp_lines.keys())
        tmp_lines_values = []
        for key in keys:
            tmp_lines_values.append(tmp_lines[key])

        if self.config['strict_mode']:
            tmp_lines_values, _ = self._searchN(tmp_lines_values, 1, self._order, 1, [], self._searchN)
        else:
            tmp_lines_values = self._ascent(tmp_lines_values, [0], 0, [], 1, self._order)
            # tmp_lines_values = self._ascent(tmp_lines_values, [0], 1, [], 0, 0)

        n = 0
        for key in keys:
            lines[key] = tmp_lines_values[n]
            n += 1

        return '\n'.join(lines)

    def _ascent(self, tmp_lines, parent_nums_head, level, args, num, startrow):

        if startrow == len(tmp_lines):
            return tmp_lines
        nums_head = self._nums_head(tmp_lines[startrow])
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

    def _nums_head(self, tmp_string):
        n = 0
        while tmp_string[n:n + 1] == '#':
            n += 1

        return n

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
