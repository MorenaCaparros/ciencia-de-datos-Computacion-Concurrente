# prod_cons_interfaz.py
# ─────────────────────────────────────────────────────────────
#  DEMO visual del monitor Productor–Consumidor
#  · Buffer circular de tamaño fijo
#  · Productores ENCOLAN cuando el buffer está lleno
#  · Consumidores ENCOLAN cuando está vacío
#  · Opcional FIFO estricto entre clientes en espera
#  · Manim Community v0.19
# ─────────────────────────────────────────────────────────────
from manim import *

#  Monitor lógico (sin hilos, sólo para la animación) 
class ProdConsMonitor:
    def __init__(self, capacidad: int, fifo: bool = True):
        self.cap   = capacidad              # tamaño del buffer
        self.buf   = []                     # lista con los “items”
        self.fifo  = fifo                   # ¿respeta orden de llegada?
        self.prod_wait = []                 # productores esperando (id, item)
        self.cons_wait = []                 # consumidores esperando (id)

    # — Producción —
    def produce(self, pid, item):
        if len(self.buf) < self.cap and (not self.fifo or not self.prod_wait):
            # hay hueco → produce inmediatamente
            self.buf.append(item)
            return "ok"
        # no hay hueco → se bloquea
        self.prod_wait.append((pid, item))
        return "wait"

    # — Consumo —
    def consume(self, cid):
        if self.buf and (not self.fifo or not self.cons_wait):
            itm = self.buf.pop(0)
            return "ok", itm
        # buffer vacío → se bloquea
        self.cons_wait.append(cid)
        return "wait", None

    # — Se invoca tras cada cambio para intentar desbloquear colas —
    def despachar(self):
        eventos = []          # [(tipo,   id, item/None), ...]
        while self.cons_wait and self.buf:
            cid = self.cons_wait.pop(0)
            itm = self.buf.pop(0)
            eventos.append(("cons_despierta", cid, itm))
        while self.prod_wait and len(self.buf) < self.cap:
            pid, itm = self.prod_wait.pop(0)
            self.buf.append(itm)
            eventos.append(("prod_despierta", pid, itm))
        return eventos


#  ESCENA MANIM 
class ProdConsScene(Scene):
    #  parámetros “macro” 
    N_PROD     = 3
    N_CONS     = 3
    BUFFER_SZ  = 4
    FIFO       = True   

    # Plan de acciones (tipo, id, item/opcional)
    PASOS = [
        ("produce", 1, "A"),
        ("produce", 2, "B"),
        ("produce", 3, "C"),
        ("consume",  1, None),
        ("consume",  2, None),
        ("produce", 1, "D"),
        ("produce", 2, "E"),
        ("consume",  3, None),
        ("consume",  1, None),
        ("consume",  2, None),
    ]

    #  utilidades gráficas 
    def _crear_actores(self):
        """Crea círculos productores arriba y consumidores abajo"""
        pxs = np.linspace(-6, 6, self.N_PROD)
        cxs = np.linspace(-6, 6, self.N_CONS)
        self.prods = VGroup(*[
            VGroup(
                Circle(0.4, color=WHITE, fill_opacity=1).set_fill(TEAL),
                Text(f"P{i+1}", font_size=22)
            ).arrange(ORIGIN).move_to([x, 3, 0])
            for i, x in enumerate(pxs)
        ])
        self.cons = VGroup(*[
            VGroup(
                Circle(0.4, color=WHITE, fill_opacity=1).set_fill(MAROON_B),
                Text(f"C{i+1}", font_size=22)
            ).arrange(ORIGIN).move_to([x, -3, 0])
            for i, x in enumerate(cxs)
        ])
        self.add(self.prods, self.cons)

    def _crear_buffer(self):
        self.slot_y = 0.5
        self.slots = [Square(1, color=YELLOW).move_to([-3 + k*2, self.slot_y, 0])
                      for k in range(self.BUFFER_SZ)]
        self.add(*self.slots)

    # flecha breve ↑ / ↓ con etiqueta
    def _flash(self, start, up=True, txt=""):
        vec = UP if up else DOWN
        arr = Arrow(start + vec*0.4, start + vec*1.2, buff=0, color=YELLOW)
        lab = Text(txt, font_size=20).next_to(arr, vec*0.2)
        self.play(Create(arr), FadeIn(lab), run_time=0.25)
        self.play(FadeOut(arr, lab), run_time=0.25)

    # mueve item visual (pequeño cuadrado con letra) hacia/un desde el buffer
    def _crear_item_mob(self, label):
        return Square(0.6, fill_color=PURPLE, fill_opacity=1).set_stroke(width=1)\
               .scale(0.8).add(Text(label, font_size=26))

    #  construct 
    def construct(self):
        # monitor “lógico”
        self.mon = ProdConsMonitor(self.BUFFER_SZ, fifo=self.FIFO)

        # escena base
        self._crear_actores()
        self._crear_buffer()
        self.wait(0.5)

        # tracking de items → slot idx
        slot_libre = 0
        items_gfx  = {}          # label -> (mobject, slot)

        # Recorro las acciones
        for paso, (tipo, who, itm) in enumerate(self.PASOS, 1):
            if tipo == "produce":
                actor = self.prods[who-1]
                # objeto visual del ítem
                item_mob = self._crear_item_mob(itm)
                item_mob.move_to(actor.get_center())
                self.add(item_mob)

                # intento producir
                estado = self.mon.produce(who, itm)
                if estado == "ok":
                    slot = len(self.mon.buf) - 1
                    destino = self.slots[slot].get_center()
                    items_gfx[itm] = (item_mob, slot)
                    self.play(item_mob.animate.move_to(destino), run_time=0.6)
                    self._flash(actor.get_center(), up=True, txt="produce")
                else:
                    self._flash(actor.get_center(), up=True, txt="FULL → espera")

            else:  # consume
                actor = self.cons[who-1]
                estado, itm_label = self.mon.consume(who)
                if estado == "ok":
                    mob, slot = items_gfx.pop(itm_label)
                    destino = actor.get_center()
                    self.play(mob.animate.move_to(destino), run_time=0.6)
                    self._flash(actor.get_center(), up=False, txt="consume")
                    self.remove(mob)
                else:
                    self._flash(actor.get_center(), up=False, txt="VACÍO → espera")

            # tras cada operación, despachar posibles desbloqueos
            eventos = self.mon.despachar()
            for ev_tipo, ev_id, ev_item in eventos:
                if ev_tipo == "cons_despierta":
                    # ya consumió arriba (se liberó hueco), así que sólo muestra mensaje
                    self._flash(self.cons[ev_id-1].get_center(), up=False, txt="¡despierta!")
                else:  # prod_despierta
                    prod_act = self.prods[ev_id-1]
                    mob, _   = items_gfx[ev_item]
                    slot = self.mon.buf.index(ev_item)
                    destino = self.slots[slot].get_center()
                    self.play(mob.animate.move_to(destino), run_time=0.5)
                    self._flash(prod_act.get_center(), up=True, txt="¡despierta!")
                    items_gfx[ev_item] = (mob, slot)

            self.wait(0.4)

        # FIN
        fin = Text("🏁 Fin de la simulación", font_size=30, color=BLUE).to_edge(UP)
        self.play(Write(fin))
        self.wait(1.5)


class ProdConsSceneFIFO(ProdConsScene):
    """Cola estricta (FIFO) para los bloqueados."""
    FIFO = True

