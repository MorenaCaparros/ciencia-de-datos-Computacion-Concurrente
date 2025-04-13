import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import random
# Configuración visual
WIDTH = 800
HEIGHT = 600
CANT_CANARIOS = 6

tk_root = tk.Tk()
tk_root.title("Columpio de Canarios")
tk_root.geometry(f"{WIDTH}x{HEIGHT}")

canvas = tk.Canvas(tk_root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Semáforos
comer_sem = threading.Semaphore(3)
columpio_sem = threading.Semaphore(1)
mutex = threading.Lock()  # Para proteger el acceso a variables compartidas

# Contadores para saber cuántos están comiendo y columpiándose
canarios_comiendo = 0
canarios_columpiandose = 0

# Cargar imágenes
estados_imagenes = {
    "esperando": "canario esperando.png",
    "comiendo": "canario comiendo.png",
    "columpiandose": "canario columpiandose.png",
    "finalizado": "canario.png"
}

imagenes = {estado: ImageTk.PhotoImage(Image.open(estados_imagenes[estado]).resize((100, 100))) for estado in estados_imagenes}

# Datos visuales de los canarios
canarios = []

for i in range(CANT_CANARIOS):
    x = 50 + (i % 3) * 250
    y = 50 + (i // 3) * 250
    img_id = canvas.create_image(x, y, anchor=tk.NW, image=imagenes["esperando"])
    text_id = canvas.create_text(x + 50, y - 20, text=f"Canario {i+1}", font=("Arial", 12, "bold"))
    estado_id = canvas.create_text(x + 50, y + 110, text="Esperando", font=("Arial", 10))
    canarios.append({"img": img_id, "estado": estado_id, "text": text_id})

def actualizar_estado(i, estado):
    canvas.itemconfig(canarios[i]["img"], image=imagenes[estado])
    if estado == "finalizado":
        canvas.itemconfig(canarios[i]["estado"], text="Acciones finalizadas", fill="gray")
    else:
        canvas.itemconfig(canarios[i]["estado"], text=estado.capitalize(), fill="black")

def comportamiento_canario(i):
    time.sleep(random.uniform(0.5, 2))  # escalonar llegada pero es random dado que un canario puede tardar x cantidad de tiempo 
    actualizar_estado(i, "esperando")

      # Comer
    comer_sem.acquire()
    actualizar_estado(i, "comiendo")
    time.sleep(random.uniform(2, 4))
    actualizar_estado(i, "esperando")
    comer_sem.release()

    # Esperar un poco antes de columpiarse
    time.sleep(random.uniform(1, 3))

    # Columpiarse
    columpio_sem.acquire()
    actualizar_estado(i, "columpiandose")
    time.sleep(random.uniform(2, 3))
    columpio_sem.release()

    actualizar_estado(i, "finalizado")

def iniciar():
    for i in range(CANT_CANARIOS):
        threading.Thread(target=comportamiento_canario, args=(i,), daemon=True).start()

iniciar()
tk_root.mainloop()