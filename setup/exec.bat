@echo off
set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe
set APP=src\main.py
set TABS=10
cd ..
echo Ejecutando %APP% con %PYTHON% %APP% %TABS% 
pause 
%PYTHON% %APP% %TABS% %*
pause
