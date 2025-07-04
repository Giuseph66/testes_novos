import os
import sys
import subprocess
import shutil
import zipfile
import urllib.request

ZIP_URL = "https://github.com/ctp-maker/Expoe/blob/main/acessar.zip?raw=true"

def is_admin():
    """Verifica se está rodando como administrador no Windows."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def check_node():
    """Verifica se o Node.js está instalado."""
    try:
        subprocess.check_call(['node', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def baixar_zip(url, destino):
    print(f"Baixando {url} ...")
    urllib.request.urlretrieve(url, destino)
    print("Download concluído.")

def main():
    if not check_node():
        print("Node.js não está instalado! Execute primeiro o script de instalação do Node.js.")
        sys.exit(1)

    user_dir = os.path.expanduser("~")
    os.chdir(user_dir)
    acessar_dir = os.path.join("C:\\", "acessar")
    server_js = os.path.join(acessar_dir, "server.js")

    if os.path.exists(server_js):
        print(f"O arquivo {server_js} já existe. Pulando download e extração do zip.")
        print("Instalando dependências do projeto...")
        os.chdir(acessar_dir)
        print("Iniciando servidor...")
        try:
            DETACHED = getattr(subprocess, 'DETACHED_PROCESS', 0x00000008)
            with open('server.log', 'w') as log:
                subprocess.Popen(
                    ['node', 'server.js'],
                    cwd=acessar_dir,
                    creationflags=DETACHED,
                    stdout=log,
                    stderr=log,
                    close_fds=True
                )
            print("Servidor iniciado com sucesso!")
        except Exception as e:
            print("Erro ao iniciar o servidor:", e)
        return

    # Caso não exista, faz download e extração normalmente
    if os.path.exists(acessar_dir):
        print("Removendo pasta existente C:\\acessar...")
        shutil.rmtree(acessar_dir, ignore_errors=True)

    zip_path = os.path.join(user_dir, "acessar.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    baixar_zip(ZIP_URL, zip_path)

    print("Descompactando o projeto...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(acessar_dir)

    os.remove(zip_path)
    print("Projeto extraído em C:\\acessar")

    os.chdir(acessar_dir)
    print("Dependências instaladas com sucesso!")
    print("Iniciando servidor...")
    try:
        DETACHED = getattr(subprocess, 'DETACHED_PROCESS', 0x00000008)
        with open('server.log', 'w') as log:
            subprocess.Popen(
                ['node', 'server.js'],
                cwd=acessar_dir,
                creationflags=DETACHED,
                stdout=log,
                stderr=log,
                close_fds=True
            )
        print("Servidor iniciado com sucesso!")
    except Exception as e:
        print("Erro ao iniciar o servidor:", e)

if __name__ == '__main__':
    main()