import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x = list(range(0, 11))
y = [10]*11

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
p, = plt.plot(x, y, linewidth=2, color='blue')
plt.axis([0, 10, 0, 100])


def val_update(val):
    yval = slider2.val
    p.set_ydata(yval)
    ax.collections.clear()
    plt.draw()
    plt.fill_between(x, 0, y)


axSlider2 = plt.axes([0.1, 0.1, 0.8, 0.05])
slider2 = Slider(
        ax=axSlider2,
        label='Slider2',
        valmin=0,
        valmax=100,
        valfmt='%1.2f',
        valstep=1,
        closedmax=True,
        color='green'
        )


cid = slider2.on_changed(val_update)

plt.show()
