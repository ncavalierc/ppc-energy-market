import sys
import time
import sysv_ipc
import threading
import concurrent.futures
import signal
import os
import signal
import random
from multiprocessing import Process

# délcarations des variables
key = 666
maBarrier = threading.Barrier(5)
energie = 10000
prix = 50
jour = 0
jour_J = 1


def worker(mq, m):

    global energie
    global prix
    global jour
    global jour_J

    print("Starting thread:", threading.current_thread().name)
    # réception de la message queue
    data = m.decode()
    data = data.split(",")
    demande = int(data[0])
    money = int(data[1])
    etat = int(data[2])

    if money > prix * demande:
        t = demande + 3
        message = demande
    else:
        message = demande / prix

    message = str(message)
    prix_encoded = str(prix)
    data = str(message) + "," + str(prix_encoded)
    mq.send(data.encode(), type=t)

    # Gestion d'achat/vente coté marché
    if etat == 0:
        print("La maison achète :", abs(demande), " d'énergies")
        jour_J += demande
    if etat == 1:
        print("La maison vend :", abs(demande), " d'énergies")
        jour_J -= demande

    maBarrier.wait()

    # Calcul des transactions d'énérgies pour calculer le nouveau prix
    if maBarrier.wait() == 0:
        print("transaction dans une journée : ", jour_J)

        prix += int(0.1 * jour_J)
        jour_J = 0
        jour += 1
        print("---------------------------------------------------------------------")
        print("Jour : ", jour, "Prix : ", prix)
        print("---------------------------------------------------------------------")


# réception d'un signal -> gestion évenement favorable et défavorable pour le marché


def handler(sig, frame):
    global jour_J
    global prix
    if sig == signal.SIGUSR1:
        prix = prix * 2
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(
            "Tension politique le prix de l'energie double ")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    if sig == signal.SIGUSR2:
        prix = int(prix / 2)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(
            "Journée international de l'energie une unité achetée une unité offerte ")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# génération aléatoire des signaux externes


def external():
    # temps d'attente pour le débuts des signaux
    time.sleep(5)

    while True:
        random_time = int(10*random.random())
        time.sleep(1)
        if random_time > 8:
            os.kill(os.getppid(), signal.SIGUSR1)
        if random_time < 2:
            os.kill(os.getppid(), signal.SIGUSR2)


if __name__ == "__main__":
    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    # définition des signaux
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)

    # Création du processus fils pour les événements externes
    childProcess = Process(target=external, args=())
    childProcess.start()

    global childPID
    childPID = childProcess.pid

    print("Débuts des transactions")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            try:
                m, t = mq.receive(type=1)
                executor.submit(worker, mq, m)
            except sysv_ipc.Error:
                print("Signal et MQ en même temps")

    print("Fin des transactions")
