"""
canbialesInterfaz.py
---------------------------------
Pequeña animación con **Manim** que ilustra la
lógica del problema “Caníbales + Cocinero”
cuando la olla se rellena en ciclos fijos
y los caníbales van tomando turno rotativo
(para que todos coman la misma cantidad).

* Autor/a: Morena Caparrós  
* Asignatura: Computación Concurrente
"""

from manim import *
import numpy as np            

# ESCENA PRINCIPAL 
class CanibalesScene(Scene):
    """
    Cada escena en Manim hereda de Scene y sobre-escribe construct().
    Aquí dibujamos la olla, los seis caníbales y ejecuto 3 ciclos
    de recarga/consumo con 4 raciones cada vez.
    """

    #  CONSTRUCTOR 
    def construct(self):
        #  1. Parámetros de la simulación 
        N_CANIBALES        = 6      # actores “comensales”
        RACIONES_POR_CICLO = 4      # M  — relleno del cocinero
        N_CICLOS           = 3      # cuántas veces cocina

        #  2. Olla (fondo y contenido) 
        # Círculo exterior (la olla)
        olla = Circle(
            radius      = 1.0,
            color       = GREY,
            fill_opacity= 1
        ).shift(UP*1.5)             # la elevamos un poco

        # Círculo interior (el guiso). Opacidad 0 → vacía.
        contenido = Circle(
            radius      = 0.9,
            color       = ORANGE,
            fill_opacity= 0.0
        ).move_to(olla)

        # Animación inicial: aparece la olla
        self.play(Create(olla), FadeIn(contenido))

        #  3. Caníbales alrededor de la olla 
        # Posiciones x equiespaciadas en [-4, +4]
        xs = np.linspace(-4, 4, N_CANIBALES)

        # Dibujamos cada caníbal como un pequeño círculo verde
        canibales = VGroup(*[
            Circle(0.30, fill_color=GREEN, fill_opacity=1)
            .move_to([x, -2, 0])     # todos a la misma altura y z=0
            for x in xs
        ])

        # Etiquetamos con los números 1..6 centrados en cada círculo
        etiquetas = VGroup(*[
            Text(str(i+1), font_size=24).move_to(canibales[i])
            for i in range(N_CANIBALES)
        ])

        # Entrada en escena (ligeramente escalonada)
        self.play(
            LaggedStart(
                *[FadeIn(circle, label)
                  for circle, label in zip(canibales, etiquetas)],
                lag_ratio=0.15)
        )
        self.wait(0.4)

        #  4. Simulación de n ciclos 
        turno = 0   # “puntero” al próximo caníbal que va a comer

        for ciclo in range(N_CICLOS):

            #  4.1 Cocinero rellena la olla 
            mensaje = Text(
                f"👨‍🍳 Ciclo {ciclo+1}: Se despierta al Cocinero y rellena la olla "
                f"{RACIONES_POR_CICLO} raciones",
                font_size=24
            ).to_edge(UP)

            self.play(Write(mensaje))
            # Opacidad al 70 % → la olla se “ve llena”
            self.play(contenido.animate.set_fill(ORANGE, opacity=0.7),
                      run_time=0.4)
            self.remove(mensaje)     # quitamos el aviso

            #  4.2 Cada ración se sirve a un caníbal 
            for r in range(RACIONES_POR_CICLO):

                # caníbal al que le toca según el “puntero”
                canibal      = canibales[turno]
                etiqueta_num = etiquetas[turno].text  # ‘1’..‘6’
                quedan       = (RACIONES_POR_CICLO-1) - r  # raciones tras comer

                aviso = Text(
                    f"🍗 Caníbal {etiqueta_num} come "
                    f"({quedan} quedan)",
                    font_size=22
                ).to_edge(DOWN)

                # Cambia a amarillo mientras come
                self.play(
                    canibal.animate.set_fill(YELLOW),
                    Write(aviso),
                    run_time=0.25
                )
                self.wait(0.25)
                # Vuelve a verde y retiramos el aviso
                self.play(
                    canibal.animate.set_fill(GREEN),
                    FadeOut(aviso),
                    run_time=0.25
                )

                # Avanzamos el turno al siguiente caníbal (circular)
                turno = (turno + 1) % N_CANIBALES

            #  4.3 Olla queda vacía 
            self.play(contenido.animate.set_fill(ORANGE, opacity=0.0),
                      run_time=0.4)
            self.wait(0.3)

        #  5. Mensaje final 
        fin = Text(
            "🏁 El cocinero cierra la cocina – ¡fin del banquete!",
            font_size=28,
            color=BLUE
        ).to_edge(UP)

        self.play(Write(fin))
        self.wait(1.5)
