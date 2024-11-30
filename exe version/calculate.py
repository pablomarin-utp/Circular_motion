import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def count_revolutions(angles):
    revolutions = 1
    for i in range(5, len(angles)):
        if angles[i] < 15 and angles[i-1] > 345:
            revolutions += 1
    
    print(f"El objeto dio {revolutions} vueltas.")
    return revolutions

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

    count_revolutions(angles)


    return angles

def xpositions(positions):
    xpositions = [pos[0] for pos in positions]
    xpositions = savgol_filter(xpositions, 5, 3)  # Aplicar filtro
    xpositions = xpositions[2:]
    return xpositions

def ypositions(positions):
    ypositions = [pos[1] for pos in positions]
    ypositions = savgol_filter(ypositions, 5, 3)  # Aplicar filtro
    ypositions = ypositions[2:]
    return ypositions

def calculate_velocity(angles, fps, radius):
    velocities = []
    delta_t = 1 / fps  # Tiempo entre cuadros

    
    for i in range(1, len(angles)):
        # Diferencia angular en radianes
        delta_theta = np.radians(angles[i] - angles[i - 1])
        # Velocidad tangencial
        velocity = (radius * delta_theta / delta_t) / 100  # Convertir a cm/s
        print (velocity)
        if velocity < -15:
            velocity = 0
        velocities.append(velocity)
        print (velocity)
    
    return velocities

    return velocities
# Cálculo de aceleración tangencial
def calculate_acceleration(velocities, fps):
    accelerations = []
    delta_t = 1 / fps  # Tiempo entre cuadros
    print("ACELERACIONES:")
    for i in range(1, len(velocities)):
        # Cambio de velocidad
        delta_v = velocities[i] - velocities[i - 1]
        # Aceleración tangencial
        acceleration = delta_v / delta_t
        print(acceleration)
        accelerations.append(acceleration)
    
    return accelerations

# Graficado de los datos
def plot_data(positions, angles, velocities, accelerations, centripetal_acceleration, fps):
    x = xpositions(positions)
    y = ypositions(positions)

    # Ajustar el tiempo para que coincida con las posiciones filtradas
    time = np.linspace(0, len(x) / fps, len(x))
    time_angles = np.linspace(0, len(angles) / fps, len(angles))
    time_velocities = np.linspace(0, len(velocities) / fps, len(velocities))
    time_accelerations = np.linspace(0, len(accelerations) / fps, len(accelerations))
    time_centripetal = np.linspace(0, len(centripetal_acceleration) / fps, len(centripetal_acceleration))

    plt.figure(figsize=(12, 16))

    # Ángulos
    plt.subplot(5, 1, 1)
    plt.plot(time_angles, angles, label='Ángulo', color='blue')
    plt.title('Variación del ángulo con respecto al tiempo (en grados)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (grados)')
    plt.grid(True)
    plt.legend()

    # Posición en x
    plt.subplot(5, 1, 2)
    plt.plot(time, x, label='Posición en x', color='red')
    plt.title('Posición en x a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('x (cm)')
    plt.grid(True)
    plt.legend()

    # Posición en y
    plt.subplot(5, 1, 3)
    plt.plot(time, y, label='Posición en y', color='green')
    plt.title('Posición en y a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('y (cm)')
    plt.grid(True)
    plt.legend()

    # Velocidad tangencial
    plt.subplot(5, 1, 4)
    plt.plot(time_velocities, velocities, label='Velocidad tangencial', color='orange')
    plt.title('Velocidad tangencial a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (cm/s)')
    plt.grid(True)
    plt.legend()

    # Aceleraciones tangencial y centrípeta
    plt.subplot(5, 1, 5)
    plt.plot(time_accelerations, accelerations, label='Aceleración tangencial', color='purple')
    plt.plot(time_centripetal, centripetal_acceleration, label='Aceleración centrípeta', color='brown')
    plt.title('Aceleración Tangencial y Centrípeta')
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

    # Calcular velocidades tangenciales
    velocities = calculate_velocity(angles, fps, radius)

    # Calcular aceleraciones tangenciales
    accelerations = calculate_acceleration(velocities, fps)

    # Calcular aceleración centrípeta
    centripetal_acceleration = [v**2 / radius for v in velocities]

    # Graficar resultados
    plot_data(positions, angles, velocities, accelerations, centripetal_acceleration, fps)

