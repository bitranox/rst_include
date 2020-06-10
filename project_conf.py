# single point for all configuration of the project

# stdlib
from setuptools import find_packages  # type: ignore
from typing import List, Dict

package_name = 'rst_include'  # type: str
version = '1.1.0'
# codeclimate_link_hash - get it under https://codeclimate.com/github/<user>/<project>/badges
codeclimate_link_hash = 'ff3f414903627e5cfc35'  # for rst_include

# cc_test_reporter_id - get it under https://codeclimate.com/github/<user>/<project> and press "test coverage"
cc_test_reporter_id = ''    # for rst_include

# pypi_password
# to create the secret :
# cd /<repository>
# travis encrypt -r bitranox/lib_parameter pypi_password=*****
# copy and paste the encrypted password here
# replace with:
# travis_pypi_secure_code = '<code>'     # pypi secure password, without '"'
travis_pypi_secure_code = 'kunEN/xI7zqyo7II2hD6oMFTUQHkMH8w11vNk5QcrfLkTGCdsEvETigtIjs1pVtUz1SXqeHMDD8I8Ooz9pc1s91l2qCmIe4N05mN47Nsn4NN5lCFBiD2PM4hLr'\
                          'U1318d/s1a46SPRZXHEb4gvA89nwwJZwWmUfOVKdMjhEClAr5xa6jLNgT8CkFSSJjS6qxBVnNCVR7Dq0mMHuyX/KEKnltIqqHG+wCI9mI7eOPBxw2zDPYduAmq'\
                          'm3F+Y5xBUIyKhRc9lTYnqq3HecP2PFJ5tXenMFBUI1IrgTLADS1+a6o4bTn1ARE5p+2rsICndrEckr4se5gtMT2RsmI40aXykB4GtqMzvMXIW4TthFKPDfB4UN'\
                          'e1ZDqkhJYi8khuJqII1CjKt9R2VvIb2MpqtePPFC45Fw8gcIoOfrcl3ekGugnR5/soLlo/qLyO1DGhIY5kqzQ+T9EL7GL7s6TixAIzzw/UEfuh97fQxi1JgkAy'\
                          'nHbhbzX9ac1YgZtyi/300gWJy0gca5ZyBGoGiypiCmAOCzYnv0TKD1TLeCviNellvbOrGIJ6THuEqPY5lw7Ex3RFax485IHTH1o8mD59EvsA1CUYEPkUWX+lvI'\
                          'LHEa+hTBVbXrWTxLOLGWVP+84XtdEx0trDb/6ZfTPRtZ2XsHNNsW6O2rERcMiVdb++0X6TNFg='

# include package data files
# package_data = {package_name: ['some_file_to_include.txt']}
package_data = dict()       # type: Dict[str, List[str]]

author = 'Robert Nowotny'
author_email = 'rnowotny1966@gmail.com'
github_account = 'bitranox'

linux_tests = True
osx_tests = True
pypy_tests = True
windows_tests = True
wine_tests = False
badges_with_jupiter = False

# a short description of the Package - especially if You deploy on PyPi !
description = 'since You can not include files into RST files on github and PyPi, You can replace those imports with this software.'

# #############################################################################################################################################################
# DEFAULT SETTINGS - no need to change usually, but can be adopted
# #############################################################################################################################################################

shell_command = package_name
src_dir = package_name
module_name = package_name
init_config_title = description
init_config_name = package_name

# we ned to have a function main_commandline in module module_name - see examples
entry_points = {'console_scripts': ['{shell_command} = {src_dir}.{module_name}:main_commandline'
                .format(shell_command=shell_command, src_dir=src_dir, module_name=module_name)]}  # type: Dict[str, List[str]]

long_description = package_name  # will be overwritten with the content of README.rst if exists

packages = [package_name]

url = 'https://github.com/{github_account}/{package_name}'.format(github_account=github_account, package_name=package_name)
github_master = 'git+https://github.com/{github_account}/{package_name}.git'.format(github_account=github_account, package_name=package_name)
travis_repo_slug = github_account + '/' + package_name

CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Software Development :: Libraries :: Python Modules']
