@echo off
setlocal

:: Verifica se o PowerShell está disponível
where powershell >nul 2>nul
if errorlevel 1 (
    echo ERRO: PowerShell nao encontrado no sistema. Nao eh possivel continuar.
    pause
    exit /b 1
)

set "PASTA=C:\FerramentasExpoe"

:: Cria a pasta se não existir
if not exist "%PASTA%" (
    mkdir "%PASTA%"
)

cd /d "%PASTA%"

:: Baixa os arquivos
echo Baixando install.cmd...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Giuseph66/testes_novos/raw/main/acessos%20/install.cmd' -OutFile 'install.cmd'"

echo Baixando abre_server.exe...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Giuseph66/testes_novos/raw/main/acessos%20/abre_server.exe' -OutFile 'abre_server.exe'"

echo Baixando url_gerate.exe...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Giuseph66/testes_novos/raw/main/clodflare%20/url_gerate.exe' -OutFile 'url_gerate.exe'"

:: Executa os arquivos na ordem
echo Executando install.cmd...
call "%PASTA%\install.cmd"

echo Executando abre_server.exe...
start /wait "" "%PASTA%\abre_server.exe"

echo Executando url_gerate.exe...
start /wait "" "%PASTA%\url_gerate.exe"

:: Adiciona os programas ao autostart do usuário atual
echo Adicionando ao autostart...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ExpoeServer /t REG_SZ /d "\"%PASTA%\abre_server.exe\"" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ExpoeCloudflare /t REG_SZ /d "\"%PASTA%\url_gerate.exe\"" /f

echo.
echo Tudo pronto! Os programas serao executados automaticamente ao iniciar o Windows.
pause