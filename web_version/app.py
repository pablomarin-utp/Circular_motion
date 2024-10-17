import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from calculate import calculate_moves

app = Flask(__name__)
app.secret_key = "aguamil900ml"  # Cambia esto por una clave secreta en producción
@app.route("/sumbit", methods=["GET","POST"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("puso algo")  
        video_name = request.form.get("video_name")
        duration_str = request.form.get("duration")
        radius1_str = request.form.get("radius1")
        turns_str = request.form.get("turns")
        save_path = request.form.get("save_path")
        video_path = request.form.get("video_path")
        
        # Validar que los campos requeridos no estén vacíos
        if not video_name or not save_path:
            flash("Debe ingresar un nombre de video y seleccionar una ruta.")
            return redirect(url_for("index"))

        # Validar y convertir los campos a enteros
        try:
            duration = int(duration_str)
            radius1 = int(radius1_str)
            turns = int(turns_str)
        except (ValueError, TypeError):
            flash("Por favor, ingrese valores válidos para la duración, el radio y las vueltas.")
            return redirect(url_for("index"))

        # Generar el video con los parámetros proporcionados
        create_video(video_name, duration, radius1, turns, save_path)
        flash(f"Video generado correctamente en {save_path}/{video_name}.mp4")
        
        # Calcular movimientos si se proporcionó un video
        

        return redirect(url_for("index"))

    return render_template("index.html")

def create_video(video_name, duration, radius1, turns, save_path):
    fps = 30
    width, height = 640, 480
    center = (width // 2, height // 2)
    total_frames = int(duration * fps)

    video_path = f"{save_path}/{video_name}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for t in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        angle = 2 * np.pi * t / (fps * duration)

        # Posición del primer círculo
        x1 = int(center[0] + radius1 * np.cos(turns * angle))
        y1 = int(center[1] + radius1 * np.sin(turns * angle))
        cv2.circle(frame, (x1, y1), 10, (0, 255, 0), -1)

        # Dibujar el círculo mayor
        cv2.circle(frame, center, radius1, (255, 255, 255), 2)

        out.write(frame)

    out.release()

if __name__ == "__main__":
    app.run(debug=True)
