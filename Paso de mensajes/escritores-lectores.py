import multiprocessing
import time
import random

# Función del proceso lector
# Cada lector solicita leer datos al servidor y espera la respuesta
def lector(id_lector, cola_lectura):
    while True:
        # Enviamos solicitud de lectura al servidor
        cola_lectura.put(("leer", id_lector))
        # Esperamos respuesta con los datos o señal de finalización
        respuesta = cola_lectura.get()
        if respuesta == "fin":
            break
        print(f"[Lector {id_lector}] Leyendo datos: {respuesta}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulamos el tiempo de lectura

# Función del proceso escritor
# Cada escritor genera datos y los envía al servidor para que los registre
def escritor(id_escritor, cola_lectura):
    for i in range(3):  # Simulamos que cada escritor produce 3 datos
        nuevo_dato = f"Dato_{id_escritor}_{i}"
        cola_lectura.put(("escribir", id_escritor, nuevo_dato))
        time.sleep(random.uniform(0.5, 2))  # Tiempo de escritura
    cola_lectura.put(("fin", id_escritor))  # Señalamos que este escritor terminó

# Función del servidor
# Administra las solicitudes de lectura y escritura y garantiza la sincronización
def servidor(cola_lectura):
    base_datos = []  # Almacena los datos escritos
    lectores_activos = 0
    fin_escritores = 0

    while True:
        if not cola_lectura.empty():
            mensaje = cola_lectura.get()

            # Si se trata de una solicitud de lectura
            if mensaje[0] == "leer":
                id_lector = mensaje[1]
                lectores_activos += 1  # Indicamos que hay un lector activo
                print(f"[Servidor] Lector {id_lector} solicita lectura.")
                cola_lectura.put(base_datos[:])  # Se envía una copia de la base de datos
                lectores_activos -= 1  # Finaliza la lectura

            # Si se trata de una solicitud de escritura
            elif mensaje[0] == "escribir":
                id_escritor, nuevo_dato = mensaje[1], mensaje[2]
                print(f"[Servidor] Escritor {id_escritor} solicita escritura: {nuevo_dato}")
                # Esperamos que no haya lectores activos antes de escribir
                while lectores_activos > 0:
                    print("[Servidor] Esperando a que lectores terminen...")
                    time.sleep(0.2)
                base_datos.append(nuevo_dato)

            # Si un escritor finaliza
            elif mensaje[0] == "fin":
                fin_escritores += 1
                # Si terminaron ambos escritores, finalizamos el servidor
                if fin_escritores == 2:
                    break

    # Notificamos a los lectores que ya no habrá más datos
    for _ in range(3):
        cola_lectura.put("fin")


if __name__ == "__main__":
    cola = multiprocessing.Queue()  # Creamos la cola de mensajes

    # Definimos los procesos: 3 lectores, 2 escritores y 1 servidor
    procesos = [
        multiprocessing.Process(target=lector, args=(1, cola)),
        multiprocessing.Process(target=lector, args=(2, cola)),
        multiprocessing.Process(target=lector, args=(3, cola)),
        multiprocessing.Process(target=escritor, args=(1, cola)),
        multiprocessing.Process(target=escritor, args=(2, cola)),
        multiprocessing.Process(target=servidor, args=(cola,))
    ]

    # Iniciamos todos los procesos
    for p in procesos:
        p.start()

    # Esperamos que todos los procesos finalicen
    for p in procesos:
        p.join()
