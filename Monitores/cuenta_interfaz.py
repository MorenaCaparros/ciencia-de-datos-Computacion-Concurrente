# cuenta_interfaz.py
# -----------------------------------------------------------
#  SIMULACIÓN DEL MONITOR "CUENTA DE AHORRO" CON MANIM
#  · Saldo nunca negativo
#  · Retiradas respetan cola FIFO (o no, según escena)
#  · Clientes -> círculos numerados
# -----------------------------------------------------------
from manim import *

# =============== LOGIC (monitor “virtual”) ==================
class CuentaMonitor:
    """Pequeño monitor lógico (sin hilos reales) para la animación"""
    def __init__(self, saldo_inicial=0, fifo=True):
        self.saldo          = saldo_inicial
        self.fifo           = fifo          # Si False, cualquiera retira si hay saldo
        self.cola_espera    = []            # ids que esperan retirar

    def depositar(self, cli_id, monto):
        self.saldo += monto
        # al depositar se despiertan TODOS los que esperaban
        esperar = self.cola_espera.copy()
        self.cola_espera.clear()
        return esperar                      # quiénes se despertaron

    def retirar(self, cli_id, monto):
        if monto <= self.saldo and (not self.fifo or cli_id == self._primero()):
            self.saldo -= monto
            return True                     # pudo retirar
        # no pudo → se encola si no estaba
        if cli_id not in self.cola_espera:
            self.cola_espera.append(cli_id)
        return False

    def _primero(self):
        return self.cola_espera[0] if self.cola_espera else None


