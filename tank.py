import time
from multiprocessing import Process


def dynamic():
    h = 0.1  # passo da solução numérica
    Fin = 2.5  # fluxo de entrada
    yk_1 = 0  # condição inicial
    yk = 0  # condição inicial
    steps = 0  # condição inicial
    tn_1 = float("{:.1f}".format(time.time()))  # condição inicial
    while 1:
        tn = float("{:.1f}".format(time.time()))  # tempo atual
        steps = (tn - tn_1)//h  # número de passos
        print(steps)
        tn_1 = tn_1 + steps*h  # atualiza o tempo
        if steps > 0:
            while(steps > 0):  # executa atualização da função
                yk = 0.004*Fin + 0.96*yk_1
                if yk < 0:  # nível não pode baixar de 0
                    yk = 0
                if yk > 0.5:  # nível não passa de 0.5
                    yk = 0.5
                yk_1 = yk
                steps -= 1
        print(yk)
