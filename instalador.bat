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

set PYTHON_VERSION=3.13.1
set INSTALLER_NAME=python-%PYTHON_VERSION%-amd64.exe
set INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%INSTALLER_NAME%
set REQUIREMENTS_FILE=requirements.txt
set ERROR_FLAG=0

echo Iniciando instalacion de Python %PYTHON_VERSION% para Windows...

:: Buscar Python
goto :buscar_python


:buscar_python
echo "Buscar python"
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
    goto :install_python
) else (
    echo Python encontrado en %PYTHON%.
)

goto :verificar_pip


:verificar_pip
echo Verificando pip...
"%PYTHON%" -m ensurepip --upgrade

if %ERRORLEVEL% NEQ 0 (
    echo Error al verificar pip. Instalando pip...
    "%PYTHON%" -m ensurepip
)

:: Actualizar pip
echo Actualizando pip...
"%PYTHON%" -m pip install --upgrade pip || set ERROR_FLAG=1

goto :instalar_librerias


:instalar_librerias
:: Instalar certificados SSL si es necesario
echo Verificando certificados SSL...
"%PYTHON%" -c "import ssl; ssl.create_default_context()" 2>ssl_error.txt
findstr "CERTIFICATE_VERIFY_FAILED" ssl_error.txt >nul
if %ERRORLEVEL% EQU 0 (
    echo Error de verificacion SSL detectado. Descargando e instalando certificados...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    "%PYTHON%" get-pip.py
    "%PYTHON%" -m pip install certifi
    for /f "delims=" %%i in ('"%PYTHON%" -c "import certifi; print(certifi.where())"') do set SSL_CERT_PATH=%%i
    setx SSL_CERT_FILE "%SSL_CERT_PATH%"
    echo Certificados instalados correctamente.
    del ssl_error.txt
    del get-pip.py
) else (
    echo Certificados SSL ya estan configurados correctamente.
    del ssl_error.txt
)

:: Instalar librerías desde requirements.txt
if exist %REQUIREMENTS_FILE% (
    echo Instalando librerias desde %REQUIREMENTS_FILE%...
    "%PYTHON%" -m pip install -r %REQUIREMENTS_FILE% || set ERROR_FLAG=1
) else (
    echo No se encontro requirements.txt. Omitiendo instalacion de librerias.
)

goto :manejar_path_warnings

:manejar_path_warnings
echo Verificando warnings de PATH...

:: Captura la salida de pip en un archivo temporal
"%PYTHON%" -m pip install yautogui openpyxl pyinstaller pandas 2>&1 > pip_output.txt

:: Procesar el archivo línea por línea
for /f "tokens=*" %%a in (pip_output.txt) do (
    echo %%a | findstr "which is not on PATH" >nul
    if %ERRORLEVEL% EQU 0 (
        
        :: Extraer la ruta entre comillas simples (')
        for /f "tokens=2 delims='" %%b in ("%%a") do (
            set NEW_PATH=%%b
            echo Se detectó un directorio faltante en el PATH: %%b
            
            :: Añadir la ruta al PATH si no está duplicada
            echo %PATH% | findstr /C:"%%b" >nul
            if %ERRORLEVEL% NEQ 0 (
                setx PATH "%PATH%;%%b" /M
                echo %%b añadido al PATH correctamente.
            ) else (
                echo La ruta ya existe en el PATH. Omitiendo...
            )
        )
    )
)

:: Eliminar el archivo temporal
del pip_output.txt


:: Añadir Python al PATH solo si hay errores
:add_python
echo "Añadiendo python? "%ERROR_FLAG%
if %ERROR_FLAG% NEQ 0 (
    echo Se detectaron errores. Anadiendo Python al PATH...
    set PYTHON_DIR=%PYTHON:\python.exe=%
    setx PATH "%PATH%;%PYTHON_DIR%\Scripts;%USERPROFILE%\.local\bin" /M
    echo PATH actualizado correctamente.
) else (
    echo Instalacion completada sin errores.
)

goto :endpoint

:install_python
echo Descargando e instalando Python %PYTHON_VERSION%...
curl -o %INSTALLER_NAME% %INSTALLER_URL%
start /wait %INSTALLER_NAME%
echo "Installed"
:: Pausa para asegurar que la instalación de Python sea reconocida
timeout /t 5 /nobreak

:: Reintentar detectar Python después de la instalación
goto :buscar_python


:endpoint
echo Instalacion completa. Pulsa Enter para salir.
pause
exit /b 0
