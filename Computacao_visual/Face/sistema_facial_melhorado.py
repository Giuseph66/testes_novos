import cv2
import face_recognition
import numpy as np
import time
from datetime import datetime
import os
import json
import logging
from typing import List, Tuple, Optional, Dict
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_facial.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConfiguracaoSistema:
    """Gerencia configurações do sistema."""
    
    def __init__(self, arquivo_config: str = "config.json"):
        self.arquivo_config = arquivo_config
        self.config_padrao = {
            "tolerance": 0.6,
            "frame_skip": 3,
            "camera_width": 640,
            "camera_height": 480,
            "camera_fps": 30,
            "modo_detalhado": True,
            "pasta_fotos": "fotos",
            "interface_tema": "dark"
        }
        self.config = self.carregar_configuracao()
    
    def carregar_configuracao(self) -> Dict:
        try:
            if os.path.exists(self.arquivo_config):
                with open(self.arquivo_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**self.config_padrao, **config}
            else:
                self.salvar_configuracao(self.config_padrao)
                return self.config_padrao
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return self.config_padrao
    
    def salvar_configuracao(self, config: Dict) -> bool:
        try:
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def atualizar_configuracao(self, chave: str, valor) -> bool:
        self.config[chave] = valor
        return self.salvar_configuracao(self.config)

