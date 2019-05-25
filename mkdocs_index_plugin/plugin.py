# coding=utf-8
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class AddIndexPlugin(BasePlugin):
    config_scheme = (
        ('strict_mode', config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self.enabled = True

    def on_page_markdown(self, markdown, page, config, files):
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

        if len(tmp_lines) == 0:
            return markdown

        keys = sorted(tmp_lines.keys())
        tmp_lines_values = []
        for key in keys:
            tmp_lines_values.append(tmp_lines[key])

        if self.config['strict_mode']:
            tmp_lines_values, _ = self._searchN(tmp_lines_values, 1, 0, 1, [], self._searchN)
        else:
            tmp_lines_values = self._ascent(tmp_lines_values, [0], 0, [], 1, 0)
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
                                                     '.'.join(('%d.' * (level - 1)).split()) % tuple(args), num+1)
            return self._ascent(tmp_lines, parent_nums_head, level, args, num+1, startrow + 1)
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
        re_str = (substr + "%d " % nextnum) if (prenum_str == '') else (substr + "%s%d " % (prenum_str, nextnum))
        tmp_line = tmp_line.replace(substr, re_str)
        return tmp_line

    def _nums_head(self, tmp_string):
        n = 0
        while tmp_string[n:n+1] == '#':
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

        re_str = (substr + "%d " % nextnum) if (prenum_str == '') else (substr + "%s%d " % (prenum_str, nextnum))
        tmp_lines[start_row] = tmp_lines[start_row].replace(substr, re_str)
        return tmp_lines, start_row + 1, True

