import cv2
import numpy as np
import time
from datetime import datetime
import os
from PIL import Image
import pyttsx3
import threading

class SistemaFacialVoz:
    def __init__(self):
        self.cap = None
        self.face_cascade = None
        self.eye_cascade = None
        
        # Inicializar síntese de voz
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Velocidade da fala
        self.engine.setProperty('volume', 0.8)  # Volume
        
        # Configurar voz em português se disponível
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'pt' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Carregar classificadores Haar
        self.carregar_classificadores()
        
        # Faces de referência
        self.faces_referencia = []
        self.nomes_referencia = []
        
        # Otimizações
        self.frame_skip = 2
        self.frame_count = 0
        
        # Métricas
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.fps = 0
        self.faces_detectadas = 0
        self.reconhecimentos_corretos = 0
        
        # Configurações
        self.tolerance = 0.7
        self.modo_detalhado = False
        self.voz_ativa = True
        
        # Controle de voz
        self.ultima_pessoa_falada = None
        self.tempo_ultima_fala = 0
        self.intervalo_fala = 3.0  # Segundos entre falas da mesma pessoa
        
        # Resultados do frame anterior
        self.last_face_locations = []
        self.last_face_names = []
        self.last_face_confidences = []
        
        # Inicializar
        self.inicializar_camera()
        self.carregar_faces_referencia()
        
        # Testar voz
        self.falar("Sistema de reconhecimento facial ativado")
    
    def carregar_classificadores(self):
        """Carrega classificadores Haar para detecção facial."""
        try:
            # Classificador principal para faces
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Classificador para olhos (para validação)
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            
            if self.face_cascade.empty():
                print("❌ Erro: Não foi possível carregar o classificador de faces")
            else:
                print("✅ Classificadores carregados com sucesso")
                
        except Exception as e:
            print(f"❌ Erro ao carregar classificadores: {e}")
    
    def falar(self, texto):
        """Fala o texto fornecido usando síntese de voz."""
        if not self.voz_ativa:
            return
            
        try:
            # Executar em thread separada para não bloquear o vídeo
            def falar_thread():
                try:
                    self.engine.say(texto)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"⚠️ Erro na síntese de voz: {e}")
            
            thread = threading.Thread(target=falar_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            print(f"⚠️ Erro ao iniciar síntese de voz: {e}")
    
    def anunciar_pessoa(self, nome, confianca):
        """Anuncia a pessoa reconhecida se for nova ou após intervalo."""
        tempo_atual = time.time()
        
        # Verificar se é uma pessoa nova ou se passou tempo suficiente
        if (nome != self.ultima_pessoa_falada or 
            tempo_atual - self.tempo_ultima_fala > self.intervalo_fala):
            
            if nome == "Desconhecido":
                mensagem = "Pessoa desconhecida detectada"
            else:
                confianca_percent = int(confianca * 100)
                mensagem = f"{nome} detectado com {confianca_percent} por cento de confiança"
            
            self.falar(mensagem)
            self.ultima_pessoa_falada = nome
            self.tempo_ultima_fala = tempo_atual
    
    def inicializar_camera(self):
        """Inicializa a câmera com configurações otimizadas."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Erro: Não foi possível abrir a câmera")
            return False
        
        # Configurações otimizadas
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        return True
    
    def carregar_faces_referencia(self):
        """Carrega faces de referência usando OpenCV."""
        pasta_fotos = "fotos"
        if not os.path.exists(pasta_fotos):
            print(f"❌ Pasta '{pasta_fotos}' não encontrada")
            return
        
        arquivos_foto = [f for f in os.listdir(pasta_fotos) if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not arquivos_foto:
            print(f"❌ Nenhuma foto encontrada em '{pasta_fotos}'")
            return
        
        print(f"🔍 Carregando {len(arquivos_foto)} faces de referência...")
        
        for i, arquivo in enumerate(arquivos_foto):
            try:
                caminho = os.path.join(pasta_fotos, arquivo)
                print(f"  📸 Carregando: {arquivo}")
                
                # Carregar imagem
                imagem = cv2.imread(caminho)
                if imagem is None:
                    print(f"    ❌ Não foi possível carregar {arquivo}")
                    continue
                
                # Converter para escala de cinza
                gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                
                # Detectar faces
                faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5, 
                    minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    # Usar a primeira face encontrada
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # Redimensionar para tamanho padrão
                    face_roi = cv2.resize(face_roi, (100, 100))
                    
                    # Calcular histograma como descritor
                    hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                    hist = cv2.normalize(hist, hist).flatten()
                    
                    self.faces_referencia.append(hist)
                    nome = f"Pessoa_{i+1}"
                    self.nomes_referencia.append(nome)
                    print(f"    ✅ Face detectada: {nome}")
                else:
                    print(f"    ❌ Nenhuma face detectada em {arquivo}")
                    
            except Exception as e:
                print(f"    ❌ Erro ao processar {arquivo}: {e}")
        
        print(f"✅ Total de faces carregadas: {len(self.faces_referencia)}")
        
        # Anunciar carregamento
        if self.faces_referencia:
            self.falar(f"Carregadas {len(self.faces_referencia)} pessoas de referência")
    
    def detectar_faces_opencv(self, frame):
        """Detecta faces usando OpenCV."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        return faces, gray
    
    def comparar_faces(self, face_roi):
        """Compara uma face com as faces de referência."""
        if not self.faces_referencia:
            return "Desconhecido", 0.0
        
        # Redimensionar para tamanho padrão
        face_roi = cv2.resize(face_roi, (100, 100))
        
        # Calcular histograma
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        # Comparar com todas as faces de referência
        melhores_matches = []
        
        for i, ref_hist in enumerate(self.faces_referencia):
            # Calcular correlação
            correlation = cv2.compareHist(hist, ref_hist, cv2.HISTCMP_CORREL)
            
            # Calcular distância Chi-quadrado
            chi_square = cv2.compareHist(hist, ref_hist, cv2.HISTCMP_CHISQR)
            
            # Calcular distância Bhattacharyya
            bhattacharyya = cv2.compareHist(hist, ref_hist, cv2.HISTCMP_BHATTACHARYYA)
            
            # Combinar métricas (correlação alta = boa, chi_square baixo = bom, bhattacharyya baixo = bom)
            score = (correlation + (1 - chi_square/1000) + (1 - bhattacharyya)) / 3
            melhores_matches.append((score, i))
        
        # Encontrar melhor match
        melhores_matches.sort(reverse=True)
        melhor_score, melhor_indice = melhores_matches[0]
        
        if melhor_score >= self.tolerance:
            nome = self.nomes_referencia[melhor_indice]
            self.reconhecimentos_corretos += 1
        else:
            nome = "Desconhecido"
        
        return nome, melhor_score
    
    def processar_frame(self, frame):
        """Processa frame principal."""
        self.frame_count += 1
        
        # Processar apenas frames alternados
        if self.frame_count % self.frame_skip == 0:
            faces, gray = self.detectar_faces_opencv(frame)
            
            face_locations = []
            face_names = []
            face_confidences = []
            
            for (x, y, w, h) in faces:
                # Extrair ROI da face
                face_roi = gray[y:y+h, x:x+w]
                
                # Comparar com faces de referência
                nome, confianca = self.comparar_faces(face_roi)
                
                face_locations.append((y, x+w, y+h, x))  # (top, right, bottom, left)
                face_names.append(nome)
                face_confidences.append(confianca)
                
                # Anunciar pessoa se confiança alta
                if confianca > 0.8:
                    self.anunciar_pessoa(nome, confianca)
            
            # Salvar resultados para próximo frame
            self.last_face_locations = face_locations
            self.last_face_names = face_names
            self.last_face_confidences = face_confidences
        else:
            # Usar resultados do frame anterior
            face_locations = self.last_face_locations
            face_names = self.last_face_names
            face_confidences = self.last_face_confidences
        
        # Desenhar resultados
        for i, ((top, right, bottom, left), name, confidence) in enumerate(zip(face_locations, face_names, face_confidences)):
            # Escolher cor baseada no reconhecimento
            if name == "Desconhecido":
                cor = (0, 0, 255)  # Vermelho
            else:
                cor = (0, 255, 0)  # Verde
            
            # Desenhar retângulo
            cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
            
            # Desenhar nome e confiança
            texto = f"{name} ({confidence:.2f})"
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
            cv2.putText(frame, texto, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Modo detalhado: detectar olhos
            if self.modo_detalhado and self.eye_cascade:
                roi_gray = gray[top:bottom, left:right]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(frame, (left + ex, top + ey), (left + ex + ew, top + ey + eh), (255, 255, 0), 1)
        
        return frame, face_locations, face_names, face_confidences
    
    def calcular_fps(self):
        """Calcula e atualiza FPS."""
        self.fps_counter += 1
        if self.fps_counter >= 30:
            tempo_atual = time.time()
            self.fps = self.fps_counter / (tempo_atual - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = tempo_atual
    
    def capturar_foto_referencia(self, frame):
        """Captura uma nova foto de referência."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"camera_{timestamp}.jpg"
        caminho = os.path.join("fotos", nome_arquivo)
        
        if cv2.imwrite(caminho, frame):
            print(f"✅ Nova foto de referência salva: {nome_arquivo}")
            self.falar("Nova foto de referência capturada")
            
            # Recarregar faces de referência
            self.faces_referencia = []
            self.nomes_referencia = []
            self.carregar_faces_referencia()
            return True
        else:
            print(f"❌ Erro ao salvar foto de referência")
            return False
    
    def mostrar_painel_info(self, frame):
        """Mostra painel com informações do sistema."""
        altura, largura = frame.shape[:2]
        
        # Painel de informações
        info_panel = np.zeros((220, largura, 3), dtype=np.uint8)
        info_panel[:] = (40, 40, 40)
        
        # Informações básicas
        cv2.putText(info_panel, f"FPS: {self.fps:.1f}", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Faces: {len(self.last_face_locations)}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Tolerancia: {self.tolerance}", (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(info_panel, f"Referencias: {len(self.faces_referencia)}", (20, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Status da voz
        status_voz = "ON" if self.voz_ativa else "OFF"
        cor_voz = (0, 255, 0) if self.voz_ativa else (0, 0, 255)
        cv2.putText(info_panel, f"Voz: {status_voz}", (20, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_voz, 2)
        
        # Estatísticas
        if self.faces_detectadas > 0:
            taxa_reconhecimento = (self.reconhecimentos_corretos / self.faces_detectadas) * 100
            cv2.putText(info_panel, f"Taxa Reconhecimento: {taxa_reconhecimento:.1f}%", (20, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Comandos
        cv2.putText(info_panel, "R: Nova Ref | T: Tolerancia | D: Detalhes | V: Voz | ESC: Sair", (20, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Combinar com frame principal
        frame_completo = np.vstack([frame, info_panel])
        return frame_completo
    
    def executar(self):
        """Executa o sistema com voz."""
        if not self.cap:
            print("❌ Câmera não inicializada")
            return
        
        if self.face_cascade is None or self.face_cascade.empty():
            print("❌ Classificadores não carregados")
            return
        
        print("=== SISTEMA DE RECONHECIMENTO FACIAL COM VOZ ===")
        print("Comandos:")
        print("  [R] - Capturar nova foto de referência")
        print("  [T] - Ajustar tolerância")
        print("  [D] - Alternar modo detalhado")
        print("  [V] - Ativar/Desativar voz")
        print("  [ESC] - Sair")
        print(f"Tolerância atual: {self.tolerance}")
        
        # Criar janela
        cv2.namedWindow('Sistema Facial com Voz', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Sistema Facial com Voz', 1000, 800)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Erro ao capturar frame")
                    break
                
                # Processar frame
                frame_processado, face_locations, face_names, face_confidences = self.processar_frame(frame)
                
                # Atualizar contadores
                self.faces_detectadas += len(face_locations)
                
                # Calcular FPS
                self.calcular_fps()
                
                # Mostrar painel de informações
                frame_final = self.mostrar_painel_info(frame_processado)
                
                cv2.imshow('Sistema Facial com Voz', frame_final)
                
                # Processar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
                elif key == ord('r') or key == ord('R'):
                    self.capturar_foto_referencia(frame)
                elif key == ord('t') or key == ord('T'):
                    # Ajustar tolerância
                    nova_tolerancia = input(f"Digite nova tolerância (0.1-1.0) [atual: {self.tolerance}]: ")
                    try:
                        self.tolerance = float(nova_tolerancia)
                        self.tolerance = max(0.1, min(1.0, self.tolerance))
                        print(f"✅ Tolerância ajustada para: {self.tolerance}")
                        self.falar(f"Tolerância ajustada para {self.tolerance}")
                    except ValueError:
                        print("❌ Valor inválido. Tolerância mantida.")
                elif key == ord('d') or key == ord('D'):
                    self.modo_detalhado = not self.modo_detalhado
                    status = "ON" if self.modo_detalhado else "OFF"
                    print(f"🔍 Modo detalhado: {status}")
                    self.falar(f"Modo detalhado {status}")
                elif key == ord('v') or key == ord('V'):
                    self.voz_ativa = not self.voz_ativa
                    status = "ativada" if self.voz_ativa else "desativada"
                    print(f"🔊 Voz: {status}")
                    if self.voz_ativa:
                        self.falar("Voz ativada")
                
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            self.falar("Sistema encerrado")
            print("👋 Sistema encerrado")
            print(f"📊 Estatísticas finais:")
            print(f"   - Faces detectadas: {self.faces_detectadas}")
            print(f"   - Reconhecimentos corretos: {self.reconhecimentos_corretos}")
            if self.faces_detectadas > 0:
                taxa = (self.reconhecimentos_corretos / self.faces_detectadas) * 100
                print(f"   - Taxa de reconhecimento: {taxa:.1f}%")

def main():
    """Função principal."""
    sistema = SistemaFacialVoz()
    sistema.executar()

if __name__ == "__main__":
    main() 