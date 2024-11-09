import cv2
import numpy as np
import matplotlib.pyplot as plt

# Suavizado de las posiciones usando media móvil
def smooth_positions(positions, window_size=5):
    smoothed_positions = []
    for i in range(len(positions)):
        start = max(0, i - window_size // 2)
        end = min(len(positions), i + window_size // 2 + 1)
        avg_x = np.mean([pos[0] for pos in positions[start:end]])
        avg_y = np.mean([pos[1] for pos in positions[start:end]])
        smoothed_positions.append((avg_x, avg_y))
    return smoothed_positions

# Cálculo de la velocidad tangencial
def calculate_velocity(positions, fps, proportion=1):
    velocities = []
    for i in range(1, len(positions)):
        delta_pos = np.array(positions[i]) - np.array(positions[i-1])
        velocity = np.linalg.norm(delta_pos) * fps * proportion  # Convertir a cm/s
        velocities.append(velocity)
    return velocities

# Cálculo de la aceleración tangencial
def calculate_acceleration(velocities, fps, proportion=1):
    accelerations = []
    for i in range(1, len(velocities)):
        delta_v = velocities[i] - velocities[i-1]
        acceleration = delta_v * fps * proportion  # Convertir a cm/s^2
        accelerations.append(acceleration)
    return accelerations

# Graficado de los datos
def plot_data(velocities, accelerations, centripetal_acceleration, fps):
    # Ajustamos la longitud de time para que coincida con las otras listas
    time = np.linspace(0, len(velocities) / fps, len(velocities))
    time_accel = time[:-1]  # Usamos time[:-1] para la aceleración y aceleración centrípeta

    plt.figure(figsize=(12, 8))

    # Gráfico de la velocidad
    plt.subplot(3, 1, 1)
    plt.plot(time, velocities, label='Velocidad Tangencial', color='blue')
    plt.title('Velocidad Tangencial a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (cm/s)')
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
    
    # Verifica si el video fue cargado correctamente
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return

    positions = []
    radius = 10  # Ajustar según el radio estimado en cm del movimiento circular
    proportion = 0.1  # Proporción de pixeles a centímetros (ajustar según el video)
    fpspos = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detección del objeto
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
                print(f"Número de fps: {fpspos}, Posicion en x: {cx} - pos en y: {cy}")

        fpspos += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Suavizar posiciones
    smoothed_positions = smooth_positions(positions)

    # Cálculo de velocidad, aceleración y aceleración centrípeta
    velocities = calculate_velocity(smoothed_positions, fps, proportion)
    accelerations = calculate_acceleration(velocities, fps, proportion)
    centripetal_acceleration = [(v**2) / (radius * proportion) for v in velocities[:-1]]  # Usar velocities[:-1] para coincidir con accelerations

    # Graficar los resultados
    plot_data(velocities, accelerations, centripetal_acceleration, fps)

# Llamada a la función con el video
