import numpy as np

# Supongamos que tienes una lista de ángulos por cada revolución.
# Por ejemplo:
angles = [
    [1.805, -3.014, -2.766, -2.392, -1.857, -1.817, -0.537, 0.146, 0.573, 1.588, 2.249, 2.836, -2.199, 0.031],
    [0.280, 0.453, 0.661, 1.016, 1.807, 3.098, -2.636, -1.472, -0.995, -0.621, -0.029]  # Ejemplo de otro conjunto
]

# Calculamos las diferencias de ángulo para ver si hay aceleración o no.
# Nota: Puedes ajustarlo a tus datos reales.
def is_accelerated(angles, time_diff_threshold=0.1):
    # Calcular las diferencias entre los ángulos sucesivos
    time_diffs = np.diff(angles)
    
    # Si la diferencia de tiempo se reduce cada vez, es acelerado
    is_accelerating = np.all(np.diff(time_diffs) < time_diff_threshold)
    
    return 1 if is_accelerating else 0

# Generar etiquetas (0 = no acelerado, 1 = acelerado)
labels = np.array([is_accelerated(rev) for rev in angles])

# Verificar los datos de etiquetas
print(labels)
