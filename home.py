import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Manager
import multiprocessing
import random
import threading
import concurrent.futures

key = 666
maBarrier = threading.Barrier(1)


def home(lst):
    production_home = int(10*random.random())
    energie = 50
    wallet = 100000

    print("La maison ", str(os.getpid()), "a une capacité de production d'énergie de : ",
          production_home)

    while True:
        energie += production_home
        if energie > 75:
            # création de la demande
            demande = int(energie / 3)
            m = demande
            w = wallet
            data = str(m) + "," + str(w) + "," + str(1)
            mq.send(str(data).encode(), type=1)

            # Reception de la transactions
            demande += 3
            m, demande = mq.receive(type=demande)

            # Gestion de la reception
            recu = m.decode()
            recu = recu.split(",")
            quantite_recue = int(recu[0])
            prix = int(recu[1])
            wallet += (demande-3) * prix
            energie -= demande - 3

            print("La maison ", str(os.getpid()), "a vendu : ",
                  quantite_recue, " d'énergies pour un prix unitaire de : ", prix)
            maBarrier.wait()

        else:
            # création de la demande
            demande = int(10*random.random()) * int(lst.value) + 1
            m = demande
            w = wallet
            data = str(m) + "," + str(w) + "," + str(0)
            mq.send(str(data).encode(), type=1)

            # Reception de la transactions
            demande += 3
            m, demande = mq.receive(type=demande)

            # Gestion de la reception
            recu = m.decode()
            recu = recu.split(",")
            quantite_recue = int(recu[0])
            prix = int(recu[1])
            wallet -= quantite_recue * prix
            energie += quantite_recue

            print("La maison ", str(os.getpid()), "a acheté : ",
                  quantite_recue, " d'énergies pour un prix unitaire de : ", prix)
            maBarrier.wait()

        time.sleep(1)

# Gestion des conditions climatiques qui influence la demande d'énergie


def temperature(lst, lock):
    while True:
        temperature = random.gauss(14, 5)
        coef = 0
        if temperature < 10:
            coef = 2
            print("aujourd'hui il fait : ", temperature,
                  "°C, énormement de consomation")
        elif temperature < 20:
            coef = 1
            print("aujourd'hui il fait : ", temperature,
                  "°C, consomation normale")
        elif temperature >= 20:
            coef = 0.5
            print("aujourd'hui il fait : ", temperature,
                  "°C, très peu de consomation")
        # Chargement du coeficient liée à la température dans la mémoire partagée avec mutex
        with lst.get_lock():
            lst.value = int(coef)

        time.sleep(1)


try:
    mq = sysv_ipc.MessageQueue(key)
except:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)


if __name__ == "__main__":

    # Manager qui gère la mémoire partagé
    with Manager() as manager:
        lst = multiprocessing.Value('i', 1)
        lock = multiprocessing.Lock()

        # Création du processus fils de température
        weather = Process(target=temperature, args=(lst, lock))
        weather.start()

        # Création de cinq maisons
        for i in range(5):
            child = Process(target=home, args=(lst,))
            child.start()

        child.join()
