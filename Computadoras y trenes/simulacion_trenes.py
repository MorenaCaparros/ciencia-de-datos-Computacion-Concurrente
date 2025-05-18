from laboratorio import LaboratorioComputacion
import threading
import time
import random

# Configuración del sistema
cant_estaciones = 4   # Cantidad de estaciones que tiene el recorrido
trenes = 6            # Cantidad de trenes que circulan simultáneamente

# Instancia del "laboratorio", en este caso modelado como un conjunto de estaciones
lab = LaboratorioComputacion(cant_estaciones)

# Función que simula el comportamiento de cada tren
def tren(id_tren):
    estacion_actual = 0

    while estacion_actual < cant_estaciones:
        # El tren intenta ocupar la estación actual (bloquea si está ocupada)
        lab.usar_estacion(estacion_actual, id_tren)

        # Mensaje informando que ingresó
        print(f"Tren {id_tren} ingresó a estación {estacion_actual+1}")

        # Simula el tiempo que permanece en la estación
        time.sleep(random.uniform(1, 2))

        # Libera la estación para que otro tren pueda usarla
        lab.liberar_estacion(estacion_actual, id_tren)
        print(f"Tren {id_tren} salió de estación {estacion_actual+1}")

        # Avanza a la siguiente estación
        estacion_actual += 1

# Crear y lanzar los hilos para cada tren
hilos = []
for i in range(trenes):
    hilo = threading.Thread(target=tren, args=(i+1,))
    hilos.append(hilo)
    hilo.start()

    # Pequeño delay para que los trenes no salgan todos al mismo tiempo
    time.sleep(0.5)

# Esperar a que todos los trenes terminen su recorrido
for hilo in hilos:
    hilo.join()
