import cv2
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict
import math

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

def processar_frame(frame, hands, mp_hands, mp_drawing, controller):
    """Processa o frame para detecção e desenho dos pontos da mão, identificando cada mão e posição dos dedos."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    h, w, _ = image_bgr.shape
    coordenadas_pulso = None

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
            label = MessageToDict(handedness)["classification"][0]["label"]
            score = MessageToDict(handedness)["classification"][0]["score"]
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
    status = (
        f"[h]Nome:{'ON' if controller['exibir_nome_mao'] else 'OFF'} "
        f"[d]Dedos:{'ON' if controller['exibir_dedos'] else 'OFF'} "
        f"[l]Conexoes:{'ON' if controller['desenhar_conexoes'] else 'OFF'} "
        f"[p]Pulso:{'ON' if controller['exibir_pulso'] else 'OFF'} "
        f"[m]Numeração:{'ON' if controller['numerar_dedos'] else 'OFF'} "
        f"[c]Dist:{'ON' if controller['calcular_distancia'] else 'OFF'} "
        f"[a]Ângulo:{'ON' if controller['calcular_angulo'] else 'OFF'} "
        f"[n]Contar:{'ON' if controller['contar_dedos'] else 'OFF'} "
        f"[g]Gestos:{'ON' if controller['reconhecer_gesto'] else 'OFF'} "
    )
    cv2.putText(image_bgr, status, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    return image_bgr, coordenadas_pulso

def main():
    """Função principal para rastreamento de mão com MediaPipe e OpenCV."""
    hands, mp_hands, mp_drawing = inicializar_mediapipe_hands()
    cap = inicializar_camera()
    window_name = 'Rastreamento de Mão'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Controller de funcionalidades
    controller = {
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
            image_bgr, coordenadas_pulso = processar_frame(frame, hands, mp_hands, mp_drawing, controller)
            cv2.imshow(window_name, image_bgr)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
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
