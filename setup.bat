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
echo Directorio del script: %cd%

set PYTHON_VERSION=3.13.1
set INSTALLER_NAME=python-%PYTHON_VERSION%-amd64.exe
set INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%INSTALLER_NAME%
set REQUIREMENTS_FILE=requirements.txt
set ERROR_FLAG=0

echo Iniciando instalacion de Python %PYTHON_VERSION% para Windows...
pause

:: Buscar Python
goto :buscar_python


:buscar_python
echo "Buscando Python en rutas conocidas..."
set PYTHON=
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe" (
    set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe
)

if "%PYTHON%"=="" (
    echo Python adecuado no encontrado. Procediendo a instalar Python...
    pause
    goto :install_python
) else (
    echo Python encontrado en %PYTHON%.
    pause
)

:verificar_pip
echo Verificando pip...
pause
"whasenv\Scripts\python.exe" -m ensurepip --upgrade

if %ERRORLEVEL% NEQ 0 (
    echo Error al verificar pip. Instalando pip...
    "whasenv\Scripts\python.exe" -m ensurepip
    pause
)

:: Actualizar pip
echo Actualizando pip...
"whasenv\Scripts\python.exe" -m pip install --upgrade pip || set ERROR_FLAG=1
pause

goto :instalar_librerias


:instalar_librerias
:: Instalar certificados SSL si es necesario
echo Verificando certificados SSL...
"whasenv\Scripts\python.exe" -c "import ssl; ssl.create_default_context()" 2>ssl_error.txt
findstr "CERTIFICATE_VERIFY_FAILED" ssl_error.txt >nul
if %ERRORLEVEL% EQU 0 (
    echo Error de verificacion SSL detectado. Descargando e instalando certificados...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    "whasenv\Scripts\python.exe" get-pip.py
    "whasenv\Scripts\python.exe" -m pip install certifi
    for /f "delims=" %%i in ('"whasenv\Scripts\python.exe" -c "import certifi; print(certifi.where())"') do set SSL_CERT_PATH=%%i
    setx SSL_CERT_FILE "%SSL_CERT_PATH%"
    echo Certificados instalados correctamente.
    del ssl_error.txt
    del get-pip.py
    pause
) else (
    echo Certificados SSL ya están configurados correctamente.
    del ssl_error.txt
    pause
)

:: Instalar librerías desde requirements.txt
if exist %REQUIREMENTS_FILE% (
    echo Instalando librerias desde %REQUIREMENTS_FILE%...
    "whasenv\Scripts\python.exe" -m pip install -r %REQUIREMENTS_FILE% || set ERROR_FLAG=1
    pause
) else (
    echo No se encontro requirements.txt. Omitiendo instalacion de librerias.
    pause
)

goto :endpoint


:install_python
echo Descargando e instalando Python %PYTHON_VERSION%...
curl -o %INSTALLER_NAME% %INSTALLER_URL%
start /wait %INSTALLER_NAME%
echo "Python instalado."
timeout /t 5 /nobreak
goto :buscar_python


:endpoint
echo Instalacion completa. Pulsa Enter para salir.
pause
exit /b 0
