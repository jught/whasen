@echo off

:: Solicitar permisos de Administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~fnx0' -Verb RunAs"
    exit /b
)

:: Cambiar al directorio del script
cd /d %~dp0
cd ..
echo Directorio del script: %cd%

:: Configuracion de Python
set PYTHON_VERSION=3.13.1
set INSTALLER_NAME=python-%PYTHON_VERSION%-amd64.exe
set INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%INSTALLER_NAME%
set REQUIREMENTS_FILE=requirements.txt
set ERROR_FLAG=0
set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe

:verificar_whatsapp
:: Verificar instalacion de WhatsApp
echo Verificando si WhatsApp Desktop esta instalado...

reg query HKEY_CURRENT_USER /f WhatsApp /s >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    reg query HKEY_LOCAL_MACHINE /f WhatsApp /s >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo WhatsApp no esta instalado.
        start https://www.whatsapp.com/download
        exit /b 1
    )
)

echo WhatsApp esta instalado. Continuando...

:: Progreso de instalacion de Python
:buscar_python
echo Iniciando instalacion de Python %PYTHON_VERSION%...
for %%P in (10 30 50 70 90 100) do (
    echo Instalacion %%P%% completada...
    timeout /t 1 >nul
)

:: Verificar instalacion de Python
if exist %PYTHON% (
    echo Python encontrado en %PYTHON%
    ::pause
    goto :instalar_librerias
) else (
    goto :install_python
)

:: Instalar Python si no existe
:install_python
echo Descargando Python %PYTHON_VERSION%...
curl -o %INSTALLER_NAME% %INSTALLER_URL%
echo Instalando Python...
start /wait %INSTALLER_NAME%
echo Python instalado.
timeout /t 5 /nobreak
setx PATH %PYTHON%
goto :buscar_python

:: Instalar librerias desde requirements.txt
:instalar_librerias
if exist %REQUIREMENTS_FILE% (
    echo Instalando librerias desde %REQUIREMENTS_FILE% con %PYTHON% ...
    "%PYTHON%" -m pip install -r %REQUIREMENTS_FILE% >pip_error.log 2>&1 || set ERROR_FLAG=1
    if %ERROR_FLAG% NEQ 0 (
        echo Error al instalar librerias. Ver pip_error.log para mas detalles.
    ) else (
        echo Librerias instaladas correctamente.
    )
    goto :endpoint
) else (
    echo No se encontro %REQUIREMENTS_FILE%. Omitiendo instalacion de librerias.
)

:endpoint
echo Instalacion completada con exito.
echo Pulsa Enter para salir.
pause
exit /b 0
