import sys
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from calculate import calculate_moves
from files import save_video_info

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Videos Circulares")
        self.root.geometry("400x300")
        self.root.configure(bg="#f7f7f7")

        title_label = tk.Label(root, text="Menú Principal", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=20)

        generate_button = tk.Button(root, text="Generar Video", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=self.open_video_generator)
        generate_button.pack(pady=10)

        calculate_button = tk.Button(root, text="Calcular Datos de Video", font=("Helvetica", 14), bg="#2196F3", fg="white", command=self.open_video_calculator)
        calculate_button.pack(pady=10)

    def open_video_generator(self):
        generator_window = tk.Toplevel(self.root)
        VideoGeneratorApp(generator_window)

    def open_video_calculator(self):
        calculator_window = tk.Toplevel(self.root)
        VideoCalculatorApp(calculator_window)

class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Video")
        self.root.geometry("400x700")
        self.root.configure(bg="#f7f7f7")

        title_label = tk.Label(root, text="Generador de Video Circular", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        self.label_video_name = tk.Label(root, text="Nombre del video:", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_video_name.pack(pady=5)
        self.video_name_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
        self.video_name_entry.pack(pady=5)

        self.label_duration = tk.Label(root, text="Duración del video (segundos):", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_duration.pack(pady=5)
        self.duration_spinbox = tk.Spinbox(root, from_=1, to=300, font=("Helvetica", 12), width=5)
        self.duration_spinbox.pack(pady=5)

        self.label_radius1 = tk.Label(root, text="Radio del primer círculo (píxeles):\n(En este sistema, 1px = 1 cm)", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_radius1.pack(pady=5)
        self.radius1_spinbox = tk.Spinbox(root, from_=1, to=500, font=("Helvetica", 12), width=5)
        self.radius1_spinbox.pack(pady=5)

        self.label_turns = tk.Label(root, text="Número de vueltas:", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_turns.pack(pady=5)
        self.turns_spinbox = tk.Spinbox(root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.turns_spinbox.pack(pady=5)

        self.acele = tk.Label(root, text="¿Cuál será la aceleración tangencial (m/s^2)?", font=("Helvetica", 12), bg="#f7f7f7")
        self.acele.pack(pady=5)
        self.acele_spinbox = tk.Spinbox(root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.acele_spinbox.pack(pady=5)

        select_path_button = tk.Button(root, text="Seleccionar ruta de guardado", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.select_save_path)
        select_path_button.pack(pady=10)

        self.save_path_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f7f7f7", fg="#333")
        self.save_path_label.pack(pady=5)

        generate_button = tk.Button(root, text="Generar video", font=("Helvetica", 14), bg="#FF5722", fg="white", command=self.generate_video)
        generate_button.pack(pady=20)

        self.save_path = ""

    def select_save_path(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.save_path_label.config(text=f"Ruta seleccionada: {self.save_path}")

    def generate_video(self):
        video_name = self.video_name_entry.get()
        if not video_name or not self.save_path:
            messagebox.showerror("Error", "Debe ingresar un nombre de video y seleccionar una ruta.")
            return

        duration = int(self.duration_spinbox.get())
        radius1 = int(self.radius1_spinbox.get())
        turns = int(self.turns_spinbox.get())
        acceleration = int(self.acele_spinbox.get())

        # Crear el video
        self.create_video(video_name, duration, radius1, turns, [2, 100], acceleration)
        messagebox.showinfo("Éxito", f"Video generado correctamente en {self.save_path}")

    def create_video(self, video_name, duration, radius1, turns, forces, aceleration):
        fps = 60
        width, height = 640, 480
        center = (width // 2, height // 2)
        total_frames = int(duration * fps)
        #time_force_applied = forces[0] * fps  # Momento en el que se aplica la fuerza, en fotogramas
        #force_value = forces[1]  # Magnitud de la fuerza aplicada
        video_path = f"{self.save_path}/{video_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        radius1 /= 100  # Convertir el radio a metros

        # Velocidad angular inicial
        angular_velocity = 2 * np.pi * turns / (fps * duration)
        angular_aceleration = aceleration / radius1
        
        for t in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            #Aplicar fuerza para cambiar la velocidad angular
            #if t == time_force_applied:
            #    angular_velocity += force_value / 1000  # Modificar este valor para ajustar el efecto de la fuerza
            # Calcular el ángulo actual usando la velocidad angular
            angular_velocity += aceleration / 3600
            angle = (angular_velocity * t ) % 360 

            # Posición del círculo
            x1 = int(center[0] + radius1 * np.cos(angle))
            y1 = int(center[1] + radius1 * np.sin(angle))
            cv2.circle(frame, (x1, y1), 20, (0, 255, 0), -1)

            # Dibujar el círculo mayor
            #cv2.circle(frame, center, radius1, (255, 255, 255), 2)

            out.write(frame)

        #save_video_info(video_name, duration, radius1, turns, angles, xpositions, ypositions, angular_velocities, acceleration, self.save_path)
        out.release()

class VideoCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculador de Datos")
        self.root.geometry("400x300")
        self.root.configure(bg="#f7f7f7")

        title_label = tk.Label(root, text="Calculador de Datos de Video", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        select_video_button = tk.Button(root, text="Seleccionar Video", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.select_video_path)
        select_video_button.pack(pady=10)

        self.save_video_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f7f7f7", fg="#333")
        self.save_video_label.pack(pady=5)

        calculate_button = tk.Button(root, text="Calcular", font=("Helvetica", 14), bg="#FF5722", fg="white", command=self.calculate_params)
        calculate_button.pack(pady=20)

        self.video_path = ""

    def select_video_path(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4;*.avi;*.mov;*.mkv")], title="Seleccione un archivo de video")
        if self.video_path:
            self.save_video_label.config(text=f"Video seleccionado: {self.video_path}")
        else:
            self.save_video_label.config(text="No se seleccionó ningún video")

    def calculate_params(self):
        if not self.video_path:
            messagebox.showerror("Error", "Debe seleccionar un video antes de calcular.")
            return

        calculate_moves(self.video_path)
        messagebox.showinfo("Éxito", "Cálculo completado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
