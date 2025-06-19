import os
import sys
import urllib.request
import subprocess
import re

# Configurações
pasta_destino = r"C:\cloudflare"
arquivo_exe = "cloudflared.exe"
url_download = "https://raw.githubusercontent.com/Giuseph66/testes_novos/main/clodflare%20/cloudflared.exe"
porta_local = 3000

# Caminho completo do executável
caminho_executavel = os.path.join(pasta_destino, arquivo_exe)

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

try:
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    # 4. Ler a saída e capturar a URL
    for line in process.stdout:
        print(line.strip())
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            url = match.group()
            print(f"\n🔗 URL pública gerada:\n{url}")
            break

except Exception as e:
    print(f"❌ Erro ao executar o túnel: {e}")
    sys.exit(1)
