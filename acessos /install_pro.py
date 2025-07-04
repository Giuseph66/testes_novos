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
        input("Pressione Enter para sair...")
        sys.exit(1)

    user_dir = os.path.expanduser("~")
    os.chdir(user_dir)
    if os.path.exists("acessar"):
        print("Removendo pasta existente C:\\acessar...")
        shutil.rmtree("acessar", ignore_errors=True)

    zip_path = os.path.join(user_dir, "acessar.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    baixar_zip(ZIP_URL, zip_path)

    print("Descompactando o projeto...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("C:\\acessar")

    os.remove(zip_path)
    print("Projeto extraído em C:\\acessar")

    print("Instalando dependências do projeto...")
    os.chdir("C:\\acessar")
    try:
        subprocess.check_call(['npm', 'install'])
    except Exception as e:
        print("Erro ao instalar dependências:", e)
        input("Pressione Enter para sair...")
        sys.exit(1)

    print("Dependências instaladas com sucesso!")

    print("Iniciando servidor...")
    try:
        subprocess.Popen(['node', 'acessar/server.js'], cwd="C:\\acessar")
        print("Servidor iniciado com sucesso!")
    except Exception as e:
        print("Erro ao iniciar o servidor:", e)

    input("Pressione Enter para sair...")

if __name__ == '__main__':
    main()
