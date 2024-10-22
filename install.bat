@echo off
echo.
echo This is a very barebones script to install Saffari for decstop on Windows. It has basically not been tested at all.
echo If you want to improve it or report issues with it, open a GH PR, issue or report it on DC.
echo You need to have Python 3 installed already for this to work, we might add a Python installer or bundle it at some point in the future.
echo Press any key to continue...
pause > nul
cls
echo.
echo Installing requirements...
echo.
pip3 install -r requirements.txt
echo.
echo If there were no errors everything should be set up now.
echo Open run.bat to start Saffari.
echo Press any key to exit...
pause > nul
exit
