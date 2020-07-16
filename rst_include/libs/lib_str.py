# OWN
import lib_list


def strip_multiline_string(str_multiline: str) -> str:
    """
    >>> strip_multiline_string('')
    ''
    >>> strip_multiline_string('a')
    'a'
    >>> strip_multiline_string('a\\nb')
    'a\\nb'
    >>> strip_multiline_string('a\\nb\\n')
    'a\\nb'
    >>> strip_multiline_string('   \\na\\nb')
    'a\\nb'
    >>> strip_multiline_string('   a\\n  a\\nb')
    '   a\\n  a\\nb'
    >>> strip_multiline_string('   \\n  a\\na\\nb   \\n   \\n')
    '  a\\na\\nb'

    """
    l_lines = str_multiline.split('\n')
    l_lines = [line.rstrip() for line in l_lines]
    l_lines = lib_list.ls_strip_list(l_lines)
    str_result = '\n'.join(l_lines)
    return str_result


def has_trailing_character_return(str_multiline: str) -> bool:
    """
    >>> has_trailing_character_return('jhgjh\\n')
    True
    >>> has_trailing_character_return('jhgjh\\ntestt')
    False
    """
    if len(str_multiline) and str_multiline[-1] == '\n':
        preserve_trailing_linefeed = True
    else:
        preserve_trailing_linefeed = False
    return preserve_trailing_linefeed


def join_if_not_empty(sep: str, str1: str, str2: str) -> str:
    """
    >>> join_if_not_empty('SEP', '', '')
    ''
    >>> join_if_not_empty('SEP', 'a', '')
    'a'
    >>> join_if_not_empty('SEP', 'a', ' ')
    'aSEP '
    >>> join_if_not_empty('SEP', 'a', 'b')
    'aSEPb'
    """
    if str1 != '' and str2 != '':
        result = sep.join((str1, str2))
    else:
        result = max(str1, str2)
    return result
