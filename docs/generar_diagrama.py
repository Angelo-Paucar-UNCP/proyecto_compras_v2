from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def caja(ax, x, y, w, h, texto, color):
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=color, edgecolor="#1f2937", linewidth=1.2,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=8.5, wrap=True)


def flecha(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#1f2937", lw=1.2))


def main():
    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis("off")
    ax.set_title("Flujo del chatbot — Grupo 5 (compra en línea)", fontsize=14, pad=12)

    caja(ax, 3.2, 14.6, 3.6, 0.9, "Saludo e instrucción\n(escribe 'ayuda' para humano)", "#dbeafe")
    flecha(ax, 5, 14.6, 5, 14.2)
    caja(ax, 3.2, 13.2, 3.6, 0.9, "Pregunta slots:\nvisitante, páginas, minutos,\nfin de semana, mes", "#dbeafe")

    flecha(ax, 3.2, 13.6, 1.6, 12.6)
    caja(ax, 0.3, 11.5, 2.6, 1.1, "Alternativo\nUsuario dice ayuda/\nsalir/asesor", "#fde68a")
    flecha(ax, 1.6, 11.5, 1.6, 2.4)

    flecha(ax, 6.8, 13.6, 8.4, 12.6)
    caja(ax, 7.1, 11.5, 2.6, 1.1, "Error de slot\nDato inválido\n(hasta 3 intentos)", "#fecaca")
    flecha(ax, 8.4, 11.5, 8.4, 10.6)
    caja(ax, 7.1, 9.5, 2.6, 1.0, "3 fallos → derivar\na humano", "#fecaca")
    flecha(ax, 8.4, 9.5, 8.4, 2.4)

    flecha(ax, 5, 13.2, 5, 12.2)
    caja(ax, 3.2, 11.2, 3.6, 0.9, "Completa defaults de train\ny llama POST /predecir", "#dbeafe")
    flecha(ax, 5, 11.2, 5, 10.6)
    caja(ax, 3.2, 9.6, 3.6, 0.9, "¿API respondió 200?", "#e5e7eb")

    flecha(ax, 3.2, 10.0, 1.6, 8.6)
    caja(ax, 0.3, 7.5, 2.6, 1.1, "Error técnico\nAPI apagada o 400/500", "#fecaca")
    flecha(ax, 1.6, 7.5, 1.6, 2.4)

    flecha(ax, 5, 9.6, 5, 8.8)
    caja(ax, 3.2, 7.8, 3.6, 0.9, "¿Predicción = 0\n(abandono)?", "#e5e7eb")
    flecha(ax, 3.2, 8.2, 1.6, 6.8)
    caja(ax, 0.2, 5.7, 2.8, 1.1, "Camino feliz (abandono)\nOfrece cupón 15%\ny deriva a asesor", "#bbf7d0")
    flecha(ax, 1.6, 5.7, 1.6, 2.4)

    flecha(ax, 6.8, 8.2, 8.4, 6.8)
    caja(ax, 7.0, 5.7, 2.8, 1.1, "Camino feliz (compra)\nInvita a ir a caja", "#bbf7d0")

    caja(ax, 3.2, 1.3, 3.6, 1.0, "Derivación a persona\nde soporte", "#fde68a")
    ax.text(5, 0.5, "Verde: feliz · Amarillo: alternativo · Rojo: error", ha="center", fontsize=9)

    out = Path(__file__).resolve().parent / "flujo_chatbot.png"
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
    print(f"Guardado {out}")


if __name__ == "__main__":
    main()
