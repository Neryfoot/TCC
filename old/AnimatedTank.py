import time
from multiprocessing import Process, Value
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

plt.ion()

h = 0.1  # passo da solução numérica
Fin = Value('f', 2.5)  # fluxo de entrada
yk_1 = 0  # condição inicial
yk_sync = Value('f', 0)  # condição inicial


def Fin_update(val):
    Fin.value = val*5/100


def fig_loop(p):
    while True:
        p.set_ydata(yk_sync.value*1000/5)
        plt.pause(0.1)


def interface():
    plt.ion()
    x = list(range(0, 11))
    y = [10]*11

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.25)
    p, = plt.plot(x, y, linewidth=2, color='blue')
    plt.axis([0, 10, 0, 100])

    axSlider2 = plt.axes([0.1, 0.1, 0.8, 0.05])
    slider2 = Slider(
        ax=axSlider2, label='Slider2',
        valmin=0, valmax=100,
        valfmt='%1.2f', valstep=1,
        closedmax=True, color='green')
    slider2.on_changed(Fin_update)
    fig_loop(p)


def dynamic():
    global yk_1
    global h
    yk = yk_sync.value
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while 1:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        # print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*Fin.value + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        yk_sync.value = yk


dynamic_process = Process(target=dynamic)
dynamic_process.start()
interface_process = Process(target=interface)
interface_process.start()
