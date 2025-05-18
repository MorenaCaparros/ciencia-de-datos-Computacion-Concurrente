import tkinter as tk
import threading
import random
from PIL import Image, ImageTk
import os
ruta_base = os.path.dirname(os.path.abspath(__file__))

colores = ["verde", "violeta", "amarillo", "azul", "gris", "rojo"]
imagenes_tren = {}
CANT_TRENES = 6
CANT_ESTACIONES = 4

WIDTH = 1100
HEIGHT = 650

# Colores
COLOR_LIBRE = "lightgray"
COLOR_OCUPADO = "green"

# Crear ventana
ventana = tk.Tk()
ventana.title("Simulador de Trenes")
for color in colores:
    ruta_img = os.path.join(ruta_base, "imagenes", f"tren_{color}.png")
    original = Image.open(ruta_img).convert("RGB").resize((80, 80))
    imagenes_tren[color] = ImageTk.PhotoImage(original)
    imagen_gris = original.convert("L").convert("RGB")  # Convertir a escala de grises y luego a RGB para Tkinter
    imagenes_tren[f"{color}_gris"] = ImageTk.PhotoImage(imagen_gris)

canvas = tk.Canvas(ventana, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

posicion_trenes = []
for i, color in enumerate(colores):
    x = 60
    y = 60 + i * 100
    img = canvas.create_image(x, y, image=imagenes_tren[color], anchor=tk.CENTER)
    label = canvas.create_text(x, y + 50, text=f"Tren {i+1}", font=("Arial", 10))
    posicion_trenes.append({"img": img, "color": color, "label": label})

# Crear estaciones visuales
espacio_x = WIDTH // (CANT_ESTACIONES + 1)
estaciones = []
semaforos_estaciones = [threading.Semaphore(1) for _ in range(CANT_ESTACIONES)]

for i in range(CANT_ESTACIONES):
    x = espacio_x * (i + 1)
    y = HEIGHT // 2
    rect = canvas.create_rectangle(x - 40, y - 40, x + 40, y + 40, fill=COLOR_LIBRE)
    texto = canvas.create_text(x, y - 60, text=f"Estación {i+1}", font=("Arial", 12))
    estaciones.append({"x": x, "y": y, "rect": rect, "texto": texto})

# Mover tren con after para que siempre actualice desde el hilo principal
def intentar_ocupar_estacion(tren_id, estacion):
    if estacion >= CANT_ESTACIONES:
        canvas.itemconfig(posicion_trenes[tren_id-1]["img"],
                  image=imagenes_tren[posicion_trenes[tren_id-1]["color"]])
        return

    ocupado = semaforos_estaciones[estacion].acquire(blocking=False)
    if not ocupado:
        ventana.after(300, lambda: intentar_ocupar_estacion(tren_id, estacion))
        return

    tren_color = posicion_trenes[tren_id-1]["color"]
    canvas.itemconfig(posicion_trenes[tren_id-1]["img"],
                      image=imagenes_tren[f"{tren_color}_gris"])
    tren_estacion = canvas.create_image(
        estaciones[estacion]["x"], estaciones[estacion]["y"],
        image=imagenes_tren[tren_color], anchor=tk.CENTER)

    def liberar():
        canvas.itemconfig(posicion_trenes[tren_id-1]["img"],
                          image=imagenes_tren[tren_color])
        canvas.delete(tren_estacion)
        semaforos_estaciones[estacion].release()
        ventana.after(500, lambda: intentar_ocupar_estacion(tren_id, estacion + 1))

    ventana.after(int(random.uniform(1500, 2500)), liberar)


for t in range(CANT_TRENES):
    ventana.after(t * 700, lambda tid=t+1: intentar_ocupar_estacion(tid, 0))

ventana.mainloop()
