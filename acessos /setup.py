import os
import sys
import subprocess
import urllib.request
import shutil
import time
import winreg

PASTA = r'C:\FerramentasExpoe'
ARQUIVOS = [
    ('https://github.com/Giuseph66/testes_novos/raw/main/acessos%20/install.cmd', 'install.cmd'),
    ('https://github.com/Giuseph66/testes_novos/raw/main/acessos%20/abre_server.exe', 'abre_server.exe'),
    ('https://github.com/Giuseph66/testes_novos/raw/main/clodflare%20/url_gerate.exe', 'url_gerate.exe'),
]
AUTOSTART = [
    ('ExpoeServer', 'abre_server.exe'),
    ('ExpoeCloudflare', 'url_gerate.exe'),
]


def criar_pasta():
    if not os.path.exists(PASTA):
        os.makedirs(PASTA)
        print(f'Pasta criada: {PASTA}')
    else:
        print(f'Pasta já existe: {PASTA}')

def baixar_arquivo(url, destino):
    for tentativa in range(2):
        try:
            print(f'Baixando {destino}...')
            with urllib.request.urlopen(url, timeout=30) as response, open(destino, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print(f'{destino} baixado com sucesso!')
            return True
        except Exception as e:
            print(f'Erro ao baixar {destino}: {e}')
            if tentativa == 0:
                print('Tentando novamente em 3 segundos...')
                time.sleep(3)
    return False

def executar_arquivo(caminho, wait=True):
    try:
        print(f'Executando {caminho}...')
        if wait:
            subprocess.run([caminho], check=True)
        else:
            subprocess.Popen([caminho], creationflags=subprocess.DETACHED_PROCESS)
    except Exception as e:
        print(f'Erro ao executar {caminho}: {e}')

def adicionar_autostart(nome, exe):
    caminho = os.path.join(PASTA, exe)
    chave = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave, 0, winreg.KEY_SET_VALUE) as regkey:
            winreg.SetValueEx(regkey, nome, 0, winreg.REG_SZ, f'"{caminho}"')
        print(f'Adicionado ao autostart: {nome}')
    except Exception as e:
        print(f'Erro ao adicionar {nome} ao autostart: {e}')

def main():
    criar_pasta()
    os.chdir(PASTA)
    for url, nome in ARQUIVOS:
        if not baixar_arquivo(url, nome):
            print(f'Falha definitiva ao baixar {nome}. Encerrando.')
            sys.exit(1)
    executar_arquivo(os.path.join(PASTA, 'install.cmd'))
    executar_arquivo(os.path.join(PASTA, 'abre_server.exe'))
    executar_arquivo(os.path.join(PASTA, 'url_gerate.exe'))
    for nome, exe in AUTOSTART:
        adicionar_autostart(nome, exe)
    print('\nTudo pronto! Os programas serao executados automaticamente ao iniciar o Windows.')
    input('Pressione Enter para sair...')

if __name__ == '__main__':
    main()
