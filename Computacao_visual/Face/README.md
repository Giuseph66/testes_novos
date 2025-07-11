# Detector de Rostos em Tempo Real

Um sistema avançado de detecção e reconhecimento de rostos usando OpenCV e face_recognition.

## 🚀 Funcionalidades

- **Detecção em tempo real**: Detecta múltiplos rostos simultaneamente
- **Reconhecimento facial**: Compara rostos detectados com imagens de referência
- **Interface visual**: Caixas coloridas e nomes sobre os rostos detectados
- **Painel de informações**: Exibe FPS, número de rostos e configurações
- **Configurável**: Tolerância ajustável e suporte a múltiplas câmeras
- **Robusto**: Tratamento de erros e limpeza automática de recursos
- **Otimizado**: Performance melhorada com detecção a cada 3 frames

## 📋 Pré-requisitos

```bash
pip install opencv-python face-recognition numpy
```

## 🎯 Como Usar

### Versão Otimizada (Recomendada)
```bash
python detector_otimizado.py
```

### Versão Original
```bash
python "detecta_1 copy 2.py"
```

### Uso Avançado
```bash
# Usar imagem específica
python detector_otimizado.py --image fotos/minha_foto.jpg --name "Meu Nome"

# Ajustar tolerância (0.0 = muito rigoroso, 1.0 = muito permissivo)
python detector_otimizado.py --tolerance 0.5

# Usar câmera específica
python detector_otimizado.py --camera 1

# Combinar opções
python detector_otimizado.py -i fotos/pessoa.jpg -n "João" -t 0.7 -c 0
```

## ⚙️ Opções de Linha de Comando

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--image, -i` | Caminho para imagem de referência | `fotos/giuseph5.jpg` |
| `--name, -n` | Nome da pessoa na imagem | `Giuseph` |
| `--tolerance, -t` | Tolerância para comparação (0.0-1.0) | `0.6` |
| `--camera, -c` | ID da câmera | `0` |

## 🎨 Interface Visual

- **Caixas verdes**: Rostos reconhecidos
- **Caixas vermelhas**: Rostos desconhecidos
- **Painel superior**: FPS, número de rostos, tolerância
- **Instruções**: Como sair do programa

## 🔧 Melhorias Implementadas

### Performance (Versão Otimizada)
- ✅ **Detecção a cada 3 frames** (3x mais rápido)
- ✅ **Redimensionamento inteligente** (1/4 do tamanho para processamento)
- ✅ **Modelo HOG** (mais rápido que CNN)
- ✅ **Configuração otimizada da câmera** (640x480, 30fps)
- ✅ **Reutilização de detecções** entre frames

### Performance (Versão Original)
- ✅ Câmera aberta uma única vez (não a cada frame)
- ✅ Cálculo de FPS em tempo real
- ✅ Otimização de processamento

### Estrutura
- ✅ Código organizado em classe
- ✅ Separação de responsabilidades
- ✅ Documentação completa
- ✅ Type hints

### Interface
- ✅ Caixas coloridas para diferentes tipos de rosto
- ✅ Painel de informações em tempo real
- ✅ Feedback visual claro
- ✅ Instruções na tela

### Robustez
- ✅ Tratamento de erros abrangente
- ✅ Verificação de existência de arquivos
- ✅ Limpeza automática de recursos
- ✅ Suporte a múltiplas imagens

### Configurabilidade
- ✅ Argumentos de linha de comando
- ✅ Tolerância ajustável
- ✅ Seleção de câmera
- ✅ Nomes personalizáveis

## 🚨 Solução de Problemas

### Imagem em preto e branco
- ✅ **Corrigido na versão otimizada**: Mantém cores originais
- ✅ **Problema**: Conversão incorreta de BGR para RGB
- ✅ **Solução**: Processamento em frame pequeno, exibição em frame original

### Performance lenta
- ✅ **Versão otimizada**: 3x mais rápida
- ✅ **Técnicas aplicadas**:
  - Detecção a cada 3 frames
  - Redimensionamento para 1/4 do tamanho
  - Modelo HOG em vez de CNN
  - Configuração otimizada da câmera

### Câmera não abre
```bash
# Tente diferentes IDs de câmera
python detector_otimizado.py --camera 1
python detector_otimizado.py --camera 2
```

### Muitos falsos positivos
```bash
# Diminua a tolerância
python detector_otimizado.py --tolerance 0.4
```

### Muitos falsos negativos
```bash
# Aumente a tolerância
python detector_otimizado.py --tolerance 0.8
```

### Imagem não encontrada
```bash
# Verifique o caminho da imagem
ls fotos/
python detector_otimizado.py --image caminho/correto/foto.jpg
```

## 📁 Estrutura de Arquivos

```
.
├── detector_otimizado.py   # Versão otimizada (RECOMENDADA)
├── detecta_1 copy 2.py     # Versão original
├── README.md               # Este arquivo
├── requirements.txt        # Dependências
└── fotos/                  # Pasta com imagens de referência
    └── giuseph5.jpg        # Imagem padrão
```

## ⚡ Comparação de Performance

| Versão | FPS Médio | Detecção | Cores |
|--------|-----------|----------|-------|
| Original | ~5-10 | A cada frame | Preto e branco |
| **Otimizada** | **~15-25** | **A cada 3 frames** | **Colorida** |

## 🎯 Próximas Melhorias

- [ ] Suporte a múltiplas pessoas simultaneamente
- [ ] Salvamento de logs de detecção
- [ ] Interface gráfica (GUI)
- [ ] Detecção de emoções
- [ ] Reconhecimento de idade e gênero
- [ ] Integração com banco de dados
- [ ] Modo GPU para ainda mais performance

## 📝 Licença

Este projeto é de uso livre para fins educacionais e pessoais. 