# =================   SCENA BASE =============================
class CuentaBaseScene(Scene):
    # parámetros comunes
    N_CLIENTES   = 5
    SALDO_INICIAL= 100
    PASOS        = [                       # (tipo, id, monto)
        ('retira', 1, 80),
        ('retira', 2, 50),
        ('deposita',3, 60),
        ('retira', 2, 50),
        ('retira', 4, 30),
        ('deposita',5, 40),
    ]

    FIFO = True  # la sub-clase lo cambiará

    # ---------- helpers visuales ----------
    def _crear_clientes(self):
        xs = np.linspace(-5, 5, self.N_CLIENTES)
        grupos = []
        for i, x in enumerate(xs):
            circ = Circle(0.35, color=WHITE, fill_opacity=1).set_fill(GREEN)
            txt  = Text(str(i + 1), font_size=22).move_to(circ)
            grupo = VGroup(circ, txt).move_to([x, -2, 0])   # <- el grupo tiene la posición
            grupos.append(grupo)

        self.clientes = VGroup(*grupos)
        self.add(self.clientes)


    def _crear_saldo(self):
        marco = Rectangle(width=7,height=1.2,stroke_color=BLUE)
        marco.to_edge(UP)
        self.vsaldo = ValueTracker(self.SALDO_INICIAL)
        self.txt_saldo = DecimalNumber(self.vsaldo.get_value(),num_decimal_places=0,
                                       font_size=40).move_to(marco.get_center())
        label = Text("Saldo:",font_size=32).next_to(self.txt_saldo,LEFT,0.3)
        self.add(marco,label,self.txt_saldo)

        # actualizador para que el número siga a vsaldo
        self.txt_saldo.add_updater(
            lambda m: m.set_value(self.vsaldo.get_value()).move_to(marco.get_center())
        )

    def _cola_visual(self):
        """Rectángulos abajo para mostrar la cola FIFO"""
        self.slot_y = -0.5
        self.slots = [Square(0.7,color=YELLOW).move_to([-4+1.1*k,self.slot_y,0])
                      for k in range(self.N_CLIENTES)]
        self.add(*self.slots)

    # ---------------------------------------------------------
    def construct(self):
        # 1. Lógica del monitor
        self.monitor = CuentaMonitor(self.SALDO_INICIAL,fifo=self.FIFO)

        # 2. Elementos visuales
        self._crear_clientes()
        self._crear_saldo()
        self._cola_visual()
        self.wait(0.5)

        # 3. Simulación paso a paso
        posiciones_cola = {}   # cli_id -> slot index
        prox_slot        = 0

        for paso,tipo,cli,monto in [(i,*p) for i,p in enumerate(self.PASOS,1)]:
            circ = self.clientes[cli-1]          # el círculo del cliente

            if tipo == 'deposita':
                circ.set_fill(GREEN_E)
                orig = circ.get_center()  # guardo posición
                destino = self.txt_saldo.get_center() + DOWN*0.2   # un pelín debajo del nº
                self.play(circ.animate.move_to(destino).scale(1.2), run_time=0.3)
                self._animar_flecha(circ, arriba=True,text=f"+${monto}")
                despiertos = self.monitor.depositar(cli,monto)
                self.play(self.vsaldo.animate.increment_value(monto), run_time=0.4)
                self.play(circ.animate.move_to(orig).scale(1/1.2), run_time=0.3)

                # Sacar de la cola visual a los despiertos
                for d in despiertos:
                    idx = posiciones_cola.pop(d)
                    self._mover_a_fuera_cola(d, idx)
                    prox_slot = min(prox_slot, idx)   # libera hueco

            else:  # retira
                puede = self.monitor.retirar(cli,monto)
                if puede:
                    circ.set_fill(RED_E)
                    self.play(circ.animate.scale(1.2), run_time=0.2)
                    self._animar_flecha(circ, arriba=False,text=f"-${monto}")
                    self.play(self.vsaldo.animate.increment_value(-monto), run_time=0.4)
                    self.play(circ.animate.scale(1/1.2), run_time=0.2)
                else:
                    # Entra / permanece en cola
                    if cli not in posiciones_cola:
                        slot = prox_slot
                        posiciones_cola[cli] = slot
                        prox_slot += 1
                        self._mover_a_cola(cli, slot)
                    circ.set_fill(GREY)

            self.wait(0.3)

        # 4. Mensaje final
        fin = Text("🏁 El banco cierra operaciones", font_size=28, color=BLUE).to_edge(UP)
        self.play(Write(fin))
        self.wait(1.5)

    # ---------- pequeñas animaciones auxiliares ----------
    def _animar_flecha(self, circ, arriba=True, text=""):
        y_dir = UP if arriba else DOWN
        flecha = Arrow(circ.get_center()+y_dir*0.4,
                       circ.get_center()+y_dir*1.2,
                       buff=0, color=YELLOW)
        lbl = Text(text,font_size=20).next_to(flecha,y_dir*0.3)
        self.play(Create(flecha), FadeIn(lbl), run_time=0.25)
        self.play(FadeOut(flecha,lbl), run_time=0.25)

    def _mover_a_cola(self, cli_id, slot_idx):
        """Desplaza el VGroup del cliente al cuadro de la cola (slot amarillo)."""
        grp      = self.clientes[cli_id - 1]            
        destino  = self.slots[slot_idx].get_center()
        self.play(grp.animate.move_to(destino), run_time=0.40)


    def _mover_a_fuera_cola(self, cli_id, slot_idx):
        """Devuelve el cliente a su posición original"""
        grp      = self.clientes[cli_id - 1]
        destino  = np.array([
            -5 + 10 * (cli_id - 1) / (self.N_CLIENTES - 1),   # misma fórmula que al crear
            -2,
            0
        ])
        self.play(
            grp.animate.move_to(destino).set_fill(GREEN),     # vuelve a color normal
            run_time=0.40
        )


# ============ Dos escenas derivadas ================
class CuentaFIFOScene(CuentaBaseScene):
    """Con cola estricta: nadie se cuela"""
    FIFO = True

class CuentaColaLibreScene(CuentaBaseScene):
    """Permite saltar la cola si hay dinero"""
    FIFO = False
