try:
    # for pytest
    from . import include1
    from . import include2
    from . import include3
    from .subdir import include_subdir
except ImportError:                                                         # pragma: no cover
    # for local doctest in pycharm
    import rst_include.tests.include1 as include1                           # type: ignore # pragma: no cover
    import rst_include.tests.include2 as include2                           # type: ignore # pragma: no cover
    import rst_include.tests.include3 as include3                           # type: ignore # pragma: no cover
    import rst_include.tests.subdir.include_subdir as include_subdir        # type: ignore # pragma: no cover


def test() -> None:
    """
    # test all python files You use in documentation - so the documentation is also tested !
    >>> include1.my_include()
    >>> include2.my_include2_0()
    >>> include2.my_include2_1()
    >>> include2.my_include2_2()
    >>> include2.my_include2_3()
    >>> include3.my_include()
    >>> include_subdir.my_include2_0()
    >>> include_subdir.my_include2_1()
    >>> include_subdir.my_include2_2()
    >>> include_subdir.my_include2_3()
    >>> test()
    """
    pass
