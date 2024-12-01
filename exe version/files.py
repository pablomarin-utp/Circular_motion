def save_video_info(video_name, duration, radius1, turns, angles, posx, posy, angular_velocities, aceleration, save_path):
    # Crear un archivo de texto para guardar la información
    try:
        file_path = f"{save_path}/{video_name}_info.txt"
        with open(file_path, "w") as f:
            f.write(f"Nombre del video: {video_name}\n")
            f.write(f"Duración del video: {duration} segundos\n")
            f.write(f"Radio del primer círculo: {radius1} píxeles\n")
            f.write(f"Número de vueltas: {turns}\n")
            f.write(f"Aceleración: {aceleration}\n")

            # Guardar ángulos
            f.write("Ángulos (grados):\n")
            f.write(", ".join(f"{angle:.2f}" for angle in angles) + "\n\n")

            # Guardar posiciones x y y
            f.write("Posiciones X (píxeles):\n")
            f.write(", ".join(f"{x:.2f}" for x in posx) + "\n\n")
            f.write("Posiciones Y (píxeles):\n")
            f.write(", ".join(f"{y:.2f}" for y in posy) + "\n\n")

            # Guardar velocidades angulares
            f.write("Velocidades angulares (rad/s):\n")
            f.write(", ".join(f"{vel:.4f}" for vel in angular_velocities) + "\n")

        print(f"Información del video guardada exitosamente en {file_path}.")
    except Exception as e:
        print(f"Error al guardar la información: {e}")
