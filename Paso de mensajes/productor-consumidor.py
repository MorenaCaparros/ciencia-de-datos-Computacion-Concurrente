import multiprocessing
import time
import random

# Función que simula el comportamiento del productor
def productor(id_prod, cola):
    for i in range(5):  # Cada productor produce 5 ítems
        item = f"item_{id_prod}_{i}"
        cola.put(("producir", item))  # Envía mensaje al servidor
        print(f"[Productor {id_prod}] Produjo: {item}")
        time.sleep(random.uniform(0.5, 1.5))
    cola.put(("fin_productor", id_prod))  # Señal de fin de producción

# Función que simula el comportamiento del consumidor
def consumidor(id_cons, cola):
    while True:
        cola.put(("consumir", id_cons))  # Solicita consumir al servidor
        respuesta = cola.get()  # Espera el ítem o "fin"
        if respuesta == "fin":
            break
        print(f"[Consumidor {id_cons}] Consumió: {respuesta}")
        time.sleep(random.uniform(0.5, 1.2))

# Servidor que administra el buffer, recibe y responde a los mensajes
def servidor(cola):
    buffer = []
    buffer_max = 5
    productores_finalizados = 0

    while True:
        if not cola.empty():
            mensaje = cola.get()

            if mensaje[0] == "producir":
                item = mensaje[1]
                if len(buffer) < buffer_max:
                    buffer.append(item)
                    print(f"[Servidor] Producto almacenado: {item}")
                else:
                    print("[Servidor] Buffer lleno. Ignorando producto temporalmente.")

            elif mensaje[0] == "consumir":
                id_cons = mensaje[1]
                if buffer:
                    item = buffer.pop(0)
                    cola.put(item)
                else:
                    cola.put("fin")  # Opción: también puede ser "espera"

            elif mensaje[0] == "fin_productor":
                productores_finalizados += 1
                if productores_finalizados == 2:  # Cantidad de productores
                    # Enviar señal de fin a los consumidores
                    for _ in range(2):  # Cantidad de consumidores
                        cola.put("fin")
                    break

if __name__ == "__main__":
    # Crear cola de mensajes
    cola_mensajes = multiprocessing.Queue()

    # Crear procesos
    procesos = [
        multiprocessing.Process(target=productor, args=(1, cola_mensajes)),
        multiprocessing.Process(target=productor, args=(2, cola_mensajes)),
        multiprocessing.Process(target=consumidor, args=(1, cola_mensajes)),
        multiprocessing.Process(target=consumidor, args=(2, cola_mensajes)),
        multiprocessing.Process(target=servidor, args=(cola_mensajes,))
    ]

    # Iniciar procesos
    for p in procesos:
        p.start()

    # Esperar que todos los procesos terminen
    for p in procesos:
        p.join()
