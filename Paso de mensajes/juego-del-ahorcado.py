import tkinter as tk
from tkinter import simpledialog, messagebox

# Dibujos del ahorcado en diferentes etapas de error (0 a 6)
AHORCADO_ASCII = [
    """
     ------
     |    |
          |
          |
          |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
          |
          |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
     |    |
          |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
    /|    |
          |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
    /|\\   |
          |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
    /|\\   |
    /     |
          |
    =========
    """,
    """
     ------
     |    |
     O    |
    /|\\   |
    / \\   |
          |
    =========
    """
]

# Clase que representa la interfaz y lógica del juego
class AhorcadoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado")
        
        self.frase_real = ""  # Frase original ingresada
        self.frase_mostrada = [] # Frase con letras ocultas
        self.intentos = 0 # Número de errores cometidos
        self.letras_adivinadas = set() # Letras que ya se intentaron
        
        # Dibujo del ahorcado
        self.label_ahorcado = tk.Label(root, text=AHORCADO_ASCII[0], font=("Courier", 12), justify="left")
        self.label_ahorcado.pack(pady=5)
        
        # Frase oculta
        self.label_frase = tk.Label(root, font=("Courier", 18))
        self.label_frase.pack(pady=10)
        
        # Instrucciones y campo de ingreso
        self.label_info = tk.Label(root, text="Ingrese una letra:", font=("Arial", 14))
        self.label_info.pack()
        
        self.entry_letra = tk.Entry(root, font=("Arial", 14))
        self.entry_letra.pack()
        self.entry_letra.bind("<Return>", self.procesar_letra)

        self.iniciar_juego()

    # Solicita al usuario la frase original y la valida
    def iniciar_juego(self):
        self.frase_real = simpledialog.askstring("Frase", "Ingrese una frase de hasta 40 caracteres:")
        if not self.frase_real or len(self.frase_real) > 40:
            messagebox.showerror("Error", "La frase es inválida.")
            self.root.destroy()  # Cierra si la frase no es válida
            return
        # Convierte la frase en una lista de guiones bajos (para ocultarla)
        self.frase_mostrada = ['_' if c != ' ' else ' ' for c in self.frase_real]
        self.actualizar_pantalla()

    # Actualiza los elementos visuales de la interfaz
    def actualizar_pantalla(self):
        self.label_frase.config(text=" ".join(self.frase_mostrada))
        self.label_ahorcado.config(text=AHORCADO_ASCII[self.intentos])

        # Verifica si se ganó o perdió el juego
        if self.intentos >= 6:
            messagebox.showinfo("Fin del juego", f"¡Perdiste! La frase era:\n{self.frase_real}")
            self.root.destroy()
        elif '_' not in self.frase_mostrada:
            messagebox.showinfo("Fin del juego", "¡Ganaste! Adivinaste la frase.")
            self.root.destroy()

    # Procesa cada letra ingresada por el jugador
    def procesar_letra(self, event=None):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END) # Limpia el campo
        if not letra.isalpha() or len(letra) != 1:
            messagebox.showwarning("Letra inválida", "Ingrese una sola letra.")
            return
        if letra in self.letras_adivinadas:
            return
        self.letras_adivinadas.add(letra)
        
        acierto = False
        # Verifica si la letra está en la frase original

        for idx, c in enumerate(self.frase_real.lower()):
            if c == letra:
                self.frase_mostrada[idx] = self.frase_real[idx] # Muestra la letra
                acierto = True
        
        if not acierto:
            self.intentos += 1 # Suma intento fallido
        
        self.actualizar_pantalla() # Refresca los elementos

# Código principal: crea la ventana y lanza el juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = AhorcadoGUI(root)
    root.mainloop()
