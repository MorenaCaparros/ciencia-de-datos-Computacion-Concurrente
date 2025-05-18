# Defino la función principal que simula el comportamiento de productor y consumidor
def productor_consumidor():
    buffer = [None] * 5
    # Variables que controlan el inicio (lectura) y el fin (escritura) del buffer circular

    inicio = 0 # Índice desde donde el consumidor leerá
    posfin = 0  # Índice donde el productor insertará
    tam = 0  # Cantidad actual de elementos en el buffer
    max_buffer = 5 # Tamaño máximo del buffer

    # Bucle principal que permite ejecutar múltiples operaciones hasta que el usuario decida salir

    while True:
        print("\nIngrese opción: 1 - Producir / 2 - Consumir / 0 - Salir")
        opcion = input("> ")

# Opción 1: Producir un nuevo valor
        if opcion == "1":
            if tam < max_buffer:
                valor = input("Ingrese un valor a producir: ")
                buffer[posfin] = valor
                posfin = (posfin + 1) % max_buffer # Avanza circularmente
                tam += 1  # Aumenta el contador de elementos
                print("Producto insertado.")
            else:
                # Si el buffer está lleno, el productor se bloquea (espera)

                print("Buffer lleno. Productor espera...")

        # Opción 2: Consumir un valor del buffer

        elif opcion == "2":
            if tam > 0:

                # Solo consume si hay datos disponibles
                print(f"Producto consumido: {buffer[inicio]}")
                buffer[inicio] = None  # Opcional, para ver el estado del buffer
                inicio = (inicio + 1) % max_buffer
                tam -= 1 # Reduce el contador de elementos
            else:
                # Si el buffer está vacío, el consumidor se bloquea (espera)

                print("Buffer vacío. Consumidor espera...")

        elif opcion == "0":
            print("Finalizando el programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el programa
productor_consumidor()
