import matplotlib.pyplot as plt
import matplotlib.image as mpimg

X_MAX = 1143
Y_MAX = 1181

img = mpimg.imread("field.png")

fig, ax = plt.subplots()
ax.imshow(img, extent=[0, X_MAX, 0, Y_MAX], origin="lower")

ax.set_xlim(0, X_MAX)
ax.set_ylim(0, Y_MAX)
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Line artists: to left wall (x=0), right wall (x=X_MAX), bottom wall (y=0), top wall (y=Y_MAX)
line_left,   = ax.plot([], [], 'r--', linewidth=1)
line_right,  = ax.plot([], [], 'g--', linewidth=1)
line_bottom, = ax.plot([], [], 'b--', linewidth=1)
line_top,    = ax.plot([], [], 'y--', linewidth=1)

# Text labels for each distance, placed at the midpoint of each line
text_left   = ax.text(0, 0, '', color='red',    fontsize=8, ha='center', va='center', backgroundcolor='white')
text_right  = ax.text(0, 0, '', color='green',  fontsize=8, ha='center', va='center', backgroundcolor='white')
text_bottom = ax.text(0, 0, '', color='blue',   fontsize=8, ha='center', va='center', backgroundcolor='white')
text_top    = ax.text(0, 0, '', color='orange', fontsize=8, ha='center', va='center', backgroundcolor='white')

# Cursor position marker
cursor_dot, = ax.plot([], [], 'ko', markersize=4)

# Small text box in a corner showing all 4 distances together
info_text = ax.text(
    0.02, 0.98, '', transform=ax.transAxes,
    fontsize=9, va='top', ha='left',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)


def on_move(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return

    x, y = event.xdata, event.ydata

    dist_left = x            # distance to x = 0
    dist_right = X_MAX - x   # distance to x = X_MAX
    dist_bottom = y          # distance to y = 0
    dist_top = Y_MAX - y     # distance to y = Y_MAX

    # Update lines: cursor -> each wall
    line_left.set_data([x, 0], [y, y])
    line_right.set_data([x, X_MAX], [y, y])
    line_bottom.set_data([x, x], [y, 0])
    line_top.set_data([x, x], [y, Y_MAX])

    # Update midpoint labels
    text_left.set_position((x / 2, y))
    text_left.set_text(f"{dist_left:.1f}")

    text_right.set_position(((x + X_MAX) / 2, y))
    text_right.set_text(f"{dist_right:.1f}")

    text_bottom.set_position((x, y / 2))
    text_bottom.set_text(f"{dist_bottom:.1f}")

    text_top.set_position((x, (y + Y_MAX) / 2))
    text_top.set_text(f"{dist_top:.1f}")

    cursor_dot.set_data([x], [y])

    info_text.set_text(
        f"Cursor: ({x:.1f}, {y:.1f})\n"
        f"Left (x=0):   {dist_left:.1f}\n"
        f"Right (x={X_MAX}): {dist_right:.1f}\n"
        f"Bottom (y=0): {dist_bottom:.1f}\n"
        f"Top (y={Y_MAX}):  {dist_top:.1f}"
    )

    fig.canvas.draw_idle()


fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.show()