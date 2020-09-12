import time
from multiprocessing import Process


def dynamic():
    h = 0.1
    Fin = 2.5
    yk_1 = 0
    yk = 0
    steps = 0
    tn_1 = float("{:.1f}".format(time.time()))
    while 1:
        tn = float("{:.1f}".format(time.time()))
        steps = (tn - tn_1)//h  # erro aqui
        print(steps)
        tn_1 = tn_1 + steps*h  # erro aqui
        if steps > 0:
            while(steps > 0):
                yk = 0.004*Fin + 0.96*yk_1
                if yk < 0:
                    yk = 0
                if yk > 0.5:
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        print(yk)
