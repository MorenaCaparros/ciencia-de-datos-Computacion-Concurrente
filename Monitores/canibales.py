import threading
import time
import random

M = 4    # raciones por recarga
N = 6    # número de caníbales
S = 3    # cuántas veces recarga el cocinero antes de terminar

class Olla:
    def __init__(self, capacidad, ciclos_max):
        self.capacidad = capacidad
        self.raciones = 0
        self.ciclos = 0
        self.ciclos_max = ciclos_max
        self.lock = threading.Lock()
        # condición para despertar al cocinero
        self.cocinerocond = threading.Condition(self.lock)
        # condición para despertar a los caníbales
        self.canibalcond = threading.Condition(self.lock)

    def servirse(self, id_canibal):
        with self.lock:
            # si no hay raciones y quedan recargas, avisar al cocinero
            while self.raciones == 0 and self.ciclos < self.ciclos_max:
                print(f"🥄 Caníbal {id_canibal} ve la olla vacía y despierta al cocinero")
                self.cocinerocond.notify()      # despierta al cocinero
                self.canibalcond.wait()         # espera a que haya raciones

            # si ya no quedan recargas, salgo
            if self.raciones == 0 and self.ciclos >= self.ciclos_max:
                return False

            # tomo mi ración
            self.raciones -= 1
            print(f"🍗 Caníbal {id_canibal} come. Quedan {self.raciones} raciones")

            # si aún hay raciones, despierto al siguiente caníbal
            if self.raciones > 0:
                self.canibalcond.notify()
            return True

    def cocinar(self):
        while True:
            with self.lock:
                # espero hasta que alguien me llame (cuando raciones == 0)
                while self.raciones > 0 and self.ciclos < self.ciclos_max:
                    self.cocinerocond.wait()

                if self.ciclos >= self.ciclos_max:
                    # no quedan más recargas, despierto a cualquier caníbal para que salgan
                    self.canibalcond.notify_all()
                    break

                # recargo
                self.raciones = self.capacidad
                self.ciclos += 1
                print(f"👨‍🍳  El cocinero rellena {self.capacidad} raciones (ciclo {self.ciclos}/{self.ciclos_max})")
                # despierto a todos los caníbales
                self.canibalcond.notify_all()

            # simulo tiempo de cocinar
            time.sleep(random.uniform(0.5, 1.5))


def canibal(id_canibal, olla):
    # cada caníbal intentará servirse hasta que devuelva False
    while olla.servirse(id_canibal):
        # simulo tiempo de “digerir” antes de volver a la olla
        time.sleep(random.uniform(0.2, 0.8))
    print(f"💀 Caníbal {id_canibal} se retira (no quedan recargas)")

def cocinero(olla):
    olla.cocinar()
    print("🏁 El cocinero ha terminado sus recargas y cierra la cocina")


if __name__ == "__main__":
    olla = Olla(capacidad=M, ciclos_max=S)

    # lanzo al cocinero
    hilo_coc = threading.Thread(target=cocinero, args=(olla,))
    hilo_coc.start()

    # lanzo a los caníbales
    hilos = []
    for i in range(1, N+1):
        h = threading.Thread(target=canibal, args=(i, olla))
        hilos.append(h)
        h.start()

    # espero a que terminen todos
    for h in hilos:
        h.join()
    hilo_coc.join()
    print("🌴 Todos los caníbales y el cocinero ya han terminado.")

