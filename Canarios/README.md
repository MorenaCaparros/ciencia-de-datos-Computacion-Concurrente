# 🐤 Simulador de Canarios Concurrentes

Este proyecto es una simulación visual en Python que representa el comportamiento concurrente de 6 canarios en una jaula. Cada canario primero quiere **comer alpiste** (hasta 3 al mismo tiempo) y luego **columpiarse** (de a uno por vez). 

Se utiliza **Tkinter** para la interfaz gráfica y **semáforos** para la sincronización entre hilos (canarios).

---

## 🚀 Requisitos

- Python 3.10 o superior  
- Librerías necesarias:
  ```bash
  pip install pillow

## Estructura
- *canarios_semaforo.py*: script principal que ejecuta la simulación.
s
- *canario esperando.png*: imagen del canario en estado inactivo.

- *canario comiendo.png*: imagen del canario comiendo.

- *canario columpiandose.png*: imagen del canario en el columpio.

- *canario.png*: imagen final del canario con acciones completadas.

## 🧠 Lógica del sistema
Se utilizan semáforos para limitar el acceso:

comer_sem = Semaphore(3): solo 3 canarios pueden comer al mismo tiempo.

columpio_sem = Semaphore(1): solo un canario puede columpiarse a la vez.

Los canarios están representados por hilos (threads) que siguen esta secuencia:

Esperan un tiempo aleatorio.

Intentan comer (si hay lugar).

Esperan un tiempo aleatorio.

Intentan columpiarse (si está libre).

Finalizan.

## 🖼️ Interfaz visual
Cada canario aparece con:

Su número (Canario 1, Canario 2, etc.)

Su imagen según el estado actual.

Un texto debajo indicando su actividad: "Esperando", "Comiendo", "Columpiándose" o "Acciones finalizadas".