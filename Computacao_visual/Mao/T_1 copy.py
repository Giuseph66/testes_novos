import cv2
import mediapipe as mp
import time

# 1. Inicialização do MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 2. Abre a câmera e ajusta resolução
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

# 3. Cria uma única janela
window_name = 'Rastreamento de Mão'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar vídeo")
            break

        # processa com MediaPipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        h, w, _ = image_bgr.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image_bgr,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(thickness=2)
                )
                # exemplo de coordenada do pulso
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                cx, cy = int(wrist.x * w), int(wrist.y * h)
                cv2.circle(image_bgr, (cx, cy), 6, (255,0,0), cv2.FILLED)
                cv2.putText(image_bgr, f'({cx},{cy})',
                            (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255,0,0), 2)

        # exibe o mesmo frame na mesma janela
        cv2.imshow(window_name, image_bgr)

        # 4. Saída ao pressionar 'q' ou ESC
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

        # 5. Pequeno delay para aliviar CPU
        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()
