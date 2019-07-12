REM
REM rst_include needs to be installed and python paths set correctly
@echo off
cls

REM # You might also use Environment Variable here, or as commandline parameter
REM # this is just an example, I use actually the build_readme.py python file myself
REM # I do not recommend cmd files anymore - why it it is so much easier under python ...
REM # I am sure there is a more elegant was to do it on batch files, this is only an example

SET repository_slug="bitranox/rst_include"
SET repository="rst_include"
SET codeclimate_link_hash="ff3f414903627e5cfc35"

REM # get dashed repository name for pypi links
echo %repository% | rst_include replace "_" "-" > temp.txt
set /p repository_dashed= < temp.txt
del temp.txt


REM paths absolute, or relative to the location of the config file
REM the notation for relative files is like on windows or linux - not like in python.
REM so You might use ../../some/directory/some_document.rst to go two levels back.
REM avoid absolute paths since You never know where the program will run.

echo 'create the sample help outputs'
rst_include -h > ./docs/rst_include_help_output.txt
rst_include include -h > ./docs/rst_include_help_include_output.txt
rst_include replace -h > ./docs/rst_include_help_replace_output.txt

echo "import the include blocks"
rst_include include -s ./docs/README_template.rst -t ./README.rst

REM please note that the replace syntax is not shown correctly in the README.rst,
REM because it gets replaced itself by the build_docs.py
REM we could overcome this by first replacing, and afterwards including -
REM check out the build_docs.cmd for the correct syntax !

echo "replace repository_slug"
rst_include replace --inplace -s ./docs/README_template.rst {repository_slug} %repository_slug%
echo "replace repository"
rst_include replace --inplace -s ./docs/README_template.rst {repository} %repository%
echo "replace repository_dashed"
rst_include replace --inplace -s ./docs/README_template.rst {repository_dashed} %repository_dashed%
echo "replace codeclimate_link_hash"
rst_include replace --inplace -s ./docs/README_template.rst {codeclimate_link_hash} %codeclimate_link_hash%

echo 'finished'
