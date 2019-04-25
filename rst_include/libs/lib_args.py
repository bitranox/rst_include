# -*- coding: utf-8 -*-

import argparse
import sys


def parse_args(cmd_args=sys.argv[1:]):
    # type: ([]) -> []
    """
    >>> # parse_args()

    """
    parser = argparse.ArgumentParser(
        description='Process .rst File Includes',
        epilog='check the documentation on github',
        add_help=True)

    subparsers = parser.add_subparsers()

    parser_include = subparsers.add_parser('include', help='include rst includes')
    parser_include.add_argument('-s', '--source', nargs='?', metavar='source', default=sys.stdin, help='default: stdin')
    parser_include.add_argument('-t', '--target', nargs='?', metavar='target', default=sys.stdout, help='default: stdout')
    parser_include.add_argument('-se', '--source_encoding', metavar='source encoding', nargs='?', default='utf-8-sig', help='default: utf-8-sig')
    parser_include.add_argument('-te', '--target_encoding', metavar='target encoding', nargs='?', default='utf-8', help='default: utf-8')
    parser_include.add_argument('-c', '--config', metavar='configfile.py', nargs='?',
                                help='If no filename is passed, the default conf_res_inc.py is searched in the current directory')

    parser_replace = subparsers.add_parser('replace', help='string replace')
    parser_replace.add_argument('-s', '--source', nargs='?', metavar='source', default=sys.stdin, help='default: stdin')
    parser_replace.add_argument('-t', '--target', nargs='?', metavar='target', default=sys.stdout, help='default: stdout')
    parser_replace.add_argument('-se', '--source_encoding', metavar='source encoding', nargs='?', default='utf-8-sig', help='default: utf-8-sig')
    parser_replace.add_argument('-te', '--target_encoding', metavar='target encoding', nargs='?', default='utf-8', help='default: utf-8')
    parser_replace.add_argument('old', type=str, help='old')
    parser_replace.add_argument('new', type=str, help='new')
    parser_replace.add_argument('count', type=int, nargs='?', help='count', default=-1)

    args = parser.parse_args(cmd_args)
    return args, parser


def cmd_args_config_flag_given(cmd_args):
    # type: ([str]) -> bool
    """
    >>> assert cmd_args_config_flag_given(['']) == False
    >>> assert cmd_args_config_flag_given(['-c']) == True
    >>> assert cmd_args_config_flag_given(['--config']) == True
    """
    if '-c' in cmd_args or '--config' in cmd_args:
        return True
    else:
        return False


def is_replace_command(args):  # type: (dict) -> bool
    """
    >>> is_replace_command({'old':''})
    True
    >>> is_replace_command({'something':''})
    False
    """
    if 'old' in args:
        return True
    else:
        return False


def is_include_command(args):  # type: (dict) -> bool
    """
    >>> is_include_command({'config':''})
    True
    >>> is_include_command({'something':''})
    False
    """
    if 'config' in args:
        return True
    else:
        return False
