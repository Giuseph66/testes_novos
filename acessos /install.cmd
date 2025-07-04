@echo off
setlocal

:: 1) Verifica privilégios de administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
  echo ⚠️  Este script precisa ser executado como Administrador.
  pause
  exit /b 1
)

:: 2) Garante TLS 1.2 para download via PowerShell
echo 🔧 Configurando TLS 1.2...
powershell -NoProfile -Command ^
  "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12"

:: 3) Instala Chocolatey se não existir
where choco >nul 2>&1
if %errorLevel% NEQ 0 (
  echo 🍫 Instalando Chocolatey...
  powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command ^
    "Set-ExecutionPolicy Bypass -Scope Process -Force; ^
     iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
) else (
  echo 🍫 Chocolatey já instalado.
)

:: 4) Verifica se o Node.js já está instalado
where node >nul 2>&1
if %errorLevel% EQU 0 (
  echo ✅ Node.js já está instalado. Versão:
  node -v
) else (
  echo ⬇️ Instalando Node.js LTS...
  choco install nodejs-lts -y
  echo 🔄 Atualizando variáveis de ambiente...
  call "%AllUsersProfile%\chocolatey\bin\refreshenv.cmd"
)

echo ✅ npm versão:
npm -v

echo.
echo Node.js instalado/verificado com sucesso!



pause
