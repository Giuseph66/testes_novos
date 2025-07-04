@echo off
setlocal

:: 1) Verifica privilégios de administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Este script precisa ser executado como Administrador.
  pause
  exit /b 1
)

:: 2) Verifica se o Node.js está instalado
where node >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Node.js não está instalado! Execute primeiro o script instalar_node.cmd.
  pause
  exit /b 1
)

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
echo Criando pasta de destino...
mkdir "C:\acessar"
echo Movendo pasta para C:\acessar...
move "temp_repo\acessos\acessar" "C:\\"

:: Remove pasta temporária
echo Limpando arquivos temporários...
rmdir /s /q "temp_repo"

echo Repositório baixado e extraído em C:\acessar

echo Instalando dependências do projeto...
cd /d C:\acessar
npm install

echo Dependências instaladas com sucesso!

node acessar/server.js

echo Servidor iniciado com sucesso!

pause
