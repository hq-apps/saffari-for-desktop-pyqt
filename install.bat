@echo off
echo.
echo This is a very barebones script to install Saffari for desktop on Windows. It has basically not been tested at all.
echo If you want to improve it or report issues with it, open a GH PR, issue or report it on DC.
echo You need to have Python 3 installed already for this to work, we might add a Python installer or bundle it at some point in the future.
echo Press any key to continue...
pause > nul
cls

REM Check if Python 3 is installed
python3 --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python 3 is not installed.
    set /p install_python="Do you want to install Python 3 now? (y/n): "
    if /i "%install_python%"=="y" (
        echo Opening Microsoft Store to install Python 3...
        start ms-windows-store://pdp/?ProductId=9PJPW5L8Z1Z5
        echo Please install Python 3 from the Microsoft Store and then run this script again.
        pause > nul
        exit
    ) else (
        echo Python 3 is required to run this script. Exiting...
        pause > nul
        exit
    )
)

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
