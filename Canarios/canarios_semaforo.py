import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import random

# Configuración de la ventana principal 
WIDTH = 800
HEIGHT = 600
CANT_CANARIOS = 6  # Número de canarios en la simulación

tk_root = tk.Tk()
tk_root.title("Columpio de Canarios")
tk_root.geometry(f"{WIDTH}x{HEIGHT}")

# Lienzo para mostrar gráficamente a los canarios
canvas = tk.Canvas(tk_root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

#Semáforos para sincronización 
comer_sem = threading.Semaphore(3)    # Solo 3 canarios pueden comer al mismo tiempo
columpio_sem = threading.Semaphore(1) # Solo 1 canario puede usar el columpio a la vez
mutex = threading.Lock()              # Lock general si en algún momento se usan variables compartidas

#Cargar imágenes para cada estado del canario
estados_imagenes = {
    "esperando": "Canarios/canario esperando.png",
    "comiendo": "Canarios/canario comiendo.png",
    "columpiandose": "Canarios/canario columpiandose.png",
    "finalizado": "Canarios/canario.png"
}

# Cargar y redimensionar imágenes
imagenes = {
    estado: ImageTk.PhotoImage(Image.open(estados_imagenes[estado]).resize((100, 100)))
    for estado in estados_imagenes
}

#Crear representación visual de los canarios
canarios = []

for i in range(CANT_CANARIOS):
    x = 50 + (i % 3) * 250  # Espaciado horizontal (3 por fila)
    y = 50 + (i // 3) * 250 # Espaciado vertical (dos filas)
    
    img_id = canvas.create_image(x, y, anchor=tk.NW, image=imagenes["esperando"])
    text_id = canvas.create_text(x + 50, y - 20, text=f"Canario {i+1}", font=("Arial", 12, "bold"))
    estado_id = canvas.create_text(x + 50, y + 110, text="Esperando", font=("Arial", 10))
    
    canarios.append({"img": img_id, "estado": estado_id, "text": text_id})

# Función para actualizar el estado visual de un canario 
def actualizar_estado(i, estado):
    canvas.itemconfig(canarios[i]["img"], image=imagenes[estado])
    if estado == "finalizado":
        canvas.itemconfig(canarios[i]["estado"], text="Acciones finalizadas", fill="gray")
    else:
        canvas.itemconfig(canarios[i]["estado"], text=estado.capitalize(), fill="black")

# Comportamiento de cada canario 
def comportamiento_canario(i):
    # Esperar un tiempo aleatorio antes de empezar (simula llegada desordenada como lo haria un canario)
    time.sleep(random.uniform(0.5, 2))
    actualizar_estado(i, "esperando")

    #  Etapa de comida 
    comer_sem.acquire()  # Espera si hay más de 3 comiendo
    actualizar_estado(i, "comiendo")
    time.sleep(random.uniform(2, 4))  # Simula tiempo que tarda en comer
    actualizar_estado(i, "esperando")
    comer_sem.release()

    #Pausa antes de usar el columpio
    time.sleep(random.uniform(1, 3))

    # Etapa del columpio
    columpio_sem.acquire()  # Solo uno puede columpiarse a la vez
    actualizar_estado(i, "columpiandose")
    time.sleep(random.uniform(2, 3))  # Simula duración del columpio
    columpio_sem.release()

    # Finaliza sus acciones 
    actualizar_estado(i, "finalizado")

# Función para iniciar todos los hilos de canarios 
def iniciar():
    for i in range(CANT_CANARIOS):
        threading.Thread(target=comportamiento_canario, args=(i,), daemon=True).start()

iniciar()

# Iniciar el loop de la interfaz gráfica
tk_root.mainloop()
