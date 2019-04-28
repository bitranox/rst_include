def strip_list_of_strings(list_of_strings: [str], chars: str = '') -> [str]:
    """
    strips list elements of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> strip_list_of_strings(testlist)
    ['a', 'b', 'c']

    """

    list_of_strings = lstrip_list_of_strings(list_of_strings, chars)
    list_of_strings = rstrip_list_of_strings(list_of_strings, chars)
    return list_of_strings


def lstrip_list_of_strings(list_of_strings: [str], chars: str = '') -> [str]:
    """
    strips list elements on the beginning of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> lstrip_list_of_strings(testlist)
    ['a', 'b', 'c', '', '']
    >>> testlist = []
    >>> lstrip_list_of_strings(testlist)
    []
    """
    while list_of_strings and list_of_strings[0] == chars:
        list_of_strings = list_of_strings[1:]
    return list_of_strings


def rstrip_list_of_strings(list_of_strings: [str], chars: str = '') -> [str]:
    """
    strips list elements on the beginning of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> rstrip_list_of_strings(testlist)
    ['', '', 'a', 'b', 'c']
    >>> testlist = []
    >>> rstrip_list_of_strings(testlist)
    []

    """
    while list_of_strings and list_of_strings[-1] == chars:
        list_of_strings = list_of_strings[:-1]
    return list_of_strings
