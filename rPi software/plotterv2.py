import numpy as np
import matplotlib.pyplot as plt

import carParser
carParser.init("/dev/ttyAMA0", 921600)

angles_deg = [90, 0, 270, 180]
angles = np.deg2rad(angles_deg)
labels = ['F', 'R', 'B', 'L']

def smooth_closed_curve(xs, ys, n=300):
    xs = np.append(xs, xs[0])
    ys = np.append(ys, ys[0])
    t = np.arange(len(xs))
    t_fine = np.linspace(0, len(xs) - 1, n)
    return np.interp(t_fine, t, xs), np.interp(t_fine, t, ys)

# --- set up figure ONCE ---
fig, ax = plt.subplots(figsize=(6, 6))
line, = ax.plot([], [], 'b-', linewidth=2, label='Distance envelope')
pts, = ax.plot([], [], 'ro', markersize=8, label='Sensor points')
annotations = [ax.annotate('', (0, 0), textcoords="offset points", xytext=(8, 8)) for _ in range(4)]

s = 0.5
ax.add_patch(plt.Rectangle((-s/2, -s/2), s, s, color='gray', label='Car'))
ax.axhline(0, color='lightgray', linewidth=0.5)
ax.axvline(0, color='lightgray', linewidth=0.5)
ax.set_aspect('equal')
ax.set_xlim(-500, 500)   # adjust to your sensor range
ax.set_ylim(-500, 500)
ax.legend()
ax.set_title("Distance sensor plot")
plt.ion()
plt.show()

while True:
    dists = np.array(carParser.getDIST())
    xs, ys = dists * np.cos(angles), dists * np.sin(angles)
    x_fine, y_fine = smooth_closed_curve(xs, ys)

    line.set_data(x_fine, y_fine)
    pts.set_data(xs, ys)
    for ann, x, y, d, lbl in zip(annotations, xs, ys, dists, labels):
        ann.set_position((x + 8, y + 8))
        ann.xy = (x, y)
        ann.set_text(f'{lbl}: {d:.1f}')

    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    plt.pause(0.001)  # lets the GUI event loop breathe
