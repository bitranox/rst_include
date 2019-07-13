"""Setuptools entry point."""
import codecs
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
changes_filename = os.path.join(dirname, 'CHANGES.rst')

long_description = description
if os.path.exists(readme_filename):
    try:
        readme_content = codecs.open(readme_filename, encoding='utf-8').read()
        long_description = readme_content
    except Exception:
        pass

if os.path.exists(changes_filename):
    try:
        changes_content = codecs.open(changes_filename, encoding='utf-8').read()
        long_description = '\n'.join((long_description, changes_content))
    except Exception:
        pass

setup(
    name='rst_include',
    python_requires='>3.5.2',
    version='1.0.8',
    description=description,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Robert Nowotny',
    author_email='rnowotny1966@gmail.com',
    url='https://github.com/bitranox/rst_include',
    packages=['rst_include', 'rst_include.libs'],
    install_requires=['pytest',
                      'typing'],
    classifiers=CLASSIFIERS,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    # scripts=['rst_inc.py'],   # old method - worked well on windows
    entry_points={
        'console_scripts': [
            'rst_include = rst_include.rst_include:main'
        ]
    }

)
