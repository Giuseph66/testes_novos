# Expoe

O **Expoe** é um sistema para gerenciamento e exposição de acessos e serviços em ambientes de TI, pensado para facilitar a administração, monitoramento e publicação de endpoints internos de forma segura e prática.

## Funcionalidades principais
- Exposição de serviços locais via Cloudflare Tunnel
- Registro e atualização automática de URLs públicas
- Interface web para visualização de status e informações do sistema
- Instalação automatizada para Windows

## Requisitos
- Windows 10 ou superior
- Node.js LTS (instalador incluso no script)
- Git (opcional, caso use o script de clonagem)
- Python 3 (caso use o instalador em Python)

## Instalação
1. **Baixe o instalador** (arquivo `.cmd` ou `.py` fornecido no repositório)
2. Execute como administrador
3. O script irá instalar o Node.js (se necessário), baixar o projeto, instalar dependências e iniciar o servidor automaticamente

## Como usar
- Após a instalação, o servidor será iniciado automaticamente
- Acesse a interface web pelo navegador em `http://localhost:15966` (ou porta configurada)
- Siga as instruções na tela para expor serviços ou monitorar o sistema

## Observações
- O projeto pode ser facilmente adaptado para outros sistemas operacionais
- Para dúvidas ou sugestões, abra uma issue no repositório

---
Desenvolvido por ctp-maker
