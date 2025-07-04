import os
import sys
import urllib.request
import subprocess
import re
import requests
import time
import json
# Configurações
pasta_destino = r"C:\cloudflare"
arquivo_exe = "cloudflared.exe"
url_download = "https://raw.githubusercontent.com/Giuseph66/testes_novos/main/clodflare%20/cloudflared.exe"
porta_local = 15966
BASE_URL = 'https://server.neurelix.com.br'  # Sua base URL
nome_maquina = os.getenv('COMPUTERNAME') or os.getenv('HOSTNAME') or 'desconhecido'
nome_maquina = nome_maquina.replace(" ", "_")

caminho_executavel = os.path.join(pasta_destino, arquivo_exe)

REGISTRO_JSON = os.path.join(pasta_destino, 'registro.json')

def criar_registro(name: str, value: str, url: str) -> dict:
    payload = {
        'name': name,
        'value': value,
        'url': url
    }
    resp = requests.post(f'{BASE_URL}/data', json=payload)
    resp.raise_for_status()
    return resp.json()


def atualizar_registro(document_id: str, name: str, value: str, url: str) -> dict:
    payload = {
        'name': name,
        'value': value,
        'url': url
    }
    resp = requests.put(f'{BASE_URL}/data/{document_id}', json=payload)
    resp.raise_for_status()
    return resp.json()

def salvar_id_registro(document_id):
    with open(REGISTRO_JSON, 'w') as f:
        json.dump({'document_id': document_id}, f)

def carregar_id_registro():
    if os.path.exists(REGISTRO_JSON):
        with open(REGISTRO_JSON, 'r') as f:
            data = json.load(f)
            return data.get('document_id')
    return None

# 1. Criar a pasta, se necessário
if not os.path.exists(pasta_destino):
    print(f"📁 Pasta não encontrada. Criando: {pasta_destino}")
    try:
        os.makedirs(pasta_destino)
    except Exception as e:
        print(f"❌ Erro ao criar a pasta: {e}")
        sys.exit(1)

# 2. Baixar o cloudflared.exe, se não existir
if not os.path.isfile(caminho_executavel):
    print(f"⬇️ Baixando cloudflared.exe de:\n{url_download}")
    try:
        urllib.request.urlretrieve(url_download, caminho_executavel)
        print(f"✅ Download concluído: {caminho_executavel}")
    except Exception as e:
        print(f"❌ Erro ao baixar o arquivo: {e}")
        sys.exit(1)
else:
    print(f"✅ Executável já existe: {caminho_executavel}")

# 3. Executar o túnel
cmd = [caminho_executavel, "tunnel", "--url", f"http://localhost:{porta_local}"]
print(f"🚀 Iniciando túnel para localhost:{porta_local}...\n")

creationflags = 0
if os.name == 'nt':
    creationflags = subprocess.CREATE_NO_WINDOW

try:
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd=pasta_destino,
        shell=False,
        creationflags=creationflags
    )

    # 4. Ler a saída e capturar a URL
    for line in process.stdout:
        print(line.strip())
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            url = match.group()
            print(f"\n🔗 URL pública gerada:\n{url}")
            document_id = carregar_id_registro()
            if document_id:
                resp = atualizar_registro(document_id, name=nome_maquina, value=str(time.time()), url=url)
                print("Registro atualizado.")
            else:
                resp = criar_registro(name=nome_maquina, value=str(time.time()), url=url)
                document_id = resp.get('documentId')
                if document_id:
                    salvar_id_registro(document_id)
                    print("Registro criado e id salvo.")    
            print(resp)
            break

except Exception as e:
    print(f"❌ Erro ao executar o túnel: {e}")
    sys.exit(1)

