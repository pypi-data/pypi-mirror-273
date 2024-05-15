import re
from pathlib import Path

from chardet.universaldetector import UniversalDetector

__char_detector = UniversalDetector()


def detect_encoding(filename):
    __char_detector.reset()
    try:
        with open(filename, 'rb') as fp:
            for line in fp.readlines():
                __char_detector.feed(line)
                if __char_detector.done:
                    break
            result = __char_detector.result
            return result['encoding']
    except FileNotFoundError:
        return 'utf-8'


def normalize_path(path: Path, anchor=Path('.')) -> Path:
    path = Path(path)
    anchor = Path(anchor)
    if path.is_absolute():
        return path.absolute()

    t = str(path)
    if t.startswith('~'):
        return Path(t.replace('~', str(Path.home()))).absolute()

    return anchor.absolute() / path


def quote_path(path, quote_char='"') -> str:
    path = str(path)
    return f'"{path}"' if ' ' in path else path


def limit_number(x, left, right):
    _min = min(left, right)
    _max = max(left, right)
    if x < _min:
        return _min
    if x > _max:
        return _max
    return x


def split_at_unquoted_spaces(line: str):
    result = []
    buffer = []
    symbols = {'"', "'", '(', ')', '[', ']', '{', '}'}
    matching = {')': '(', ']': '[', '}': '{'}
    stack = []
    in_quotes = False
    quote_char = ''

    for char in str(line):
        if char in symbols:
            if in_quotes:
                if char == quote_char:
                    in_quotes = False
            else:
                if char == '"' or char == "'":
                    in_quotes = True
                    quote_char = char
                elif char in matching and stack and stack[-1] == matching[char]:
                    stack.pop()
                else:
                    stack.append(char)
        if char == ' ' and not stack and not in_quotes:
            result.append(''.join(buffer))
            buffer = []
        else:
            buffer.append(char)

    # 如果缓冲区还有字符，则将它们加入到结果列表中。
    if buffer:
        result.append(''.join(buffer))

    return result


def unquote_text(s: str):
    """删除字符串前后的成对引号以及多余的空格"""
    pattern = r'^("|\')((?:(?=(\\?))\3.)*?)\1$'
    text = s.strip()
    match = re.match(pattern, text)
    if match:
        text = match.group(2)
    return text.strip()


def quote_text(s: str, quote='"'):
    """阔起字符串，默认使用引号。如果给定的quote包含多个字符，则会使用前两个分别阔起，例如使用括号"""
    left = quote[0]
    right = quote[1] if len(quote) > 1 else left
    return left + str(s) + right
