from laboratorio import LaboratorioComputacion
import threading
import time
import random

# Crear una instancia del laboratorio con 4 computadoras disponibles
lab = LaboratorioComputacion(4)

# Función que representa el comportamiento de cada estudiante
def estudiante(id_estudiante):
    # Solicita una computadora (bloquea si no hay disponibles)
    id_compu = lab.usar_computadora(id_estudiante)

    # Imprime mensaje de inicio de uso
    print(f"Estudiante {id_estudiante} comenzó a usar la computadora {id_compu+1}")

    # Simula el tiempo que el estudiante está usando la computadora
    time.sleep(random.uniform(1, 2.5))

    # Libera la computadora al terminar
    lab.liberar_computadora(id_compu)

    # Imprime mensaje de finalización
    print(f"Estudiante {id_estudiante} terminó de usar la computadora {id_compu+1}")

# Lista para almacenar los hilos
hilos = []

# Crear y lanzar 6 hilos (uno por cada estudiante)
for i in range(6):
    hilo = threading.Thread(target=estudiante, args=(i+1,))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos (estudiantes) terminen
for hilo in hilos:
    hilo.join()
