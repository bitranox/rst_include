cd C:\opt\vm-shared-folder\pyapps\rst_include

:loop
C:\Python37-64\Scripts\pytest.exe
cd C:\opt\vm-shared-folder\pyapps\rst_include
mypy -p rst_include
goto loop
