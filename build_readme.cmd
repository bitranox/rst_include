REM
REM rst_include needs to be installed and python paths set correctly
@echo off
cls

SET repository="rst_include"

REM # get dashed repository name for pypi links
echo %repository% | rst_inc.py replace "_" "-" > temp.txt
set /p repository_dashed= < temp.txt
del tmp.txt


echo 'create the sample help outputs'
rst_inc.py -h > ./docs/rst_include_help_output.txt
rst_inc.py include -h > ./docs/rst_include_help_include_output.txt
rst_inc.py replace -h > ./docs/rst_include_help_replace_output.txt

echo 'import the include blocks'
rst_inc.py include -s ./docs/README_template.rst -t ./docs/README_template_included.rst

echo 'replace repository strings'
rst_inc.py replace -s ./docs/README_template_included.rst -t ./docs/README_template_repo_replaced.rst {repository} %repository%
rst_inc.py replace -s ./docs/README_template_repo_replaced.rst -t ./README.rst {repository_dashed} %repository_dashed%

echo 'finished'
