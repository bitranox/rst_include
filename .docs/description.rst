since You can not include files into RST files on github or PyPi, You can resolve such imports with this software.

That means You can locally write Your RST documents (for instance with pycharm) and use there
the *.. include:* option to include other RST Files or code snippets into Your Document.
Afterwards You can run this software to create a monolithic README.rst that can be viewed on Github or Pypi

You might also include Text/Code from Jupyter Notebooks (sorry, no pictures at the moment, but it is not very hard to do that)

This has many advantages like :

- dont repeat Yourself, create standard blocks to include into Your documentation
- include tested code snippets from Your code files into Your documentation, to avoid untested or outdated documentation
- include other RST Files
- very simple usage, throwing exit codes to detect errors on documentation at travis build-time
- commandline or programmatic interface, You can even use it in the travis.yml
- commandline interface supporting shellscript, cmd, pipes, config-files
