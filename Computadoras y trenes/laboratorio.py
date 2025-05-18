from threading import Semaphore, Lock

class LaboratorioComputacion:
    def __init__(self, cantidad_recursos):
        """
        Inicializa el laboratorio o sistema de estaciones con una cantidad fija de recursos compartidos.
        Estos recursos pueden representar computadoras (para estudiantes) o estaciones (para trenes).
        """
        self.recursos = [True] * cantidad_recursos  # Lista que indica si cada recurso está disponible
        self.semaforo = Semaphore(cantidad_recursos)  # Controla la cantidad máxima de accesos simultáneos
        self.lock = Lock()  # Exclusión mutua para modificar el estado de recursos

    def usar_computadora(self, estudiante_id):
        """
        Método llamado por un estudiante cuando quiere usar una computadora.
        Bloquea si no hay computadoras disponibles.
        Devuelve el índice de la computadora asignada.
        """
        self.semaforo.acquire()  # Espera si ya están ocupadas todas las computadoras
        with self.lock:  # Entra en sección crítica
            for i, libre in enumerate(self.recursos):
                if libre:
                    self.recursos[i] = False  # Marca la computadora como ocupada
                    return i  # Devuelve el ID de la computadora asignada

    def liberar_computadora(self, id_computadora):
        """
        Libera la computadora que estaba en uso, marcándola como disponible nuevamente.
        """
        with self.lock:
            self.recursos[id_computadora] = True  # Marca la computadora como libre
        self.semaforo.release()  # Permite que otro estudiante pueda usarla

    def usar_estacion(self, estacion_id, tren_id):
        """
        Método llamado por un tren que quiere ingresar a una estación.
        Usa semáforo para bloquear si todas están ocupadas.
        Devuelve True si pudo entrar, False si no (aunque esto no se usa con bloqueo=False).
        """
        self.semaforo.acquire()  # Espera si no hay estaciones disponibles
        with self.lock:
            if self.recursos[estacion_id]:  # Si la estación está libre
                self.recursos[estacion_id] = False  # La ocupa
                print(f"Tren {tren_id} entra en estación {estacion_id+1}")
                return True
            else:
                self.semaforo.release()  # Si no estaba libre, libera el semáforo
                return False

    def liberar_estacion(self, estacion_id, tren_id):
        """
        Libera la estación que estaba ocupada por un tren.
        """
        print(f"Tren {tren_id} salió de la estación {estacion_id + 1}")

        with self.lock:
            self.recursos[estacion_id] = True  # Marca la estación como libre
            print(f"Tren {tren_id} sale de estación {estacion_id+1}")
        self.semaforo.release()  # Permite que otro tren pueda usarla
