@echo off
:: Activar el entorno virtual (usando Scripts para Windows)
echo Activando entorno virtual 'whasenv'...
call whasenv\Scripts\activate.bat
pause
:: Verificar si la activación fue exitosa
if %errorlevel% neq 0 (
    echo Error: No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

:: Ejecutar la aplicación
echo Ejecutando la aplicación...
python src\main.py 10 %*

:: Cerrar el entorno virtual
echo Cerrando entorno virtual...
deactivate

pause
