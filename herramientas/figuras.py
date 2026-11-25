"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py [--png]
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def lienzo(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.2, fontweight=peso)


def flecha(ax, a, b, color=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def pagina(ax, x, y, w, h, titulo):
    caja(ax, x, y, w, h, None, fc=SUP, ec=TINTA2, r=0.06)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=CAJA, ec=TINTA2, lw=1.2))
    ax.text(x + 0.15, y + h - 0.175, titulo, ha="left", va="center", fontsize=9, color=TINTA2)
    for i in range(5):
        ax.plot([x + 0.2, x + w - 0.2 - (0.5 if i % 2 else 0)], [y + h - 0.7 - i * 0.32] * 2,
                color=GRIS, lw=3, solid_capstyle="round")





def i1_ramas():
    fig, ax = lienzo(7.9, 4.4, (0, 11.6), (0, 6.2))
    ramas = [("1. Percibir", "identificar emociones"), ("2. Usar", "facilitar el pensamiento"), ("3. Comprender", "causas y evolución"), ("4. Regular", "gestionar según objetivos")]
    for i, (t, st) in enumerate(ramas):
        x, y = 0.4 + i * 1.3, 0.3 + i * 1.4
        ax.add_patch(FancyBboxPatch((x, y), 6.4, 1.2, boxstyle="round,pad=0,rounding_size=0.12", fc=S[i], ec="none", alpha=0.22))
        ax.text(x + 0.3, y + 0.78, t, fontsize=12.5, fontweight="bold", color=TINTA, va="center")
        ax.text(x + 0.3, y + 0.34, st, fontsize=10, color=TINTA2, va="center")
    flecha(ax, (11.3, 0.5), (11.3, 5.7)); ax.text(10.95, 3.1, "más complejas", rotation=90, ha="center", va="center", fontsize=10, color=TINTA2)
    guardar(fig, "i1_ramas.svg")


def i2_circumplejo():
    fig, ax = lienzo(7.0, 5.6, (-5.6, 5.6), (-4.6, 4.6))
    for (sx, sy), c in (((-1, 1), S[1]), ((1, 1), S[3]), ((-1, -1), S[0]), ((1, -1), S[2])):
        ax.add_patch(FancyBboxPatch((0.15 if sx > 0 else -5.15, 0.15 if sy > 0 else -4.15), 5.0, 4.0, boxstyle="round,pad=0,rounding_size=0.15", fc=c, ec="none", alpha=0.15))
    flecha(ax, (-5.4, 0), (5.4, 0)); flecha(ax, (0, -4.4), (0, 4.4))
    ax.text(5.3, -0.4, "Agradable", ha="right", fontsize=10, color=TINTA2); ax.text(-5.3, -0.4, "Desagradable", ha="left", fontsize=10, color=TINTA2)
    ax.text(0.2, 4.2, "Activación alta", fontsize=10, color=TINTA2); ax.text(0.2, -4.35, "Activación baja", fontsize=10, color=TINTA2)
    pts = [(-3.6, 2.9, "ansiedad"), (-2.2, 1.9, "frustración"), (-4.0, 1.2, "enfado"), (2.4, 3.0, "entusiasmo"), (3.9, 1.8, "curiosidad"), (1.6, 1.1, "orgullo"),
           (-3.5, -1.3, "desánimo"), (-1.8, -2.6, "tristeza"), (-3.9, -3.4, "aburrimiento"), (3.6, -1.4, "satisfacción"), (1.8, -2.4, "alivio"), (3.8, -3.3, "calma")]
    for x, y, t in pts:
        ax.plot([x], [y], "o", ms=6, color=TINTA); ax.text(x, y + 0.3, t, ha="center", fontsize=10.5, color=TINTA)
    guardar(fig, "i2_circumplejo.svg")


def i3_proceso():
    fig, ax = lienzo(10, 4.0, (0, 15), (-0.6, 5.2))
    etapas = ["Situación", "Atención", "Valoración", "Respuesta"]
    for i, t in enumerate(etapas):
        caja(ax, 0.4 + i * 3.7, 3.3, 2.8, 1.1, t, fs=12, peso="bold")
        if i < 3: flecha(ax, (3.2 + i * 3.7, 3.85), (4.1 + i * 3.7, 3.85))
    fam = [(0.8, "Selección de\nla situación", S[0]), (2.8, "Modificación de\nla situación", S[0]), (5.5, "Despliegue de\nla atención", S[1]), (9.2, "Cambio\ncognitivo", S[2]), (12.9, "Modulación de\nla respuesta", S[4])]
    for x, t, c in fam:
        ax.add_patch(FancyArrowPatch((x, 1.45 if x != 2.8 else 0.6), (x, 3.25), arrowstyle="-|>", mutation_scale=12, color=c, lw=1.8))
        ax.text(x, 0.85 if x != 2.8 else 0.0, t, ha="center", va="center", fontsize=9.5, color=TINTA, linespacing=1.15)
    guardar(fig, "i3_proceso.svg")


if __name__ == "__main__":
    i1_ramas(); i2_circumplejo(); i3_proceso()
