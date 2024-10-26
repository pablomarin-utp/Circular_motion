import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_velocity(positions, fps):
    velocities = []
    for i in range(1, len(positions)):
        delta_pos = np.array(positions[i]) - np.array(positions[i-1])
        velocity = np.linalg.norm(delta_pos) * fps  
        velocities.append(velocity)
    return velocities

def calculate_acceleration(velocities, fps):
    accelerations = []
    for i in range(1, len(velocities)):
        delta_v = velocities[i] - velocities[i-1]
        acceleration = delta_v * fps  
        accelerations.append(acceleration)
    return accelerations

def plot_data(velocities, accelerations, centripetal_acceleration, fps):
    # Generar un array de tiempo basado en la cantidad de frames y FPS
    time = np.linspace(0, len(velocities) / fps, len(velocities))

    plt.figure(figsize=(12, 8))

    # Gráfico de la velocidad
    plt.subplot(3, 1, 1)
    plt.plot(time, velocities, label='Velocidad Tangencial', color='blue')
    plt.title('Velocidad Tangencial a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (píxeles/s)')
    plt.grid(True)
    plt.legend()

    # Gráfico de la aceleración tangencial
    plt.subplot(3, 1, 2)
    if len(accelerations) == len(time) - 1:  # Asegurarse de que las longitudes coincidan
        plt.plot(time[:-1], accelerations, label='Aceleración Tangencial', color='green')
    plt.title('Aceleración Tangencial a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (píxeles/s^2)')
    plt.grid(True)
    plt.legend()

    # Gráfico de la aceleración centrípeta
    plt.subplot(3, 1, 3)
    if len(centripetal_acceleration) == len(time) - 1:  # Asegurarse de que las longitudes coincidan
        plt.plot(time[:-1], centripetal_acceleration, label='Aceleración Centrípeta', color='red')
    plt.title('Aceleración Centrípeta a lo largo del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración Centrípeta (píxeles/s^2)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def calculate_moves(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Verifica si el video fue cargado correctamente
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return  # Termina la función si no se puede abrir el video

    positions = []
    radius = 10  # Radio del movimiento circular (se puede estimar o calcular)
    fpspos = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Proceso de detección del objeto (ajusta según el tipo de video)
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

        cv2.imshow('Frame', frame)
        fpspos += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Verificar si hay suficientes posiciones para calcular la velocidad y aceleración
    if len(positions) < 2:
        print("Error: No hay suficientes datos para calcular velocidades y aceleraciones.")
        return

    # Calculamos las velocidades y aceleraciones
    velocities = calculate_velocity(positions, fps)
    accelerations = calculate_acceleration(velocities, fps)

    if velocities:
        centripetal_acceleration = [v**2 / radius for v in velocities]
    else:
        centripetal_acceleration = []

    plot_data(velocities, accelerations, centripetal_acceleration, fps)
