import numpy as np

def reduce_array_size(arr,num=0, max_length=1024):
    """
    Reduce el tamaño de un array de NumPy calculando el promedio entre pares sucesivos
    hasta que el tamaño sea menor o igual a max_length.
    """
    while len(arr) > max_length:
        arr = (arr[::2] + arr[1::2]) / 2  # Promedio de pares sucesivos
    return np.round(arr,num)  # Convertir a enteros
def save_video_info(video_name, duration, radius1, turns, angles, 
                    posx, posy, angular_velocities, aceleration, 
                    angular_ac, centripetals, torque , save_path):
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
        angular_velocities = reduce_array_size(angular_velocities,2)
        centripetals = reduce_array_size(centripetals,2)

        with open(file_path, "w") as f:
            f.write(f"{video_name}\n")
            f.write(f"{video_name}\n")
            f.write(f"{duration}\n")
            f.write(f"{radius1}\n")
            f.write(f"{turns}\n")
            f.write(f"{aceleration}\n")
            f.write(f"{angular_ac}\n")

            # Guardar los ángulos
            f.write(" ".join(map(str, angles)) + "\n")

            # Guardar posiciones X y Y
            f.write(" ".join(map(str, posx)) + "\n")
            f.write(" ".join(map(str, posy)) + "\n")

            # Guardar velocidades angulares
            f.write(" ".join(map(str, angular_velocities)) + "\n")

            # Guardar aceleraciones centrípetas
            f.write(" ".join(map(str, centripetals)) + "\n")
            f.write(f"{torque}\n")

        print(f"Información del video guardada exitosamente en {file_path}.")
    except Exception as e:
        print(f"Error al guardar la información: {e}")


def load_video_info(file_path):
    """
    Carga la información de un video desde un archivo de texto y devuelve los valores desempaquetados.
    """
    try:
        with open(file_path, "r") as f:
            # Leer todas las líneas del archivo
            lines = f.readlines()

            # Eliminar saltos de línea y espacios extraños
            lines = [line.strip() for line in lines]

            # Desempaquetar los datos
            video_name = lines[1]
            duration = float(lines[2])
            radius1 = float(lines[3])
            turns = int(lines[4])
            aceleration = float(lines[5])
            angular_ac = float(lines[6])

            # Convertir los siguientes elementos en listas de números
            angles = list(map(float, lines[7].split()))
            posx = list(map(float, lines[8].split()))
            posy = list(map(float, lines[9].split()))
            angular_velocities = list(map(float, lines[10].split()))
            centripetals = list(map(float, lines[11].split()))
            torque = float(lines[12])            
        return video_name, duration, radius1, turns, angles, posx, posy, angular_velocities, aceleration, angular_ac, centripetals, torque
    except Exception as e:
        print(f"Error al cargar la información: {e}")
        return None
    
