import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Cálculo de ángulos
def calculate_angle(positions, center):
    angles = []
    for pos in positions:
        x, y = pos
        # Calcular el ángulo en radianes usando atan2
        angle = np.arctan2(y - center[1], x - center[0])
        angles.append(angle)

    # Eliminar discontinuidades y convertir a grados
    angles = np.unwrap(angles)  # Hace continuo el cambio angular
    angles = np.degrees(angles)  # Convierte a grados
    angles = angles % 360  # Ajusta al rango de 0° a 360°

    for i in range(len(angles)):
        if i % 2 == 0:
            print(angles[i])
    return angles

def xpositions(positions):
    xpositions = []
    for pos in positions:
        x, y = pos
        xpositions.append(x)
    #aplicar filtro de savgol
    xpositions = savgol_filter(xpositions, 5, 3)
    return xpositions

def ypositions(positions):
    ypositions = []
    for pos in positions:
        x, y = pos
        ypositions.append(y)
    #aplicar filtro de savgol
    ypositions = savgol_filter(ypositions, 5, 3)
    return ypositions
    

# Cálculo de aceleración tangencial
def calculate_acceleration(velocities, fps, proportion=1):
    accelerations = []
    for i in range(1, len(velocities)):
        delta_v = velocities[i] - velocities[i-1]
        acceleration = delta_v * fps * proportion / 100  # Convertir a cm/s²
        accelerations.append(acceleration)
    return accelerations

# Graficado de los datos
def plot_data(positions, angles, accelerations, centripetal_acceleration, fps):
    time = np.linspace(0, len(angles) / fps, len(angles))
    time_accel = time[:-1]

    plt.figure(figsize=(12, 8))

    # Angulos sin suavizar
    plt.subplot(3, 1, 1)
    plt.plot(time, angles, label='Ángulo', color='blue')
    plt.title('Variación del ángulo con respecto al tiempo (en grados)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (grados)')
    plt.grid(True)
    plt.legend()

    #Gráfico de la POSICION en x
    plt.subplot(3, 1, 2)
    x = xpositions(positions)
    plt.plot(time, x, label='Posición en x', color='red')
    plt.title('Posision en x a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('x(cm)')
    plt.grid(True)
    plt.legend()

    #Grafico de la  
    plt.subplot(3, 1, 3)
    y = ypositions(positions)
    plt.plot(time, y, label='Posición en y', color='green')
    plt.title('Posision en y a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('y(cm)')
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

    # Calcular ángulos 
    angles = calculate_angle(positions, center=[320, 240])

    # Cálculo de aceleraciones y aceleración centrípeta
    accelerations = calculate_acceleration(angles, fps, proportion)
    centripetal_acceleration = [(v**2) / (radius * proportion) for v in angles[:-1]]

    # Graficar resultados
    plot_data(positions, angles, accelerations, centripetal_acceleration, fps)

