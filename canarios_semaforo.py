import threading
import time
import random

# Canario:
#     - Espera su turno para comer (semáforo del plato)
#     - Come (simulado con sleep)
#     - Libera el plato
#     - Espera su turno para columpiarse (semáforo del columpio)
#     - Se columpia (sleep)
#     - Libera el columpio

# Semáforos
sem_plato = threading.Semaphore(3)      # Solo 3 canarios pueden comer al mismo tiempo
sem_columpio = threading.Semaphore(1)   # Solo 1 canario puede columpiarse

def canario(nombre):
    print(f"{nombre} quiere comer.")
    sem_plato.acquire()
    print(f"{nombre} está comiendo.")
    time.sleep(random.uniform(1, 3))  # Tiempo aleatorio de comida
    print(f"{nombre} terminó de comer.")
    sem_plato.release()

    print(f"{nombre} quiere columpiarse.")
    sem_columpio.acquire()
    print(f"{nombre} está en el columpio.")
    time.sleep(random.uniform(1, 2))  # Tiempo aleatorio en el columpio
    print(f"{nombre} terminó de columpiarse.")
    sem_columpio.release()

# Crear e iniciar hilos para los canarios
nombres_canarios = [f"Canario {i}" for i in range(1, 7)]
hilos = []

for nombre in nombres_canarios:
    hilo = threading.Thread(target=canario, args=(nombre,))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos terminen
for hilo in hilos:
    hilo.join()
