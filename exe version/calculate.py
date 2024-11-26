import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Suavizado de posiciones usando media móvil
def smooth_positions(positions, window_size=3):
    smoothed_positions = []
    for i in range(len(positions)):
        x_vals = [positions[j][0] for j in range(max(0, i - window_size), i + 1)]
        y_vals = [positions[j][1] for j in range(max(0, i - window_size), i + 1)]
        smoothed_positions.append((np.mean(x_vals), np.mean(y_vals)))
    for i in range(len(smoothed_positions)):
        if i % 2 == 0:
            print(smoothed_positions[i])
    return smoothed_positions

# Cálculo de ángulos
def calculate_angle(positions, center):
    angles = []
    for pos in positions:
        x, y = pos
        # Calcular el ángulo usando atan2, que devuelve el ángulo en radianes
        angle = np.arctan2(y - center[1], x - center[0])
        # Convertir el ángulo a grados para facilidad de lectura
        angles.append(np.degrees(angle))
    return angles

# Normalización de ángulos para evitar cambios bruscos al cruzar cuadrantes
def normalize_angles(angles):
    normalized = [angles[0]]  # Inicia con el primer ángulo
    for i in range(1, len(angles)):
        delta = angles[i] - normalized[-1]
        if delta > 180:  # Ajustar cambio hacia el lado positivo
            angles[i] -= 360
        elif delta < -180:  # Ajustar cambio hacia el lado negativo
            angles[i] += 360
        normalized.append(angles[i])
    return normalized

# Cálculo de aceleración tangencial
def calculate_acceleration(velocities, fps, proportion=1):
    accelerations = []
    for i in range(1, len(velocities)):
        delta_v = velocities[i] - velocities[i-1]
        acceleration = delta_v * fps * proportion / 100  # Convertir a cm/s²
        accelerations.append(acceleration)
    return accelerations

# Graficado de los datos
def plot_data(angles, accelerations, centripetal_acceleration, fps):
    time = np.linspace(0, len(angles) / fps, len(angles))
    time_accel = time[:-1]

    plt.figure(figsize=(12, 8))

    # Gráfico de ángulos
    plt.subplot(3, 1, 1)
    plt.plot(time, angles, label='Ángulo suavizado', color='blue')
    plt.title('Variación del ángulo con respecto al tiempo (en grados)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (grados)')
    plt.grid(True)
    plt.legend()

    # Gráfico de la aceleración tangencial
    plt.subplot(3, 1, 2)
    plt.plot(time_accel, accelerations, label='Aceleración Tangencial', color='green')
    plt.title('Aceleración Tangencial a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (cm/s²)')
    plt.grid(True)
    plt.legend()

    # Gráfico de la aceleración centrípeta
    plt.subplot(3, 1, 3)
    plt.plot(time_accel, centripetal_acceleration, label='Aceleración Centrípeta', color='red')
    plt.title('Aceleración Centrípeta a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (cm/s²)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Cálculo de posiciones y velocidades a partir del video
def calculate_moves(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return

    positions = []
    radius = 10  # Ajustar según el radio estimado en cm del movimiento circular
    proportion = 0.1  # Proporción de pixeles a centímetros

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                positions.append((cx, cy))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Suavizar posiciones
    smoothed_positions = smooth_positions(positions, window_size=5)

    # Calcular ángulos y normalizarlos
    angles = calculate_angle(smoothed_positions, center=(320, 240))
    normalized_angles = normalize_angles(angles)

    # Suavizar ángulos
    smoothed_angles = savgol_filter(normalized_angles, window_length=5, polyorder=2)

    # Cálculo de aceleraciones y aceleración centrípeta
    accelerations = calculate_acceleration(smoothed_angles, fps, proportion)
    centripetal_acceleration = [(v**2) / (radius * proportion) for v in smoothed_angles[:-1]]

    # Graficar resultados
    plot_data(smoothed_angles, accelerations, centripetal_acceleration, fps)

