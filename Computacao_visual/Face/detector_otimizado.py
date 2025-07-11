import cv2
import face_recognition
import sys
import os
import time
from typing import Optional, Tuple, List
import argparse

class FaceDetector:
    """
    Classe para detecção e reconhecimento de rostos usando OpenCV e face_recognition.
    """
    
    def __init__(self, tolerance: float = 0.6, camera_id: int = 0):
        """
        Inicializa o detector de rostos.
        
        Args:
            tolerance: Tolerância para comparação de rostos (0.0 a 1.0)
            camera_id: ID da câmera a ser usada
        """
        self.tolerance = tolerance
        self.camera_id = camera_id
        self.cap = None
        self.known_encodings = []
        self.known_names = []
        
    def load_known_faces(self, image_paths: List[str], names: List[str]) -> None:
        """
        Carrega rostos conhecidos de imagens.
        
        Args:
            image_paths: Lista de caminhos para as imagens
            names: Lista de nomes correspondentes às imagens
        """
        if len(image_paths) != len(names):
            raise ValueError("O número de imagens deve ser igual ao número de nomes")
            
        for path, name in zip(image_paths, names):
            if not os.path.exists(path):
                print(f"⚠️  Aviso: Imagem '{path}' não encontrada, pulando...")
                continue
                
            try:
                encoding = self._get_face_encoding_from_image(path)
                self.known_encodings.append(encoding)
                self.known_names.append(name)
                print(f"✅ Carregado: {name} de '{path}'")
            except Exception as e:
                print(f"❌ Erro ao carregar '{path}': {e}")
                
        if not self.known_encodings:
            raise ValueError("Nenhum rosto válido foi carregado")
            
    def _get_face_encoding_from_image(self, path: str) -> List[float]:
        """
        Carrega imagem do disco, detecta o primeiro rosto e retorna seu encoding.
        
        Args:
            path: Caminho para a imagem
            
        Returns:
            Encoding do rosto detectado
            
        Raises:
            ValueError: Se nenhum rosto for encontrado
        """
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        
        if not encodings:
            raise ValueError(f"Nenhum rosto encontrado na imagem '{path}'")
            
        return encodings[0]
    
    def _detect_faces_in_frame(self, frame) -> Tuple[List[Tuple[int, int, int, int]], List[List[float]]]:
        """
        Detecta rostos em um frame e retorna suas localizações e encodings.
        
        Args:
            frame: Frame da câmera
            
        Returns:
            Tupla com localizações e encodings dos rostos
        """
        # Redimensiona o frame para melhor performance (1/4 do tamanho)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Converte de BGR (OpenCV) para RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detecta rostos no frame pequeno usando modelo HOG (mais rápido)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Converte as localizações de volta para o tamanho original
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4) 
                         for (top, right, bottom, left) in face_locations]
        
        return face_locations, face_encodings
    
    def _draw_face_boxes(self, frame, face_locations: List[Tuple[int, int, int, int]], 
                        face_names: List[str]) -> None:
        """
        Desenha caixas ao redor dos rostos detectados com seus nomes.
        
        Args:
            frame: Frame da câmera
            face_locations: Localizações dos rostos
            face_names: Nomes dos rostos
        """
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Desenha a caixa
            color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Desenha o nome
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
    
    def _draw_info_panel(self, frame, fps: float, faces_detected: int) -> None:
        """
        Desenha painel de informações na tela.
        
        Args:
            frame: Frame da câmera
            fps: FPS atual
            faces_detected: Número de rostos detectados
        """
        # Painel de informações
        info_text = [
            f"FPS: {fps:.1f}",
            f"Rostos: {faces_detected}",
            f"Tolerancia: {self.tolerance}",
            "Pressione 'q' para sair"
        ]
        
        y_offset = 30
        for text in info_text:
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (255, 255, 255), 2)
            y_offset += 25
    
    def start_detection(self) -> None:
        """
        Inicia o processo de detecção em tempo real.
        """
        try:
            # Abre a câmera uma única vez
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                raise RuntimeError(f"Não foi possível abrir a câmera {self.camera_id}")
            
            # Configura a câmera para melhor performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print("🚀 Iniciando detecção de rostos...")
            print("📋 Pessoas carregadas:", ", ".join(self.known_names))
            print("💡 Pressione 'q' para sair")
            
            frame_count = 0
            start_time = time.time()
            fps = 0
            
            # Variáveis para armazenar detecções anteriores
            face_locations = []
            face_names = []
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Erro ao capturar frame da câmera")
                    break
                
                # Detecta rostos a cada 3 frames para melhor performance
                if frame_count % 3 == 0:
                    face_locations, face_encodings = self._detect_faces_in_frame(frame)
                    face_names = []
                    
                    # Compara com rostos conhecidos
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(
                            self.known_encodings, 
                            face_encoding, 
                            tolerance=self.tolerance
                        )
                        
                        name = "Desconhecido"
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = self.known_names[first_match_index]
                        
                        face_names.append(name)
                
                # Desenha caixas e informações
                self._draw_face_boxes(frame, face_locations, face_names)
                
                # Calcula e exibe FPS
                frame_count += 1
                if frame_count % 30 == 0:  # Atualiza FPS a cada 30 frames
                    elapsed_time = time.time() - start_time
                    fps = frame_count / elapsed_time
                
                self._draw_info_panel(frame, fps, len(face_locations))
                
                # Exibe o frame
                cv2.imshow('Detector de Rostos', frame)
                
                # Verifica tecla de saída
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n⏹️  Interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro durante a detecção: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """
        Libera recursos da câmera e janelas.
        """
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Recursos liberados")

def main():
    """
    Função principal do programa.
    """
    parser = argparse.ArgumentParser(description='Detector de rostos em tempo real')
    parser.add_argument('--image', '-i', default='fotos/giuseph5.jpg', 
                       help='Caminho para a imagem de referência')
    parser.add_argument('--name', '-n', default='Giuseph', 
                       help='Nome da pessoa na imagem')
    parser.add_argument('--tolerance', '-t', type=float, default=0.6,
                       help='Tolerância para comparação (0.0-1.0)')
    parser.add_argument('--camera', '-c', type=int, default=0,
                       help='ID da câmera')
    
    args = parser.parse_args()
    
    try:
        # Verifica se a imagem existe
        if not os.path.exists(args.image):
            print(f"❌ Erro: Imagem '{args.image}' não encontrada")
            sys.exit(1)
        
        # Cria e configura o detector
        detector = FaceDetector(tolerance=args.tolerance, camera_id=args.camera)
        
        # Carrega rostos conhecidos
        detector.load_known_faces([args.image], [args.name])
        
        # Inicia a detecção
        detector.start_detection()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 