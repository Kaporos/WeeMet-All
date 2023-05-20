import matplotlib.pyplot as plt
import numpy as np
import tomllib
import wemeetall

with open("config.toml", "rb") as f:
    data = tomllib.load(f)

# Creating base stuff
step = data["simulation"]["step"]
count = int(150 * (1e-7 / step))
animated = True
offset = int(data["simulation"]["warmup"] // step)
app = wemeetall.WeMeetAll(data)
wanted = app.wanted

# Creating time data
x = np.linspace(0, count * step, count)

y = []
for i in wanted:
    y.append(np.zeros(count))

for i in range(offset):
    app.step(step)

if not animated:
    for i in range(count):
        app.step(step)
        for (j, iy) in enumerate(wanted):
            y[j][i] = iy.output



fig, ax = plt.subplots()
ax.set_ylim([0,10])

ln = []
for (i,iy) in enumerate(y):
    (iln,) = ax.plot(x, iy, animated=animated, label=wanted[i].name())
    ln.append(iln)

def on_close(event):
    plt.close()  # close the figure

fig.canvas.mpl_connect('close_event', on_close)
plt.legend()
plt.show(block=(not animated))

if not animated:
    exit()

plt.pause(0.5)

bg = fig.canvas.copy_from_bbox(fig.bbox)


# Below is the animation part. Don't overthing about it. No one can undertsand it, even me. (ok i didnt try). Thanks copy paste.

for iln in ln:
    ax.draw_artist(iln)

fig.canvas.blit(fig.bbox)
old_fig_size = fig.get_size_inches()
import time
while True:
    plt.pause(0.00001)
    app.step(step)
    if (old_fig_size != fig.get_size_inches()).any():
        bg = fig.canvas.copy_from_bbox(fig.bbox)
        old_fig_size = fig.get_size_inches()
    fig.canvas.restore_region(bg)
    for (i, iy) in enumerate(y):
        iy = np.delete(iy, 0)
        iy = np.append(iy, wanted[i].output)
        ln[i].set_ydata(iy)
        y[i] = iy
    for iln in ln:
        ax.draw_artist(iln)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()
    if not plt.fignum_exists(fig.number):
        break  # exit the loop if the figure is closed

print("End of the program bro !")
