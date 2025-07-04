@echo off
setlocal

:: 1) Verifica privilégios de administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Este script precisa ser executado como Administrador.
  exit /b 1
)

:: 2) Verifica se o Node.js já está instalado
where node >nul 2>&1
if %errorLevel% EQU 0 (
  echo Node.js já está instalado. Versão:
  node -v
  echo.
  echo Pronto! Agora execute o script instalar_pro.exe para continuar.
  exit /b 0
)

:: 3) Garante TLS 1.2 para download via PowerShell
echo Configurando TLS 1.2...
powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12"

:: 4) Instala Chocolatey se não existir
where choco >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Instalando Chocolatey...
  powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
  timeout /t 5
  call "%AllUsersProfile%\chocolatey\bin\refreshenv.cmd"
) else (
  echo Chocolatey já instalado.
  call "%AllUsersProfile%\chocolatey\bin\refreshenv.cmd"
)

:: 5) Instala Node.js LTS
echo Instalando Node.js LTS...
choco install nodejs-lts -y
call "%AllUsersProfile%\chocolatey\bin\refreshenv.cmd"

echo.
echo Node.js instalado/verificado com sucesso!
echo.
echo Agora execute o script instalar_projeto.cmd para continuar
