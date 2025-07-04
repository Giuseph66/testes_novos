@echo off
setlocal

:: 1) Verifica privilégios de administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Este script precisa ser executado como Administrador.
  pause
  exit /b 1
)

:: 2) Verifica se o Node.js já está instalado
where node >nul 2>&1
if %errorLevel% EQU 0 (
  echo Node.js já está instalado. Versão:
  node -v
  goto CONTINUAR
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

:CONTINUAR

echo npm versão:
npm -v

echo.
echo Node.js instalado/verificado com sucesso!

:: 6) Baixa e extrai o repositório do GitHub
echo Baixando repositório do GitHub...
cd /d C:\

:: Remove pasta existente se houver
if exist "acessar" (
  echo Removendo pasta existente...
  rmdir /s /q "acessar"
)

:: Baixa o repositório usando git clone
echo Clonando repositório...
git clone https://github.com/ctp-maker/Expoe.git temp_repo

:: Move a pasta específica para C:\acessar
echo Movendo pasta para C:\acessar...
move "temp_repo\acessos\acessar" "C:\acessar"

:: Remove pasta temporária
echo Limpando arquivos temporários...
rmdir /s /q "temp_repo"

echo Repositório baixado e extraído em C:\acessar

:: 7) Instala dependências do projeto
echo Instalando dependências do projeto...
cd /d C:\acessar
npm install

echo Dependências instaladas com sucesso!

node acessar/server.js

echo Servidor iniciado com sucesso!

pause
