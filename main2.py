import tkinter as tk
import cmath

W, H, N = 500, 500, 250
PALETTE = [
    (12, 44, 138), (24, 82, 177), (57, 125, 209), (134, 181, 229),
    (211, 236, 248), (241, 233, 191), (248, 201, 95), (255, 170, 0),
    (204, 128, 0), (153, 87, 0),
]

root = tk.Tk()
root.title("Фракталы")

canvas = tk.Canvas(root, width=W, height=H, bg="black")
canvas.pack(side=tk.RIGHT, padx=20, pady=20)

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)

mode = tk.StringVar(value="Мандельброт")
formula = tk.StringVar(value="z^2 + c")


def make_entry(row, label, value, pady=0):
    tk.Label(frame, text=label).grid(row=row, column=0, sticky="e", pady=pady)
    e = tk.Entry(frame, width=12)
    e.insert(0, value)
    e.grid(row=row, column=1, sticky="w", pady=pady)
    return e


def update_labels(*_):
    mandel = mode.get() == "Мандельброт"
    const_label.config(text="z0 (константа):" if mandel else "c (константа):")
    range_label.config(text="Диапазон c (Re / Im):" if mandel
                       else "Диапазон z0 (Re / Im):")


tk.Label(frame, text="Режим:").grid(row=0, column=0, columnspan=2, sticky="w")
for i, m in enumerate(("Мандельброт", "Жюлиа")):
    tk.Radiobutton(frame, text=m, variable=mode, value=m,
                   command=update_labels).grid(row=1, column=i, sticky="w")


tk.Label(frame, text="Формула:").grid(row=2, column=0, sticky="w", pady=(8, 0))
tk.OptionMenu(frame, formula, "z^2 + c", "z^3 + c", "z^1.5 + c").grid(
    row=2, column=1, sticky="w", pady=(8, 0))


const_label = tk.Label(frame, text="z0 (константа):")
const_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
const_re = make_entry(4, "Re:", "0")
const_im = make_entry(5, "Im:", "0")

range_label = tk.Label(frame, text="Диапазон c (Re / Im):")
range_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))
re_min = make_entry(7, "Re min:", "-2.0")
re_max = make_entry(8, "Re max:", "1.0")
im_min = make_entry(9, "Im min:", "-1.5")
im_max = make_entry(10, "Im max:", "1.5")


iter_entry = make_entry(11, "Макс. итераций:", "100", pady=(8, 0))


def f(z, c, formula):
    if formula == "z^2 + c":
        return z * z + c
    if formula == "z^3 + c":
        return z * z * z + c
    return cmath.exp(1.5 * cmath.log(z)) + c if z else c


def escape_color(i, max_iter):
    if i >= max_iter:
        return (0, 0, 0)
    idx = (i / max_iter) ** 0.5 * (len(PALETTE) - 1)
    lo = int(idx)
    hi = min(lo + 1, len(PALETTE) - 1)
    frac = idx - lo
    p, q = PALETTE[lo], PALETTE[hi]
    return tuple(int(p[k] + (q[k] - p[k]) * frac) for k in range(3))


def start_draw():
    try:
        const = complex(float(const_re.get()), float(const_im.get()))
        rmin, rmax = float(re_min.get()), float(re_max.get())
        imin, imax = float(im_min.get()), float(im_max.get())
        max_iter = max(1, int(iter_entry.get()))
    except ValueError:
        return

    mandel = mode.get() == "Мандельброт"
    formula = formula.get()

    img = tk.PhotoImage(width=N, height=N)
    for py in range(N):
        im = imin + (imax - imin) * py / N
        row = []
        for px in range(N):
            re = rmin + (rmax - rmin) * px / N
            z, c = (const, complex(re, im)) if mandel else (complex(re, im), const)
            i = 0
            while i < max_iter and abs(z) <= 2.0:
                z = f(z, c, formula)
                i += 1
            row.append("#%02x%02x%02x" % escape_color(i, max_iter))
        img.put("{" + " ".join(row) + "}", to=(0, py))

    img = img.zoom(2)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=img)
    canvas.image = img


tk.Button(frame, text="Нарисовать", command=start_draw,
          bg="gray", fg="white").grid(row=12, column=0, columnspan=2, pady=15)

update_labels()
root.mainloop()