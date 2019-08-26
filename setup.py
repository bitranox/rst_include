"""Setuptools entry point."""
import codecs
import os
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def install_requirements_when_using_setup_py():
    proc = subprocess.Popen([sys.executable, "-m", "pip", "install", '-r', './requirements_setup.txt'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    encoding = sys.getdefaultencoding()
    print(stdout.decode(encoding))
    print(stderr.decode(encoding))

    if proc.returncode != 0:
        raise RuntimeError('Error installing requirements_setup.txt')


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

description = 'include files to rst for documentation purposes'

dirname = os.path.dirname(__file__)
readme_filename = os.path.join(dirname, 'README.rst')

long_description = description
if os.path.exists(readme_filename):
    readme_content = codecs.open(readme_filename, encoding='utf-8').read()
    long_description = readme_content


setup(name='rst_include',
      python_requires='>=3.6.0',
      version='1.0.8',
      description=description,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='Robert Nowotny',
      author_email='rnowotny1966@gmail.com',
      url='https://github.com/bitranox/rst_include',
      packages=['rst_include', 'rst_include.libs'],
      classifiers=CLASSIFIERS,
      # scripts=['rst_inc.py'],   # old method - worked well on windows
      entry_points={'console_scripts': ['rst_include = rst_include.rst_include:main']},
      # specify what a project minimally needs to run correctly
      install_requires=['typing', 'lib_list', 'lib_log_utils', 'lib_path'],
      # minimally needs to run the setup script, dependencies needs also to put here for setup.py install test
      setup_requires=['typing', 'pytest-runner', 'lib_list', 'lib_log_utils', 'lib_path'],
      # minimally needs to run tests
      tests_require=['typing', 'pytest']
      )
