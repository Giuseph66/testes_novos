import subprocess
import re

# Caminho completo do cloudflared.exe
cloudflared_path = r"C:\cloudflare\cloudflared.exe"

# Porta local do servidor
porta = 3000

# Comando para rodar o túnel
cmd = [cloudflared_path, "tunnel", "--url", f"http://localhost:{porta}"]

print(f"Iniciando túnel na porta {porta}...")

# Executa o processo
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

# Lê a saída em tempo real
url_tunel = None
for line in process.stdout:
    print(line.strip())  # Exibe tudo
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        url_tunel = match.group()
        print("\n🔗 URL pública gerada:")
        print(url_tunel)
        break  # Se quiser parar aqui, remova esta linha se quiser continuar rodando

# (Opcional) Continuar exibindo a saída do processo
for line in process.stdout:
    print(line.strip())

# Você pode encerrar manualmente o processo se quiser:
# process.terminate()