class FaceDatabase:
    """Gerencia banco de dados de faces."""
    
    def __init__(self, pasta_fotos: str = "fotos"):
        self.pasta_fotos = pasta_fotos
        self.criar_pasta_se_nao_existe()
    
    def criar_pasta_se_nao_existe(self):
        if not os.path.exists(self.pasta_fotos):
            os.makedirs(self.pasta_fotos)
            logger.info(f"Pasta '{self.pasta_fotos}' criada")
    
    def carregar_faces(self) -> Tuple[List, List, List]:
        """Carrega todas as faces de referência da pasta fotos."""
        face_encodings = []
        face_names = []
        face_images = []
        
        if not os.path.exists(self.pasta_fotos):
            logger.warning(f"Pasta '{self.pasta_fotos}' não encontrada")
            return face_encodings, face_names, face_images
        
        # Listar todos os arquivos de imagem na pasta
        arquivos_foto = [f for f in os.listdir(self.pasta_fotos) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        if not arquivos_foto:
            logger.warning(f"Nenhuma foto encontrada em '{self.pasta_fotos}'")
            return face_encodings, face_names, face_images
        
        logger.info(f"🔍 Carregando {len(arquivos_foto)} faces de referência...")
        
        for i, arquivo in enumerate(arquivos_foto):
            try:
                caminho = os.path.join(self.pasta_fotos, arquivo)
                logger.info(f"  📸 Processando: {arquivo}")
                
                # Carregar imagem
                image = face_recognition.load_image_file(caminho)
                
                # Detectar faces na imagem
                face_encodings_batch = face_recognition.face_encodings(image)
                face_locations = face_recognition.face_locations(image)
                
                if face_encodings_batch and face_locations:
                    # Usar a primeira face encontrada na imagem
                    face_encodings.append(face_encodings_batch[0])
                    
                    # Extrair imagem da face para exibição
                    top, right, bottom, left = face_locations[0]
                    face_image = image[top:bottom, left:right]
                    face_images.append(face_image)
                    
                    # Usar o nome do arquivo (sem extensão) como identificação
                    nome = os.path.splitext(arquivo)[0]
                    face_names.append(nome)
                    
                    logger.info(f"    ✅ Face detectada: {nome}")
                else:
                    logger.warning(f"    ❌ Nenhuma face detectada em {arquivo}")
                    
            except Exception as e:
                logger.error(f"    ❌ Erro ao processar {arquivo}: {e}")
        
        logger.info(f"✅ Total de faces carregadas: {len(face_encodings)}")
        return face_encodings, face_names, face_images
    
    def adicionar_face(self, frame: np.ndarray, nome: str) -> bool:
        """Adiciona uma nova face ao banco de dados."""
        try:
            # Detectar face no frame
            face_locations = face_recognition.face_locations(frame)
            
            if not face_locations:
                logger.warning("Nenhuma face detectada no frame")
                return False
            
            # Usar a primeira face detectada
            top, right, bottom, left = face_locations[0]
            
            # Salvar imagem da face
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{nome}_{timestamp}.jpg"
            caminho = os.path.join(self.pasta_fotos, nome_arquivo)
            
            # Extrair e salvar apenas a região da face
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(caminho, face_image)
            
            logger.info(f"✅ Nova face salva: {nome_arquivo}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar face: {e}")
            return False

class InterfaceGrafica:
    """Gerencia interface gráfica."""
    
    def __init__(self, tema: str = "dark"):
        self.tema = tema
        self.cores = self.definir_cores()
    
    def definir_cores(self) -> Dict:
        if self.tema == "dark":
            return {
                'fundo': (40, 40, 40),
                'texto': (255, 255, 255),
                'texto_secundario': (200, 200, 200),
                'sucesso': (0, 255, 0),
                'erro': (0, 0, 255),
                'aviso': (0, 255, 255),
                'info': (255, 255, 0),
                'borda': (100, 100, 100)
            }
        else:
            return {
                'fundo': (240, 240, 240),
                'texto': (0, 0, 0),
                'texto_secundario': (100, 100, 100),
                'sucesso': (0, 150, 0),
                'erro': (200, 0, 0),
                'aviso': (200, 150, 0),
                'info': (0, 0, 200),
                'borda': (150, 150, 150)
            }
    
    def criar_painel_info(self, frame: np.ndarray, dados: Dict) -> np.ndarray:
        altura, largura = frame.shape[:2]
        altura_painel = 200
        info_panel = np.zeros((altura_painel, largura, 3), dtype=np.uint8)
        info_panel[:] = self.cores['fundo']
        
        # Título
        cv2.putText(info_panel, "SISTEMA DE RECONHECIMENTO FACIAL", (20, 30), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.8, self.cores['texto'], 2)
        
        # Métricas
        y_offset = 70
        cv2.putText(info_panel, f"FPS: {dados.get('fps', 0):.1f}", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.cores['sucesso'], 2)
        
        cv2.putText(info_panel, f"Faces: {dados.get('faces_detectadas', 0)}", (200, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.cores['info'], 2)
        
        cv2.putText(info_panel, f"Tolerância: {dados.get('tolerance', 0):.2f}", (400, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.cores['aviso'], 2)
        
        # Estatísticas
        y_offset += 40
        if dados.get('faces_detectadas', 0) > 0:
            taxa_reconhecimento = (dados.get('reconhecimentos_corretos', 0) / dados.get('faces_detectadas', 1)) * 100
            cv2.putText(info_panel, f"Taxa Reconhecimento: {taxa_reconhecimento:.1f}%", (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cores['sucesso'], 2)
        
        cv2.putText(info_panel, f"Faces Conhecidas: {dados.get('faces_conhecidas', 0)}", (350, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cores['texto'], 2)
        
        # Comandos
        y_offset += 40
        comandos = [
            "R: Nova Referência | T: Tolerância | D: Detalhes | C: Configurações | ESC: Sair"
        ]
        for comando in comandos:
            cv2.putText(info_panel, comando, (20, y_offset), 
                       cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, self.cores['texto_secundario'], 1)
            y_offset += 25
        
        frame_completo = np.vstack([frame, info_panel])
        return frame_completo
    
    def desenhar_face_detectada(self, frame: np.ndarray, face_data: Tuple, 
                               modo_detalhado: bool = False) -> np.ndarray:
        """Desenha informações da face detectada no frame."""
        (top, right, bottom, left), name, confidence = face_data
        
        # Escolher cor baseada no reconhecimento
        if name == "conheço nao":
            cor = self.cores['erro']  # Vermelho para desconhecidos
        else:
            cor = self.cores['sucesso']  # Verde para conhecidos
        
        # Desenhar retângulo ao redor da face
        cv2.rectangle(frame, (left, top), (right, bottom), cor, 3)
        
        # Preparar texto com nome e confiança
        texto = f"{name} ({confidence:.2f})"
        
        # Calcular tamanho do texto para criar fundo adequado
        (text_width, text_height), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        
        # Desenhar retângulo de fundo para o texto
        cv2.rectangle(frame, (left, bottom - 35), (left + text_width + 10, bottom), cor, cv2.FILLED)
        
        # Desenhar texto
        cv2.putText(frame, texto, (left + 5, bottom - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.cores['texto'], 1)
        
        # Modo detalhado: mostrar landmarks
        if modo_detalhado:
            centro_x = left + (right - left) // 2
            centro_y = top + (bottom - top) // 2
            cv2.circle(frame, (centro_x, centro_y), 4, self.cores['info'], -1)
        
        return frame

class SistemaFacialAvancado:
    def __init__(self, config_arquivo: str = "config.json"):
        # Configurações
        self.config_sistema = ConfiguracaoSistema(config_arquivo)
        self.config = self.config_sistema.config
        
        # Componentes
        self.face_db = FaceDatabase(self.config['pasta_fotos'])
        self.interface = InterfaceGrafica(self.config['interface_tema'])
        
        # Câmera
        self.cap = None
        
        # Dados de faces
        self.face_encodings_known = []
        self.face_names_known = []
        self.face_images_known = []
        
        # Otimizações
        self.frame_skip = self.config['frame_skip']
        self.frame_count = 0
        self.tolerance = self.config['tolerance']
        
        # Métricas
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.fps = 0
        self.faces_detectadas = 0
        self.reconhecimentos_corretos = 0
        
        # Estado
        self.sistema_ativo = True
        self.modo_detalhado = self.config['modo_detalhado']
        
        # Threading
        self.processing_lock = threading.Lock()
        self.last_results = None
        
        # Inicializar
        self.inicializar_sistema()
    
    def inicializar_sistema(self):
        """Inicializa todos os componentes do sistema."""
        logger.info("🚀 Inicializando Sistema de Reconhecimento Facial...")
        
        if not self.inicializar_camera():
            logger.error("❌ Falha ao inicializar câmera")
            return False
        
        self.carregar_faces_referencia()
        logger.info("✅ Sistema inicializado com sucesso")
        return True
    
    def inicializar_camera(self) -> bool:
        """Inicializa a câmera com configurações otimizadas."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logger.error("❌ Não foi possível abrir a câmera")
                return False
            
            # Configurações de alta qualidade
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera_width'])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera_height'])
            self.cap.set(cv2.CAP_PROP_FPS, self.config['camera_fps'])
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            logger.info(f"✅ Câmera inicializada: {self.config['camera_width']}x{self.config['camera_height']} @ {self.config['camera_fps']}fps")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar câmera: {e}")
            return False
    
    def carregar_faces_referencia(self):
        """Carrega faces de referência do banco de dados."""
        self.face_encodings_known, self.face_names_known, self.face_images_known = self.face_db.carregar_faces()
    
    def processar_frame_thread(self, frame: np.ndarray) -> Tuple[List, List, List]:
        """Processa frame em thread separada para otimização."""
        try:
            # Redimensionar para processamento mais rápido
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Detectar faces
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Reconhecer faces
            face_names = []
            face_confidences = []
            
            for face_encoding in face_encodings:
                if not self.face_encodings_known:
                    face_names.append("conheço nao")
                    face_confidences.append(0.0)
                    continue
                
                # Calcular distâncias para todas as faces conhecidas
                face_distances = face_recognition.face_distance(self.face_encodings_known, face_encoding)
                
                # Encontrar a melhor correspondência
                best_match_index = np.argmin(face_distances)
                min_distance = face_distances[best_match_index]
                
                # Calcular confiança (1 - distância)
                confidence = 1 - min_distance
                
                if min_distance <= self.tolerance:
                    name = self.face_names_known[best_match_index]
                else:
                    name = "conheço nao"
                
                face_names.append(name)
                face_confidences.append(confidence)
            
            return face_locations, face_names, face_confidences
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento de frame: {e}")
            return [], [], []
    
    def processar_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List, List, List]:
        """Processa frame principal com otimizações."""
        self.frame_count += 1
        
        # Processar apenas frames alternados
        if self.frame_count % self.frame_skip == 0:
            face_locations, face_names, face_confidences = self.processar_frame_thread(frame)
            self.last_results = (face_locations, face_names, face_confidences)
        else:
            # Usar resultados do frame anterior
            face_locations, face_names, face_confidences = self.last_results or ([], [], [])
        
        # Desenhar resultados
        for i, ((top, right, bottom, left), name, confidence) in enumerate(zip(face_locations, face_names, face_confidences)):
            # Escalar de volta para o tamanho original
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Desenhar face detectada
            face_data = ((top, right, bottom, left), name, confidence)
            frame = self.interface.desenhar_face_detectada(frame, face_data, self.modo_detalhado)
            
            # Atualizar contadores
            if name != "conheço nao":
                self.reconhecimentos_corretos += 1
        
        self.faces_detectadas += len(face_locations)
        return frame, face_locations, face_names, face_confidences
    
    def calcular_fps(self):
        """Calcula e atualiza FPS."""
        self.fps_counter += 1
        if self.fps_counter >= 30:
            tempo_atual = time.time()
            self.fps = self.fps_counter / (tempo_atual - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = tempo_atual
    
    def capturar_foto_referencia(self, frame: np.ndarray) -> bool:
        """Captura uma nova foto de referência."""
        try:
            nome = input("Digite o nome da pessoa (ou Enter para usar timestamp): ").strip()
            if not nome:
                nome = f"Pessoa_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if self.face_db.adicionar_face(frame, nome):
                # Recarregar faces de referência
                self.carregar_faces_referencia()
                logger.info(f"✅ Nova referência adicionada: {nome}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao capturar foto de referência: {e}")
            return False
    
    def ajustar_tolerancia(self):
        """Ajusta a tolerância de reconhecimento."""
        try:
            print(f"\nTolerância atual: {self.tolerance}")
            print("Valores recomendados:")
            print("  0.3 - Muito restritivo (poucos falsos positivos)")
            print("  0.6 - Padrão (equilibrado)")
            print("  0.8 - Permissivo (mais reconhecimentos)")
            
            nova_tolerancia = input(f"Digite nova tolerância (0.1-1.0): ")
            valor = float(nova_tolerancia)
            valor = max(0.1, min(1.0, valor))
            
            self.tolerance = valor
            self.config_sistema.atualizar_configuracao('tolerance', valor)
            logger.info(f"✅ Tolerância ajustada para: {valor}")
            
        except ValueError:
            logger.warning("❌ Valor inválido. Tolerância mantida.")
        except Exception as e:
            logger.error(f"❌ Erro ao ajustar tolerância: {e}")
    
    def mostrar_configuracoes(self):
        """Mostra e permite editar configurações."""
        try:
            print("\n=== CONFIGURAÇÕES DO SISTEMA ===")
            for chave, valor in self.config.items():
                print(f"{chave}: {valor}")
            
            print("\nConfigurações editáveis:")
            print("1. Modo detalhado")
            print("2. Frame skip")
            print("3. Tema da interface")
            print("4. Qualidade da câmera")
            
            opcao = input("Digite o número da opção para editar (ou Enter para sair): ").strip()
            
            if opcao == "1":
                self.modo_detalhado = not self.modo_detalhado
                self.config_sistema.atualizar_configuracao('modo_detalhado', self.modo_detalhado)
                logger.info(f"🔍 Modo detalhado: {'ON' if self.modo_detalhado else 'OFF'}")
            
            elif opcao == "2":
                novo_skip = input(f"Digite novo frame skip (atual: {self.frame_skip}): ")
                try:
                    self.frame_skip = int(novo_skip)
                    self.config_sistema.atualizar_configuracao('frame_skip', self.frame_skip)
                    logger.info(f"✅ Frame skip ajustado para: {self.frame_skip}")
                except ValueError:
                    logger.warning("❌ Valor inválido.")
            
            elif opcao == "3":
                novo_tema = input("Digite o tema (dark/light): ").strip().lower()
                if novo_tema in ['dark', 'light']:
                    self.interface = InterfaceGrafica(novo_tema)
                    self.config_sistema.atualizar_configuracao('interface_tema', novo_tema)
                    logger.info(f"✅ Tema alterado para: {novo_tema}")
                else:
                    logger.warning("❌ Tema inválido. Use 'dark' ou 'light'.")
            
            elif opcao == "4":
                print("\nQualidade da câmera:")
                print("1. Baixa (640x480)")
                print("2. Média (1280x720)")
                print("3. Alta (1920x1080)")
                qualidade = input("Escolha a qualidade (1-3): ").strip()
                
                if qualidade == "1":
                    self.config['camera_width'] = 640
                    self.config['camera_height'] = 480
                elif qualidade == "2":
                    self.config['camera_width'] = 1280
                    self.config['camera_height'] = 720
                elif qualidade == "3":
                    self.config['camera_width'] = 1920
                    self.config['camera_height'] = 1080
                else:
                    logger.warning("❌ Opção inválida.")
                    return
                
                self.config_sistema.atualizar_configuracao('camera_width', self.config['camera_width'])
                self.config_sistema.atualizar_configuracao('camera_height', self.config['camera_height'])
                logger.info(f"✅ Qualidade alterada para: {self.config['camera_width']}x{self.config['camera_height']}")
                logger.info("⚠️ Reinicie o sistema para aplicar as mudanças.")
                    
        except Exception as e:
            logger.error(f"❌ Erro ao mostrar configurações: {e}")
    
    def executar(self):
        """Executa o sistema avançado de reconhecimento facial."""
        if not self.cap:
            logger.error("❌ Câmera não inicializada")
            return
        
        logger.info("=== SISTEMA AVANÇADO DE RECONHECIMENTO FACIAL ===")
        logger.info("Comandos:")
        logger.info("  [R] - Capturar nova foto de referência")
        logger.info("  [T] - Ajustar tolerância")
        logger.info("  [D] - Alternar modo detalhado")
        logger.info("  [C] - Configurações do sistema")
        logger.info("  [ESC] - Sair")
        logger.info(f"Tolerância atual: {self.tolerance}")
        
        # Criar janela
        cv2.namedWindow('Sistema Facial Avançado', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Sistema Facial Avançado', 1200, 900)
        
        try:
            while self.sistema_ativo:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("❌ Erro ao capturar frame")
                    break
                
                # Processar frame
                frame_processado, face_locations, face_names, face_confidences = self.processar_frame(frame)
                
                # Melhorar qualidade da imagem
                frame_processado = self.melhorar_qualidade_imagem(frame_processado)
                
                # Calcular FPS
                self.calcular_fps()
                
                # Preparar dados para interface
                dados_interface = {
                    'fps': self.fps,
                    'faces_detectadas': len(face_locations),
                    'tolerance': self.tolerance,
                    'reconhecimentos_corretos': self.reconhecimentos_corretos,
                    'faces_conhecidas': len(self.face_encodings_known),
                    'sistema_ativo': self.sistema_ativo
                }
                
                # Mostrar painel de informações
                frame_final = self.interface.criar_painel_info(frame_processado, dados_interface)
                
                cv2.imshow('Sistema Facial Avançado', frame_final)
                
                # Processar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
                elif key == ord('r') or key == ord('R'):
                    self.capturar_foto_referencia(frame)
                elif key == ord('t') or key == ord('T'):
                    self.ajustar_tolerancia()
                elif key == ord('d') or key == ord('D'):
                    self.modo_detalhado = not self.modo_detalhado
                    self.config_sistema.atualizar_configuracao('modo_detalhado', self.modo_detalhado)
                    logger.info(f"🔍 Modo detalhado: {'ON' if self.modo_detalhado else 'OFF'}")
                elif key == ord('c') or key == ord('C'):
                    self.mostrar_configuracoes()
                
        except KeyboardInterrupt:
            logger.info("⚠️ Sistema interrompido pelo usuário")
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
        finally:
            self.encerrar_sistema()
    
    def encerrar_sistema(self):
        """Encerra o sistema de forma limpa."""
        try:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            
            logger.info("👋 Sistema encerrado")
            logger.info(f"📊 Estatísticas finais:")
            logger.info(f"   - Faces detectadas: {self.faces_detectadas}")
            logger.info(f"   - Reconhecimentos corretos: {self.reconhecimentos_corretos}")
            if self.faces_detectadas > 0:
                taxa = (self.reconhecimentos_corretos / self.faces_detectadas) * 100
                logger.info(f"   - Taxa de reconhecimento: {taxa:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ Erro ao encerrar sistema: {e}")

    def melhorar_qualidade_imagem(self, frame: np.ndarray) -> np.ndarray:
        """Aplica filtros para melhorar a qualidade da imagem."""
        try:
            # Redimensionar para melhor qualidade se necessário
            if frame.shape[1] < 1280:
                frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LANCZOS4)
            
            # Aplicar filtro de suavização para reduzir ruído
            frame = cv2.bilateralFilter(frame, 9, 75, 75)
            
            # Ajustar contraste e brilho
            alpha = 1.1  # Contraste (1.0 = normal, >1.0 = mais contraste)
            beta = 10    # Brilho (0 = normal, >0 = mais brilho)
            frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            
            # Aplicar sharpening para melhorar nitidez
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            frame = cv2.filter2D(frame, -1, kernel)
            
            return frame
            
        except Exception as e:
            logger.error(f"❌ Erro ao melhorar qualidade da imagem: {e}")
            return frame

def main():
    """Função principal."""
    try:
        sistema = SistemaFacialAvancado()
        sistema.executar()
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main() 