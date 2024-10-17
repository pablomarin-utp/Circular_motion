import cv2
import numpy as np

# Parámetros del video (movimiento curvilíneo)
video_path = r'C:\Python\COMPUTER VISION\Videos generados\curvilineo.mp4'
fps = 30
duration = 10  # duración del video en segundos
width, height = 640, 480
center = (width // 2, height // 2)  # Centro del plano de referencia

# Crear el video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

# Función para generar una trayectoria aleatoria curvilínea
def random_trajectory(t, width, height):
    # Movimiento curvilíneo basado en seno y coseno con factores aleatorios
    x = int(width // 2 + 200 * np.sin(2 * np.pi * t / 300) + 50 * np.sin(0.5 * np.pi * t / 50))
    y = int(height // 2 + 150 * np.cos(2 * np.pi * t / 250) + 70 * np.sin(0.3 * np.pi * t / 80))
    return x, y

# Crear cada frame para el video
for t in range(int(duration * fps)):
    # Frame vacío (negro) para el video
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Obtener la posición de la partícula en el frame actual
    x, y = random_trajectory(t, width, height)
    
    # Dibujar la partícula en movimiento
    cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)  # Partícula en movimiento (amarillo)

    # Dibujar el plano de referencia (ejes x e y en el centro)
    cv2.line(frame, (center[0], 0), (center[0], height), (255, 255, 255), 1)  # Eje Y (blanco)
    cv2.line(frame, (0, center[1]), (width, center[1]), (255, 255, 255), 1)  # Eje X (blanco)

    # Dibujar una línea que conecte el centro con la partícula (el radio)
    cv2.line(frame, center, (x, y), (0, 0, 255), 2)  # Línea roja desde el centro a la partícula

    # Calcular el radio (distancia desde el centro a la partícula)
    radius = int(np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2))

    # Dibujar la circunferencia con el radio calculado
    cv2.circle(frame, center, radius, (0, 255, 0), 2)  # Circunferencia verde

    # Guardar el frame en el video
    out.write(frame)

# Liberar el video
out.release()

print(f"Video generado en {video_path}")
