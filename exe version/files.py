import numpy as np

def reduce_array_size(arr, max_length=2048):
    """
    Reduce el tamaño de un array de NumPy calculando el promedio entre pares sucesivos
    hasta que el tamaño sea menor o igual a max_length.
    """
    while len(arr) > max_length:
        arr = (arr[::2] + arr[1::2]) / 2  # Promedio de pares sucesivos
    return arr.astype(int)  # Convertir a enteros
def save_video_info(video_name, duration, radius1, turns, angles, posx, posy, angular_velocities, aceleration, save_path):
    """
    Guarda información del video en un archivo de texto, asegurándose de que los arrays
    tengan un tamaño menor a 2048 elementos y sin decimales.
    """
    try:
        file_path = f"{save_path}/{video_name}_info.txt"

        # Reducir las listas a un tamaño manejable
        angles = reduce_array_size(angles)
        posx = reduce_array_size(posx)
        posy = reduce_array_size(posy)
        angular_velocities = reduce_array_size(angular_velocities)

        with open(file_path, "w") as f:
            f.write(f"Nombre del video: {video_name}\n")
            f.write(f"Duración del video: {duration} segundos\n")
            f.write(f"Radio del primer círculo: {radius1} píxeles\n")
            f.write(f"Número de vueltas: {turns}\n")
            f.write(f"Aceleración: {aceleration}\n\n")

            # Guardar ángulos
            f.write("Ángulos (grados):\n")
            f.write(" ".join(map(str, angles)) + "\n\n")

            # Guardar posiciones x y y
            f.write("Posiciones X (píxeles):\n")
            f.write(" ".join(map(str, posx)) + "\n\n")
            f.write("Posiciones Y (píxeles):\n")
            f.write(" ".join(map(str, posy)) + "\n\n")

            # Guardar velocidades angulares
            f.write("Velocidades angulares (rad/s):\n")
            f.write(" ".join(map(str, angular_velocities)) + "\n")

        print(f"Información del video guardada exitosamente en {file_path}.")
    except Exception as e:
        print(f"Error al guardar la información: {e}")