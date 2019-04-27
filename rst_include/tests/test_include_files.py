import rst_include.tests.include1 as include1
import rst_include.tests.include2 as include2
import rst_include.tests.include3 as include3
import rst_include.tests.subdir.include_subdir as include_subdir


def test():
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
