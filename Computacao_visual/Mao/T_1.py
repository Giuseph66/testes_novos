import cv2
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict
import math
import numpy as np
from collections import deque

def inicializar_mediapipe_hands():
    """Inicializa e retorna o objeto MediaPipe Hands."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    return hands, mp_hands, mp.solutions.drawing_utils

def inicializar_camera(indice_camera=0, largura=1024, altura=768):
    """Inicializa a câmera e ajusta a resolução."""
    cap = cv2.VideoCapture(indice_camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
    return cap

def calcular_distancia(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)
    return math.hypot(x2 - x1, y2 - y1), (x1, y1), (x2, y2)

def calcular_angulo(p1, p2, p3):
    # Calcula o ângulo em graus entre os pontos p1-p2-p3
    a = [p1.x - p2.x, p1.y - p2.y]
    b = [p3.x - p2.x, p3.y - p2.y]
    dot = a[0]*b[0] + a[1]*b[1]
    norm_a = math.hypot(a[0], a[1])
    norm_b = math.hypot(b[0], b[1])
    if norm_a * norm_b == 0:
        return 0
    angle = math.acos(dot / (norm_a * norm_b))
    return math.degrees(angle)

def contar_dedos(hand_landmarks, mp_hands, hand_label):
    dedos = [mp_hands.HandLandmark.THUMB_TIP,
             mp_hands.HandLandmark.INDEX_FINGER_TIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
             mp_hands.HandLandmark.RING_FINGER_TIP,
             mp_hands.HandLandmark.PINKY_TIP]
    bases = [mp_hands.HandLandmark.THUMB_IP,
             mp_hands.HandLandmark.INDEX_FINGER_PIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
             mp_hands.HandLandmark.RING_FINGER_PIP,
             mp_hands.HandLandmark.PINKY_PIP]
    count = 0
    for i in range(5):
        tip = hand_landmarks.landmark[dedos[i]]
        base = hand_landmarks.landmark[bases[i]]
        if i == 0:  # polegar
            if hand_label == 'Right':
                if tip.x < base.x:
                    count += 1
            else:  # Left
                if tip.x > base.x:
                    count += 1
        else:
            if tip.y < base.y:
                count += 1
    return count

def reconhecer_gesto(hand_landmarks, mp_hands, hand_label):
    dedos_levantados = []
    dedos = [mp_hands.HandLandmark.THUMB_TIP,
             mp_hands.HandLandmark.INDEX_FINGER_TIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
             mp_hands.HandLandmark.RING_FINGER_TIP,
             mp_hands.HandLandmark.PINKY_TIP]
    bases = [mp_hands.HandLandmark.THUMB_IP,
             mp_hands.HandLandmark.INDEX_FINGER_PIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
             mp_hands.HandLandmark.RING_FINGER_PIP,
             mp_hands.HandLandmark.PINKY_PIP]
    for i in range(5):
        tip = hand_landmarks.landmark[dedos[i]]
        base = hand_landmarks.landmark[bases[i]]
        if i == 0:
            if hand_label == 'Right':
                dedos_levantados.append(1 if tip.x < base.x else 0)
            else:
                dedos_levantados.append(1 if tip.x > base.x else 0)
        else:
            dedos_levantados.append(1 if tip.y < base.y else 0)
    if dedos_levantados == [1,0,0,0,0]:
        return "Joinha"
    if dedos_levantados == [0,1,1,0,0]:
        return "Paz e Amor"
    if dedos_levantados == [1,1,1,1,1]:
        return "Mão Aberta"
    if dedos_levantados == [0,0,0,0,0]:
        return "Mão Fechada"
    return "Outro"

def calcular_angulo_pulso(hand_landmarks, mp_hands):
    # Ângulo entre os vetores pulso->indicador (5) e pulso->mínimo (17)
    p0 = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    p5 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    p17 = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    v1 = [p5.x - p0.x, p5.y - p0.y]
    v2 = [p17.x - p0.x, p17.y - p0.y]
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    norm1 = math.hypot(v1[0], v1[1])
    norm2 = math.hypot(v2[0], v2[1])
    if norm1 * norm2 == 0:
        return 0
    angle = math.acos(dot / (norm1 * norm2))
    return math.degrees(angle)

# Função para coletar landmarks detalhados
landmarks_history = []  # Para salvar landmarks de cada frame
trajetorias = {}  # Para rastrear trajetória por mão
velocidades = {}  # Para velocidade/aceleração

# Função para salvar landmarks (pode ser expandida para salvar em arquivo)
def coletar_landmarks(hand_landmarks, w, h):
    pontos = [(int(lm.x * w), int(lm.y * h), lm.z) for lm in hand_landmarks.landmark]
    return pontos

# Função para calcular ângulos das articulações de um dedo
def angulo_articulacao(p0, p1, p2):
    a = np.array([p0.x - p1.x, p0.y - p1.y])
    b = np.array([p2.x - p1.x, p2.y - p1.y])
    if np.linalg.norm(a) * np.linalg.norm(b) == 0:
        return 0
    cos_ang = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    ang = np.arccos(np.clip(cos_ang, -1.0, 1.0))
    return np.degrees(ang)

# Função para orientação/inclinação da mão
def calcular_orientacao(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    index_mcp = hand_landmarks.landmark[5]
    pinky_mcp = hand_landmarks.landmark[17]
    v1 = np.array([index_mcp.x - wrist.x, index_mcp.y - wrist.y])
    v2 = np.array([pinky_mcp.x - wrist.x, pinky_mcp.y - wrist.y])
    ang = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
    return np.degrees(ang)

# Função para detecção de contato (ex: polegar e indicador)
def detectar_contato(hand_landmarks, mp_hands, w, h, limiar=30):
    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    dist, _, _ = calcular_distancia(thumb, index, w, h)
    return dist < limiar

# Função para análise de padrões de movimento (exemplo: detectar círculo)
def analisar_padrao_movimento(traj):
    if len(traj) < 10:
        return "-"
    traj_np = np.array(traj)
    # Exemplo simples: se a trajetória cobre uma área grande, pode ser círculo
    area = np.ptp(traj_np[:,0]) * np.ptp(traj_np[:,1])
    if area > 10000:
        return "Movimento amplo"
    return "Movimento restrito"

def processar_frame(frame, hands, mp_hands, mp_drawing, controller):
    global landmarks_history, trajetorias, velocidades
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    h, w, _ = image_bgr.shape
    coordenadas_pulso = None

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
            label = MessageToDict(handedness)["classification"][0]["label"]
            score = MessageToDict(handedness)["classification"][0]["score"]
            # Coleta de landmarks detalhados
            if controller['coletar_landmarks']:
                pontos = coletar_landmarks(hand_landmarks, w, h)
                landmarks_history.append({'label': label, 'pontos': pontos})
                for i, (x, y, z) in enumerate(pontos):
                    cv2.circle(image_bgr, (x, y), 2, (255, 255, 255), -1)
                    cv2.putText(image_bgr, f"{i}:({x},{y})", (x+2, y-2), cv2.FONT_HERSHEY_PLAIN, 0.9, (200,200,0), 1)
            # Rastrear trajetória do pulso
            if controller['rastrear_trajetoria']:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                if label not in trajetorias:
                    trajetorias[label] = deque(maxlen=100)
                trajetorias[label].append((wx, wy))
                for i in range(1, len(trajetorias[label])):
                    cv2.line(image_bgr, trajetorias[label][i-1], trajetorias[label][i], (0,255,255), 2)
                # Análise de padrão de movimento
                if controller['analise_padrao']:
                    padrao = analisar_padrao_movimento(trajetorias[label])
                    cv2.putText(image_bgr, f'Padrao:{padrao}', (wx+10, wy+60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            # Velocidade e aceleração
            if controller['velocidade']:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                if label not in velocidades:
                    velocidades[label] = deque(maxlen=2)
                velocidades[label].append((wx, wy))
                if len(velocidades[label]) == 2:
                    v = np.linalg.norm(np.array(velocidades[label][1]) - np.array(velocidades[label][0]))
                    cv2.putText(image_bgr, f'Vel:{v:.1f}', (wx+10, wy+80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)
            # Orientação/inclinação da mão
            if controller['orientacao']:
                ang = calcular_orientacao(hand_landmarks)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                cv2.putText(image_bgr, f'Or:{int(ang)}', (wx+10, wy+100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            # Detecção de contato/pressão
            if controller['contato']:
                contato = detectar_contato(hand_landmarks, mp_hands, w, h)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                if contato:
                    cv2.putText(image_bgr, 'Contato!', (wx+10, wy+120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            # Cálculo de ângulos das articulações
            if controller['angulos_articulacoes']:
                # Exemplo: ângulo do dedo indicador (MCP-PIP-TIP)
                mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                ang = angulo_articulacao(mcp, pip, tip)
                px, py = int(pip.x * w), int(pip.y * h)
                cv2.putText(image_bgr, f'AngInd:{int(ang)}', (px+10, py-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,128,0), 2)
            if controller['desenhar_conexoes']:
                mp_drawing.draw_landmarks(
                    image_bgr,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(thickness=2)
                )
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            cx, cy = int(wrist.x * w), int(wrist.y * h)
            coordenadas_pulso = (cx, cy)
            if controller['exibir_nome_mao']:
                cv2.putText(image_bgr, f'{label} ({score:.2f})',
                            (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255,0,0), 2)
            if controller['exibir_pulso']:
                cv2.circle(image_bgr, (cx, cy), 6, (255,0,0), cv2.FILLED)
                cv2.putText(image_bgr, f'Pulso:({cx},{cy})',
                            (cx+10, cy+30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255,0,0), 2)
            dedos = {
                'Polegar': mp_hands.HandLandmark.THUMB_TIP,
                'Indicador': mp_hands.HandLandmark.INDEX_FINGER_TIP,
                'Médio': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                'Anelar': mp_hands.HandLandmark.RING_FINGER_TIP,
                'Mínimo': mp_hands.HandLandmark.PINKY_TIP
            }
            if controller['exibir_dedos']:
                for i, (nome, idx_dedo) in enumerate(dedos.items()):
                    dedo = hand_landmarks.landmark[idx_dedo]
                    dx, dy = int(dedo.x * w), int(dedo.y * h)
                    cv2.circle(image_bgr, (dx, dy), 8, (0,255,0), 2)
                    cv2.putText(image_bgr, f'{nome}:({dx},{dy})',
                                (dx+10, dy), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0,128,0), 2)
            if controller['numerar_dedos']:
                for i, idx_dedo in enumerate(dedos.values()):
                    dedo = hand_landmarks.landmark[idx_dedo]
                    dx, dy = int(dedo.x * w), int(dedo.y * h)
                    cv2.putText(image_bgr, f'{i+1}', (dx-10, dy-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            if controller['calcular_distancia']:
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                dist, (x1, y1), (x2, y2) = calcular_distancia(thumb, index, w, h)
                cv2.line(image_bgr, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.putText(image_bgr, f'Dist:{int(dist)}px', (min(x1,x2), min(y1,y2)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            if controller['calcular_angulo']:
                ang = calcular_angulo_pulso(hand_landmarks, mp_hands)
                wx, wy = int(wrist.x * w), int(wrist.y * h)
                cv2.putText(image_bgr, f'Ang:{int(ang)}', (wx+10, wy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128,0,255), 2)
            if controller['contar_dedos']:
                n = contar_dedos(hand_landmarks, mp_hands, label)
                cv2.putText(image_bgr, f'Dedos:{n}', (cx+10, cy+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,128,255), 2)
            if controller['reconhecer_gesto']:
                gesto = reconhecer_gesto(hand_landmarks, mp_hands, label)
                cv2.putText(image_bgr, f'Gesto:{gesto}', (cx+10, cy+70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    return image_bgr, coordenadas_pulso

def desenhar_controller(controller, frame=None):
    # Janela ainda maior e mais espaçada
    largura, altura = 800, 1000
    painel_largura = 400
    img = np.zeros((altura, largura, 3), dtype=np.uint8)
    img[:] = (30, 30, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cor_on = (0, 255, 0)
    cor_off = (0, 0, 255)
    cor_label = (255, 255, 255)
    cor_tecla = (255, 200, 0)
    linhas = [
        ("x", "Landmarks Detalhados", controller['coletar_landmarks']),
        ("t", "Trajetória do Pulso", controller['rastrear_trajetoria']),
        ("v", "Velocidade do Pulso", controller['velocidade']),
        ("o", "Orientação da Mão", controller['orientacao']),
        ("z", "Contato/Pressão", controller['contato']),
        ("j", "Ângulo Artic. Indicador", controller['angulos_articulacoes']),
        ("r", "Análise de Padrão", controller['analise_padrao']),
        ("h", "Exibir Nome da Mão", controller['exibir_nome_mao']),
        ("d", "Exibir Dedos", controller['exibir_dedos']),
        ("l", "Desenhar Conexões", controller['desenhar_conexoes']),
        ("p", "Exibir Pulso", controller['exibir_pulso']),
        ("m", "Numeração dos Dedos", controller['numerar_dedos']),
        ("c", "Distância Polegar-Indicador", controller['calcular_distancia']),
        ("a", "Ângulo do Pulso", controller['calcular_angulo']),
        ("n", "Contar Dedos", controller['contar_dedos']),
        ("g", "Reconhecer Gestos", controller['reconhecer_gesto']),
    ]
    cv2.putText(img, 'CONTROLLER', (40, 70), font, 2.5, (255,255,0), 6)
    for i, (tecla, nome, status) in enumerate(linhas):
        y = 130 + i*45
        cv2.putText(img, f'[{tecla.upper()}]', (40, y), font, 1.7, cor_tecla, 4)
        cv2.putText(img, nome, (180, y), font, 1.5, cor_label, 3)
        cor = cor_on if status else cor_off
        txt = 'ON' if status else 'OFF'
        cv2.putText(img, txt, (largura-100, y), font, 1.7, cor, 4)
    cv2.putText(img, '[Q] Sair', (40, altura-40), font, 1.7, (255,255,255), 4)
    return img

def main():
    """Função principal para rastreamento de mão com MediaPipe e OpenCV."""
    global landmarks_history, trajetorias, velocidades
    hands, mp_hands, mp_drawing = inicializar_mediapipe_hands()
    cap = inicializar_camera()
    window_name = 'Rastreamento de Mão'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow('Controller', cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1024, 768)
    cv2.resizeWindow('Controller', 1024, 768)

    controller = {
        'coletar_landmarks': False,
        'rastrear_trajetoria': False,
        'velocidade': False,
        'orientacao': False,
        'contato': False,
        'angulos_articulacoes': False,
        'analise_padrao': False,
        'exibir_nome_mao': True,
        'exibir_dedos': True,
        'desenhar_conexoes': True,
        'exibir_pulso': True,
        'numerar_dedos': False,
        'calcular_distancia': False,
        'calcular_angulo': False,
        'contar_dedos': False,
        'reconhecer_gesto': False
    }

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Falha ao capturar vídeo")
                break
            frame = cv2.flip(frame, 1)
            image_bgr, _ = processar_frame(frame, hands, mp_hands, mp_drawing, controller)
            cv2.imshow(window_name, image_bgr)
            controller_img = desenhar_controller(controller, frame)
            cv2.imshow('Controller', controller_img)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('x'):
                controller['coletar_landmarks'] = not controller['coletar_landmarks']
            elif key == ord('t'):
                controller['rastrear_trajetoria'] = not controller['rastrear_trajetoria']
            elif key == ord('v'):
                controller['velocidade'] = not controller['velocidade']
            elif key == ord('o'):
                controller['orientacao'] = not controller['orientacao']
            elif key == ord('z'):
                controller['contato'] = not controller['contato']
            elif key == ord('j'):
                controller['angulos_articulacoes'] = not controller['angulos_articulacoes']
            elif key == ord('r'):
                controller['analise_padrao'] = not controller['analise_padrao']
            elif key == ord('h'):
                controller['exibir_nome_mao'] = not controller['exibir_nome_mao']
            elif key == ord('d'):
                if controller['numerar_dedos']:
                    controller['numerar_dedos'] = False
                controller['exibir_dedos'] = not controller['exibir_dedos']
            elif key == ord('l'):
                controller['desenhar_conexoes'] = not controller['desenhar_conexoes']
            elif key == ord('p'):
                controller['exibir_pulso'] = not controller['exibir_pulso']
            elif key == ord('m'):
                if not controller['exibir_dedos']:
                    controller['exibir_dedos'] = True
                controller['numerar_dedos'] = not controller['numerar_dedos']
            elif key == ord('c'):
                controller['calcular_distancia'] = not controller['calcular_distancia']
            elif key == ord('a'):
                controller['calcular_angulo'] = not controller['calcular_angulo']
            elif key == ord('n'):
                controller['contar_dedos'] = not controller['contar_dedos']
            elif key == ord('g'):
                controller['reconhecer_gesto'] = not controller['reconhecer_gesto']
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
