import cv2
import time
from datetime import datetime
import os

def criar_pasta_fotos():
    """Cria a pasta fotos se não existir."""
    if not os.path.exists("fotos"):
        os.makedirs("fotos")
        print("✅ Pasta 'fotos' criada")

def capturar_foto(cap, contador):
    """Captura e salva uma foto."""
    ret, frame = cap.read()
    if not ret:
        print("❌ Erro ao capturar frame")
        return contador
    
    # Gerar nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"camera_{timestamp}.jpg"
    caminho = os.path.join("fotos", nome_arquivo)
    
    # Salvar foto
    if cv2.imwrite(caminho, frame):
        contador += 1
        print(f"✅ Foto {contador} salva: {nome_arquivo}")
    else:
        print(f"❌ Erro ao salvar foto")
    
    return contador

def main():
    """Função principal do app de câmera."""
    print("=== CAMERA APP SIMPLES ===")
    print("Comandos:")
    print("  [ESPACO] - Tirar foto")
    print("  [ESC] - Sair")
    print("  [C] - Contador regressivo")
    
    # Criar pasta de fotos
    criar_pasta_fotos()
    
    # Inicializar câmera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Erro: Não foi possível abrir a câmera")
        return
    
    # Configurar resolução
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Variáveis
    contador_fotos = 0
    modo_contador = False
    tempo_contador = 0
    tempo_inicio = time.time()
    
    # Criar janela
    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera', 800, 600)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Erro ao capturar vídeo")
                break
            
            # Processar contador regressivo
            if modo_contador:
                tempo_atual = time.time()
                tempo_decorrido = int(tempo_atual - tempo_inicio)
                tempo_restante = tempo_contador - tempo_decorrido
                
                if tempo_restante > 0:
                    # Mostrar contador na tela
                    cv2.putText(frame, f"CONTADOR: {tempo_restante}", 
                               (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
                else:
                    # Capturar foto automaticamente
                    contador_fotos = capturar_foto(cap, contador_fotos)
                    modo_contador = False
                    print("📸 Foto capturada automaticamente!")
            
            # Mostrar informações na tela
            cv2.putText(frame, f"Fotos: {contador_fotos}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if modo_contador:
                cv2.putText(frame, "Modo Contador Ativo", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Mostrar comandos na tela
            cv2.putText(frame, "ESPACO: Foto | C: Contador | ESC: Sair", 
                       (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Camera', frame)
            
            # Processar teclas
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # ESPAÇO
                contador_fotos = capturar_foto(cap, contador_fotos)
            elif key == ord('c') or key == ord('C'):
                if not modo_contador:
                    modo_contador = True
                    tempo_contador = 3  # 3 segundos
                    tempo_inicio = time.time()
                    print("⏰ Contador iniciado: 3 segundos")
                else:
                    modo_contador = False
                    print("❌ Contador cancelado")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\n📸 Total de fotos tiradas: {contador_fotos}")
        print(f"📁 Fotos salvas em: {os.path.abspath('fotos')}")

if __name__ == "__main__":
    main() 