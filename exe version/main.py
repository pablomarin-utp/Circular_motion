import sys
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from calculate import calculate_moves, plot_data_from_file
from files import save_video_info, reduce_array_size, load_video_info
from mass import VideoGeneratorApp

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
        # Eliminar la extensión .mp4 y agregar _info.txt
        print(f"{self.video_path.rsplit('.', 1)[0]}_info.txt")
        video_name,duration, radius1, turns, angles, posx, posy, angular_velocities, aceleration, angular_ac, centripetals,torque = load_video_info(f"{self.video_path.rsplit('.', 1)[0]}_info.txt")
        
        plot_data_from_file(video_name, duration, radius1, turns, angles, 
                    posx, posy, angular_velocities, aceleration, 
                    angular_ac, centripetals,torque, 30 )
        messagebox.showinfo("Éxito", "Cálculo completado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()