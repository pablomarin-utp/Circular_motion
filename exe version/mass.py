import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import cv2
from files import save_video_info, reduce_array_size, load_video_info

class MassConfigWindow:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent.root)
        self.root.title("Configuración de Masa y Objeto")
        self.root.geometry("400x600")
        self.root.configure(bg="#f7f7f7")

        title_label = tk.Label(self.root, text="Configuración de Masa y Objeto", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        # Configuración de número de vueltas
        self.label_turns = tk.Label(self.root, text="Número de vueltas:", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_turns.pack(pady=5)
        self.turns_spinbox = tk.Spinbox(self.root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.turns_spinbox.pack(pady=5)

        # Configuración de aceleración tangencial
        self.acele = tk.Label(self.root, text="Aceleración tangencial (m/s^2):", font=("Helvetica", 12), bg="#f7f7f7")
        self.acele.pack(pady=5)
        self.acele_spinbox = tk.Spinbox(self.root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.acele_spinbox.pack(pady=5)

        # Configuración de masa del objeto
        self.masac = tk.Label(self.root, text="Masa del objeto (kg):", font=("Helvetica", 12), bg="#f7f7f7")
        self.masac.pack(pady=5)
        self.masac_spinbox = tk.Spinbox(self.root, from_=1, to=100, font=("Helvetica", 12), width=5)
        self.masac_spinbox.pack(pady=5)

        # Configuración del color
        self.color_label = tk.Label(self.root, text="Color del objeto:", font=("Helvetica", 12), bg="#f7f7f7")
        self.color_label.pack(pady=5)

        # Colores disponibles como checkboxes
        self.colors = {
            "Rojo": (0, 0, 255),       # #FF0000 en BGR
            "Verde": (0, 255, 0),      # #00FF00 en BGR
            "Azul": (255, 0, 0),       # #0000FF en BGR
            "Amarillo": (0, 255, 255), # #FFFF00 en BGR
            "Naranja": (0, 165, 255),  # #FFA500 en BGR
        }

        self.color_vars = {color: tk.IntVar() for color in self.colors}
        for color, var in self.color_vars.items():
            tk.Checkbutton(self.root, text=color, variable=var, font=("Helvetica", 12), bg="#f7f7f7").pack(anchor="w", padx=20)

        # Botón de guardar
        save_button = tk.Button(self.root, text="Guardar", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.save_config)
        save_button.pack(pady=10)

        # Botón de omitir
        skip_button = tk.Button(self.root, text="Omitir configuración", font=("Helvetica", 12), bg="#FF5722", fg="white", command=self.skip_config)
        skip_button.pack(pady=5)

        # Para almacenar los valores guardados
        self.saved_data = []

    def save_config(self):
        # Crear una lista de colores (suponiendo que tienes una lista de colores predefinida)
        available_colors = list(self.color_vars.keys())  # Aquí asumo que self.color_vars tiene colores como claves
        
        # Crear tres diccionarios en un ciclo
        for i in range(3):
            # Obtener los valores ingresados
            turns = self.get_turns()
            acceleration = self.get_acceleration()
            mass = self.get_mass()

            # Verificar que exactamente un color esté seleccionado en cada iteración
            selected_color = available_colors[i % len(available_colors)]  # Seleccionamos un color de forma cíclica

            # Guardar los datos en el diccionario
            self.saved_data.append({
                "turns": turns,
                "acceleration": acceleration,
                "mass": mass,
                "color": self.colors[selected_color],  # Se usa el color correspondiente
            })
            
            # Limpiar los campos para la próxima iteración
            self.clear_fields()

        # Transferir los datos a la clase principal
        self.parent.mass_config_data.extend(self.saved_data)

        # Verificar si se ha alcanzado el límite de tres configuraciones
        if len(self.saved_data) >= 3:
            messagebox.showinfo("Guardado", "Se ha alcanzado el máximo de masas configuradas.")
            self.root.destroy()
        else:
            messagebox.showinfo("Guardado", "La configuración se ha guardado correctamente. ¿Desea configurar otra masa?")

    def skip_config(self):
        # Omitir la configuración y guardar una lista vacía
        self.saved_data = []
        self.parent.mass_config_data.append(self.saved_data)
        self.root.destroy()


    def clear_fields(self):
        # Limpiar los campos para permitir configurar otra masa
        self.turns_spinbox.delete(0, tk.END)
        self.acele_spinbox.delete(0, tk.END)
        self.masac_spinbox.delete(0, tk.END)
        for var in self.color_vars.values():
            var.set(0)

    def get_turns(self):
        return int(self.turns_spinbox.get())

    def get_acceleration(self):
        return int(self.acele_spinbox.get())

    def get_mass(self):
        return int(self.masac_spinbox.get())

    def get_saved_data(self):
        return self.saved_data


class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Video")
        self.root.geometry("400x500")
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

        self.label_radius1 = tk.Label(root, text="Radio del círculo (píxeles):\n(En este sistema, 1px = 1 cm)", font=("Helvetica", 12), bg="#f7f7f7")
        self.label_radius1.pack(pady=5)
        self.radius1_spinbox = tk.Spinbox(root, from_=1, to=500, font=("Helvetica", 12), width=5)
        self.radius1_spinbox.pack(pady=5)

        self.angular_acceleration_0_var = tk.BooleanVar()
        self.angular_acceleration_0_check = tk.Checkbutton(root, text="Aceleración angular 0", variable=self.angular_acceleration_0_var, font=("Helvetica", 12), bg="#f7f7f7")
        self.angular_acceleration_0_check.pack(pady=5)

        select_path_button = tk.Button(root, text="Seleccionar ruta de guardado", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.select_save_path)
        select_path_button.pack(pady=10)

        self.save_path_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f7f7f7", fg="#333")
        self.save_path_label.pack(pady=5)

        config_mass_button = tk.Button(root, text="Configurar masa y objeto", font=("Helvetica", 12), bg="#2196F3", fg="white", command=self.open_mass_config)
        config_mass_button.pack(pady=10)

        generate_button = tk.Button(root, text="Generar video", font=("Helvetica", 14), bg="#FF5722", fg="white", command=self.generate_video)
        generate_button.pack(pady=20)

        self.save_path = ""
        self.mass_config = None  # Para almacenar la referencia a la ventana de configuración de masas

    def open_mass_config(self):
        self.mass_config = MassConfigWindow(self)

    def select_save_path(self):
        self.save_path = filedialog.askdirectory()
        self.save_path_label.config(text=f"Ruta seleccionada: {self.save_path}")

    def generate_video(self):
        video_name = self.video_name_entry.get()
        if not video_name or not self.save_path:
            messagebox.showerror("Error", "Debe ingresar un nombre de video y seleccionar una ruta.")
            return

        if not self.mass_config_data:
            messagebox.showerror("Error", "Debe configurar la masa y el objeto.")
            return
        
        print(self.mass_config_data)

        duration = int(self.duration_spinbox.get())
        radius1 = int(self.radius1_spinbox.get())
        turns = self.mass_config_data["turns"]
        acceleration = self.mass_config_data["acceleration"]
        mass = self.mass_config_data["mass"]
        color = self.mass_config_data["color"]
        # Crear el video
        self.create_video(video_name, duration, radius1, turns, acceleration, mass, color)
        messagebox.showinfo("Éxito", f"Video generado correctamente en {self.save_path}")

    
    def create_video(self, video_name, duration, radius1, turns, aceleration, mass, color):
        fps = 30
        width, height = 640, 480
        center = (width // 2, height // 2)
        total_frames = int(duration * fps)
        video_path = f"{self.save_path}/{video_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))


        torque = mass * aceleration * radius1
        angular_velocities = np.array([])  # Usar arrays de NumPy
        xpositions = np.array([])  
        ypositions = np.array([])  
        angles = np.array([])
        centripetals = np.array([])

        # Aceleración angular calculada como α = a_t / r (en m)
        angular_acceleration = aceleration / radius1

        if self.angular_acceleration_0_var.get():
            angular_velocity = (2*np.pi*turns - 1/2*(aceleration/radius1)*((duration*fps)**2)) / (duration*fps)
        else: 
            angular_velocity = 2 * np.pi * turns / (fps * duration)

        # Velocidad angular inicial (calculada sin afectar la física)
        

        for t in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Calcular la nueva velocidad angular en cada frame
            
            
            angular_velocity += (angular_acceleration / fps) 

            angle = (angular_velocity * t)  # El ángulo se calcula usando la velocidad angular

            # Posición del círculo
            x1 = int(center[0] + radius1 * np.cos(angle))  # Usar el radio en píxeles
            y1 = int(center[1] + radius1 * np.sin(angle))  # Usar el radio en píxeles
            cv2.circle(frame, (x1, y1), 20, color, -1)  # Dibujar el círculo en el frame

            # Almacenar posiciones y ángulos para análisis
            xpositions = np.append(xpositions, x1 - center[0])
            ypositions = np.append(ypositions, y1 - center[1])
            angles = np.append(angles,(np.degrees(angle) % 360))
            angular_velocities = np.append(angular_velocities, angular_velocity)
            centripetals = np.append(centripetals, (angular_velocity**2) * radius1)
            out.write(frame)  # Escribir el frame en el video

        # Reducir el tamaño de las listas antes de guardar
        xpositions = reduce_array_size(xpositions,0)
        ypositions = reduce_array_size(ypositions,0)
        angles = reduce_array_size(angles,0)
        angular_velocities = reduce_array_size(angular_velocities,2)
        print(angles, len(angles))
        # Guardar información sobre el video generado
        save_video_info(video_name, duration, radius1, turns, angles, xpositions,
                         ypositions, angular_velocities, aceleration, angular_acceleration,
                           centripetals, torque, self.save_path)

        out.release()


