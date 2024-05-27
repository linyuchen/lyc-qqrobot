import re


def get_substring(start_string: str, end_string: str, data: str, contain_start=False, contain_end=False) -> str:
    if not start_string:
        pos0 = 0
    else:
        pos0 = data.find(start_string)

        if -1 == pos0:
            return ""

        if not contain_start:
            pos0 += len(start_string)

    data = data[pos0:]
    if not end_string:
        pos1 = len(data)
    else:
        pos1 = data.find(end_string)

    if -1 == pos1:
        return ""

    if contain_end:
        pos1 += len(end_string)

    data = data[:pos1]

    return data


def split_lines(text: str, line_width: int) -> list[str]:
    current_line_width = 0
    current_line = []
    result = []
    for c in text:
        # 标点符号算作全角字符
        if not re.match(r"[\da-zA-Z,`#!@$*%^&().<>'\"\[\]\-=]", c):
            # if unicodedata.east_asian_width(c) in ('F', 'W'):
            # 全角字符
            current_line_width += 1
        else:
            # 半角字符
            current_line_width += 0.4
        current_line.append(c)
        if current_line_width >= line_width:
            result.append("".join(current_line))
            current_line = []
            current_line_width = 0
    if current_line:
        result.append("".join(current_line))
    return result


if __name__ == '__main__':
    print(split_lines("我``..**我aa我123@@4567**(8", 3))
