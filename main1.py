import tkinter as tk
import math

root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack(side=tk.RIGHT, padx=20, pady=20)

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)


DEPTH_LIMITS = {
    "Серпинский": (1, 8),
    "Снежинка Коха": (1, 7),
    "Дерево": (1, 12),
}

_updating = False
_redraw_job = None


def serpinski(depth, p1, p2, p3):
    if depth == 0:
        canvas.create_polygon(
            p1[0], p1[1], p2[0], p2[1], p3[0], p3[1],
            outline="white", fill=""
        )
    else:
        m1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        m2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        m3 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        serpinski(depth - 1, p1, m1, m3)
        serpinski(depth - 1, m1, p2, m2)
        serpinski(depth - 1, m3, m2, p3)


def koh(depth, p1, p2):
    if depth == 0:
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="cyan")
    else:
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        pa = (p1[0] + dx / 3, p1[1] + dy / 3)
        pb = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)

        cos60, sin60 = 0.5, math.sin(math.pi / 3)
        vx, vy = pb[0] - pa[0], pb[1] - pa[1]
        ppeak = (
            pa[0] + vx * cos60 - vy * sin60,
            pa[1] + vx * sin60 + vy * cos60,
        )

        koh(depth - 1, p1, pa)
        koh(depth - 1, pa, ppeak)
        koh(depth - 1, ppeak, pb)
        koh(depth - 1, pb, p2)


def tree(depth, x, y, length, angle):
    if depth == 0:
        return
    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)
    canvas.create_line(x, y, x2, y2, fill="lightgreen")
    tree(depth - 1, x2, y2, length * 0.7, angle - 0.5)
    tree(depth - 1, x2, y2, length * 0.7, angle + 0.5)


def start_draw():
    global _redraw_job
    _redraw_job = None

    canvas.delete("all")
    f_type = choice.get()
    depth = int(slider.get())

    if f_type == "Серпинский":
        serpinski(depth, (250, 50), (50, 450), (450, 450))
    elif f_type == "Снежинка Коха":
        p1 = (150, 350)
        p2 = (350, 350)
        p3 = (250, 350 - 200 * math.sin(math.pi / 3))
        koh(depth, p1, p2)
        koh(depth, p2, p3)
        koh(depth, p3, p1)
    elif f_type == "Дерево":
        tree(depth, 250, 450, 100, -math.pi / 2)


def schedule_redraw(*args):
    global _redraw_job
    if _redraw_job is not None:
        root.after_cancel(_redraw_job)
    _redraw_job = root.after(150, start_draw)


def on_slider_change(value):
    if _updating:
        return
    schedule_redraw()


def on_fractal_change():
    global _updating
    _updating = True

    name = choice.get()
    lo, hi = DEPTH_LIMITS[name]
    slider.config(from_=lo, to=hi)

    val = int(slider.get())
    val = max(lo, min(hi, val))
    slider.set(val)

    _updating = False
    schedule_redraw()


choice = tk.StringVar(value="Серпинский")
for name in ["Серпинский", "Снежинка Коха", "Дерево"]:
    tk.Radiobutton(
        frame, text=name, variable=choice, value=name,
        command=on_fractal_change
    ).pack(anchor="w", pady=2)

tk.Label(frame, text="Глубина рекурсии:").pack(anchor="w", pady=(15, 2))
slider = tk.Scale(
    frame, from_=1, to=8, orient=tk.HORIZONTAL,
    command=on_slider_change
)
slider.set(3)
slider.pack()

on_fractal_change()
root.mainloop()