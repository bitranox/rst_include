import argparse
import logging
import sys
from typing import List, Tuple, Union

logger = logging.getLogger()


def parse_args(cmd_args: List[str] = sys.argv[1:]) -> Tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(
        description='Process .rst File Includes',
        epilog='check the documentation on github',
        prog='rst_include',
        add_help=True)

    subparsers = parser.add_subparsers()

    parser_include = subparsers.add_parser('include', help='include rst includes')
    parser_include.add_argument('-s', '--source', nargs='?', metavar='source', default=sys.stdin, help='default: stdin')
    parser_include.add_argument('-t', '--target', nargs='?', metavar='target', default=sys.stdout, help='default: stdout')
    parser_include.add_argument('-se', '--source_encoding', metavar='source encoding', nargs='?', default='utf-8-sig', help='default: utf-8-sig')
    parser_include.add_argument('-te', '--target_encoding', metavar='target encoding', nargs='?', default='utf-8', help='default: utf-8')
    parser_include.add_argument('-i', '--inplace', help='inplace - target file = sourcefile, implies -f', action="store_true")
    parser_include.add_argument('-c', '--config', metavar='configfile.py', nargs='?',
                                help='If no filename is passed, the default conf_rst_inc.py is searched in the current directory')

    parser_replace = subparsers.add_parser('replace', help='string replace')
    parser_replace.add_argument('-s', '--source', nargs='?', metavar='source', default=sys.stdin, help='default: stdin')
    parser_replace.add_argument('-t', '--target', nargs='?', metavar='target', default=sys.stdout, help='default: stdout')
    parser_replace.add_argument('-se', '--source_encoding', metavar='source encoding', nargs='?', default='utf-8-sig', help='default: utf-8-sig')
    parser_replace.add_argument('-te', '--target_encoding', metavar='target encoding', nargs='?', default='utf-8', help='default: utf-8')
    parser_replace.add_argument('-i', '--inplace', help='inplace - target file = sourcefile, implies -f', action="store_true")
    parser_replace.add_argument('old', type=str, help='old')
    parser_replace.add_argument('new', type=str, help='new')
    parser_replace.add_argument('count', type=int, nargs='?', help='count', default=-1)

    args = parser.parse_args(cmd_args)

    if args.inplace:
        if args.source == sys.stdin:
            raise SyntaxError('You need to specify the input file if You use option --inplace')
        elif args.target == args.source:
            logger.warning('You dont need to specify the target file if You use option --inplace')
        elif args.target != sys.stdout:
            raise SyntaxError('You dont have to use option --inplace and specify a target file different to the input file')
        args.target = args.source
        args.force = True

    return args, parser


def cmd_args_config_flag_given(cmd_args: List[str]) -> bool:
    """
    >>> assert cmd_args_config_flag_given(['']) == False
    >>> assert cmd_args_config_flag_given(['-c']) == True
    >>> assert cmd_args_config_flag_given(['--config']) == True
    """
    if '-c' in cmd_args or '--config' in cmd_args:
        return True
    else:
        return False


def is_option_inplace_set(cmd_args: List[str] = sys.argv[1:]) -> bool:
    """

    >>> is_option_inplace_set(['replace', '-i', '-s', '/test.txt','x', 'y'])
    True

    >>> is_option_inplace_set(['replace', '--inplace', '-s', '/test.txt','x', 'y'])
    True

    >>> is_option_inplace_set(['replace', '-i', 'x', 'y'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    SyntaxError: You need to specify the input file if You use option --inplace

    >>> is_option_inplace_set(['replace', '--inplace', '-s', '/test.txt', '-t', '/test.txt', 'x', 'y'])
    True

    >>> is_option_inplace_set(['replace', '--inplace', '-s', '/test.txt', '-t', '/test2.txt', 'x', 'y'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    SyntaxError: You dont have to use option --inplace and specify a target file different to the input file

    >>> is_option_inplace_set(['replace','x','y'])
    False

    """
    args, parser = parse_args(cmd_args)
    if args.inplace:
        return True
    else:
        return False


def is_replace_command(args: argparse.Namespace) -> bool:
    """
    >>> args = argparse.Namespace()
    >>> args.old = ''
    >>> is_replace_command(args)
    True
    >>> del args.old
    >>> is_replace_command(args)
    False
    """
    if 'old' in args:
        return True
    else:
        return False


def is_include_command(args: argparse.Namespace) -> bool:
    """
    >>> args = argparse.Namespace()
    >>> args.config = ''
    >>> is_include_command(args)
    True
    >>> del args.config
    >>> is_include_command(args)
    False
    """
    if 'config' in args:
        return True
    else:
        return False
