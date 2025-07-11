import cv2
import numpy as np
import time
from datetime import datetime
import os

class CameraApp:
    def __init__(self):
        self.cap = None
        self.foto_count = 0
        self.pasta_fotos = "fotos"
        self.contador_tempo = 0
        self.modo_contador = False
        self.delay_contador = 3  # segundos
        
        # Criar pasta de fotos se não existir
        if not os.path.exists(self.pasta_fotos):
            os.makedirs(self.pasta_fotos)
        
        # Inicializar câmera
        self.inicializar_camera()
        
        # Configurações da interface
        self.largura_janela = 1200
        self.altura_janela = 800
        self.largura_painel = 300
        
    def inicializar_camera(self):
        """Inicializa a câmera com verificações de erro."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro: Não foi possível abrir a câmera")
            return False
        
        # Configurar resolução
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return True
    
    def criar_painel_controles(self, frame):
        """Cria o painel de controles ao lado da imagem."""
        altura, largura = frame.shape[:2]
        painel = np.zeros((altura, self.largura_painel, 3), dtype=np.uint8)
        painel[:] = (40, 40, 40)  # Cor de fundo escura
        
        # Título
        cv2.putText(painel, "CAMERA APP", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1.2, (255, 255, 0), 2)
        
        # Informações
        cv2.putText(painel, f"Fotos tiradas: {self.foto_count}", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Contador regressivo
        if self.modo_contador and self.contador_tempo > 0:
            cv2.putText(painel, f"Contador: {self.contador_tempo}", (20, 140), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        
        # Botões
        self.desenhar_botao(painel, "CAPTURAR", (20, 200, 260, 50), (0, 255, 0))
        self.desenhar_botao(painel, "CONTADOR 3s", (20, 270, 260, 50), (255, 165, 0))
        self.desenhar_botao(painel, "CONTADOR 5s", (20, 340, 260, 50), (255, 165, 0))
        self.desenhar_botao(painel, "CANCELAR", (20, 410, 260, 50), (0, 0, 255))
        
        # Comandos de teclado
        cv2.putText(painel, "Comandos:", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 1)
        cv2.putText(painel, "[ESPACO] - Capturar", (20, 530), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(painel, "[3] - Contador 3s", (20, 550), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(painel, "[5] - Contador 5s", (20, 570), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(painel, "[ESC] - Sair", (20, 590), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return painel
    
    def desenhar_botao(self, img, texto, coords, cor):
        """Desenha um botão no painel."""
        x, y, w, h = coords
        cv2.rectangle(img, (x, y), (x+w, y+h), cor, 2)
        cv2.rectangle(img, (x+2, y+2), (x+w-2, y+h-2), (60, 60, 60), -1)
        
        # Centralizar texto
        (text_width, text_height), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        text_x = x + (w - text_width) // 2
        text_y = y + (h + text_height) // 2
        
        cv2.putText(img, texto, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)
    
    def verificar_clique_botao(self, x, y):
        """Verifica se um botão foi clicado."""
        if x < self.largura_painel:  # Clique no painel
            if 200 <= y <= 250:  # Botão CAPTURAR
                return "capturar"
            elif 270 <= y <= 320:  # Botão CONTADOR 3s
                return "contador_3"
            elif 340 <= y <= 390:  # Botão CONTADOR 5s
                return "contador_5"
            elif 410 <= y <= 460:  # Botão CANCELAR
                return "cancelar"
        return None
    
    def capturar_foto(self):
        """Captura uma foto da câmera."""
        ret, frame = self.cap.read()
        if not ret:
            return False
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"camera_{timestamp}.jpg"
        caminho_completo = os.path.join(self.pasta_fotos, nome_arquivo)
        
        # Salvar foto
        if cv2.imwrite(caminho_completo, frame):
            self.foto_count += 1
            print(f"✅ Foto salva: {caminho_completo}")
            return True
        else:
            print(f"❌ Erro ao salvar foto: {caminho_completo}")
            return False
    
    def iniciar_contador(self, segundos):
        """Inicia o contador regressivo."""
        self.modo_contador = True
        self.contador_tempo = segundos
        print(f"⏰ Contador iniciado: {segundos} segundos")
    
    def cancelar_contador(self):
        """Cancela o contador regressivo."""
        self.modo_contador = False
        self.contador_tempo = 0
        print("❌ Contador cancelado")
    
    def atualizar_contador(self):
        """Atualiza o contador regressivo."""
        if self.modo_contador and self.contador_tempo > 0:
            self.contador_tempo -= 1
            if self.contador_tempo == 0:
                # Capturar foto automaticamente
                self.capturar_foto()
                self.modo_contador = False
                print("📸 Foto capturada automaticamente!")
    
    def processar_frame(self, frame):
        """Processa o frame para exibição."""
        # Redimensionar frame para caber na janela
        altura, largura = frame.shape[:2]
        nova_largura = self.largura_janela - self.largura_painel
        nova_altura = int(altura * nova_largura / largura)
        frame_redimensionado = cv2.resize(frame, (nova_largura, nova_altura))
        
        # Criar painel de controles
        painel = self.criar_painel_controles(frame_redimensionado)
        
        # Combinar frame e painel
        frame_completo = np.hstack([frame_redimensionado, painel])
        
        return frame_completo
    
    def executar(self):
        """Executa o aplicativo da câmera."""
        if not self.cap:
            print("Erro: Câmera não inicializada")
            return
        
        print("=== CAMERA APP ===")
        print("Comandos:")
        print("  [ESPACO] - Capturar foto")
        print("  [3] - Contador 3 segundos")
        print("  [5] - Contador 5 segundos")
        print("  [ESC] - Sair")
        print("  Clique nos botões para usar")
        
        # Configurar callback do mouse
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                acao = self.verificar_clique_botao(x, y)
                if acao == "capturar":
                    self.capturar_foto()
                elif acao == "contador_3":
                    self.iniciar_contador(3)
                elif acao == "contador_5":
                    self.iniciar_contador(5)
                elif acao == "cancelar":
                    self.cancelar_contador()
        
        # Criar janela e configurar callback
        cv2.namedWindow('Camera App', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Camera App', mouse_callback)
        cv2.resizeWindow('Camera App', self.largura_janela, self.altura_janela)
        
        tempo_anterior = time.time()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Erro ao capturar frame")
                    break
                
                # Atualizar contador a cada segundo
                tempo_atual = time.time()
                if tempo_atual - tempo_anterior >= 1.0:
                    self.atualizar_contador()
                    tempo_anterior = tempo_atual
                
                # Processar e exibir frame
                frame_processado = self.processar_frame(frame)
                cv2.imshow('Camera App', frame_processado)
                
                # Processar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
                elif key == 32:  # ESPAÇO
                    self.capturar_foto()
                elif key == ord('3'):
                    self.iniciar_contador(3)
                elif key == ord('5'):
                    self.iniciar_contador(5)
                elif key == ord('c') or key == ord('C'):
                    self.cancelar_contador()
                
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            print(f"\n📸 Total de fotos tiradas: {self.foto_count}")
            print(f"📁 Fotos salvas em: {os.path.abspath(self.pasta_fotos)}")

def main():
    """Função principal."""
    app = CameraApp()
    app.executar()

if __name__ == "__main__":
    main() 