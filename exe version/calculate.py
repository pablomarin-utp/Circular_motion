import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Cálculo de la velocidad a partir de los tiempos entre revoluciones
def calculate_velocity(tiempos, radio):
    velocities = []
    for tiempo in tiempos:
        velocidad = (2 * np.pi * radio) / tiempo  # Fórmula de velocidad
        velocities.append(velocidad)
    return velocities

def count_revolutions(angles):
    revolutions = 1
    space_between = []
    prom_rev = []

    for i in range(5, len(angles)):
        if angles[i] < 165 and angles[i-1] > 210:
            revolutions += 1
            space_between.append(i)
    
    for i in range(len(space_between)):
        space_between[i] = space_between[i] + 4
        prom_rev.append(space_between[i] / (i+1))

    space_between.append((len(angles) - 1) - 4)
    prom_rev.append(space_between[-1] / revolutions)
    desvest = np.std(prom_rev)
    acel_prom = np.mean(desvest)

    # Retornamos los tiempos entre revoluciones
    return revolutions, acel_prom, prom_rev

# Cálculo de ángulos
def calculate_angle(positions, center):
    angles = []
    xpos = xpositions(positions)
    ypos = ypositions(positions)

    for i in range(len(xpos)):
        x = xpos[i]
        y = ypos[i]
        # Calcular el ángulo en radianes usando atan2
        angle = np.arctan2(y - center[1], x - center[0])
        angles.append(angle)

    # Eliminar discontinuidades y convertir a grados
    angles = np.unwrap(angles)  # Hace continuo el cambio angular
    angles = np.degrees(angles)  # Convierte a grados
    angles = angles % 360  # Ajusta al rango de 0° a 360°

    return angles

def xpositions(positions):
    xpositions = [pos[0] for pos in positions]
    xpositions = xpositions[2:]
    return xpositions

def ypositions(positions):
    ypositions = [pos[1] for pos in positions]
    ypositions = ypositions[2:]
    return ypositions

# Cálculo de posiciones y velocidades a partir del video
def calculate_moves(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return

    positions = []
    radius = 10  # Ajustar según el radio estimado en cm del movimiento circular

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

    # Calcular tiempos entre revoluciones
    _, aceleration, prom_rev = count_revolutions(angles)

    # Calcular las velocidades a partir de los tiempos entre revoluciones
    velocities = calculate_velocity(prom_rev, radius)

    window = len(velocities) / 3
    if window % 2 == 0:
        window += 1

    # Aplicar el filtro de Savitzky-Golay a las velocidades
    smoothed_velocities = savgol_filter(velocities, int(window), int(window - 1))

    # Graficar resultados
    plot_data(positions, angles, smoothed_velocities, aceleration, fps, radius)

def plot_data(positions, angles, velocities, aceleration, fps, radius):

    if aceleration < 1.5:
        aceleration = 0
    x = xpositions(positions)
    y = ypositions(positions)

    # Ajustar el tiempo para que coincida con las posiciones filtradas
    time = np.linspace(0, len(x) / fps, len(x))
    time_angles = np.linspace(0, len(angles) / fps, len(angles))
    time_velocities = np.linspace(0, len(velocities) / fps, len(velocities))

    aceleration_list = [aceleration for i in range(len(time))]
    
    if aceleration == 0:
        first_velocity = velocities[0]
        last_velocity = velocities[-1]
        velocityprom = (first_velocity + last_velocity) / len(velocities)
        velocities = [velocityprom for i in range(len(time_velocities))]
    
    plt.figure(figsize=(12, 16))

    # Ángulos
    plt.subplot(3, 2, 1)
    plt.plot(time_angles, angles, label='Ángulo', color='blue')
    plt.title('Variación del ángulo con respecto al tiempo (en grados)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (grados)')
    plt.grid(True)
    plt.legend()

    # Posición en x
    plt.subplot(3, 2, 2)
    plt.plot(time, x, label='Posición en x', color='red')
    plt.title('Posición en x a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('x (cm)')
    plt.grid(True)
    plt.legend()

    # Posición en y
    plt.subplot(3, 2, 3)
    plt.plot(time, y, label='Posición en y', color='green')
    plt.title('Posición en y a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('y (cm)')
    plt.grid(True)
    plt.legend()

    # Velocidad calculada
    plt.subplot(3, 2, 4)
    plt.plot(time_velocities, velocities, label='Velocidad calculada', color='orange')
    plt.title('Velocidad a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (cm/s)')
    plt.grid(True)
    plt.legend()

    # Aceleraciones tangencial y centrípeta
    plt.subplot(3, 2, 5)
    plt.plot(time, aceleration_list, label='Aceleración tangencial', color='purple')
    plt.title('Aceleración Tangencial y Centrípeta')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (cm/s²)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
