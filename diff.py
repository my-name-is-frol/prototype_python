from __future__ import print_function
from collections import namedtuple
import sys

Keep = namedtuple('Keep', ['line'])
Insert = namedtuple('Insert', ['line'])
Remove = namedtuple('Remove', ['line'])

Frontier = namedtuple('Frontier', ['x', 'history'])


def myers_diff(a_lines, b_lines):
    frontier = {1: Frontier(0, [])}

    def one(idx):
        return idx - 1

    a_max = len(a_lines)
    b_max = len(b_lines)
    for d in range(0, a_max + b_max + 1):
        for k in range(-d, d + 1, 2):
            go_down = (k == -d or (k != d and frontier[k - 1].x < frontier[k + 1].x))

            if go_down:
                old_x, history = frontier[k + 1]
                x = old_x
            else:
                old_x, history = frontier[k - 1]
                x = old_x + 1

            history = history[:]
            y = x - k

            if 1 <= y <= b_max and go_down:
                history.append(Insert(b_lines[one(y)]))
            elif 1 <= x <= a_max:
                history.append(Remove(a_lines[one(x)]))

            while x < a_max and y < b_max and a_lines[one(x + 1)] == b_lines[one(y + 1)]:
                x += 1
                y += 1
                history.append(Keep(a_lines[one(x)]))

            if x >= a_max and y >= b_max:
                return history
            else:
                frontier[k] = Frontier(x, history)


if __name__ == '__main__':
    _, a_file, b_file, res_file = sys.argv

    with open(a_file) as a_handle:
        a_lines = [line.rstrip() for line in a_handle]

    with open(b_file) as b_handle:
        b_lines = [line.rstrip() for line in b_handle]

    diff = myers_diff(a_lines, b_lines)

    i = 0

    diff_arr = []

    for elem in diff:
        if isinstance(elem, Keep):
            print(' ' + elem.line)
            i += 1
        elif isinstance(elem, Insert):
            print(str(i) + '@' + elem.line)
            diff_arr.append(str(i) + '@' + elem.line)
        else:
            print(str(-1 * i) + '@' + elem.line)
            diff_arr.append(str(-1 * i) + '@' + elem.line)
            i += 1

    with open(res_file, 'w') as f:
        for item in diff_arr:
            f.write("%s\n" % item)
