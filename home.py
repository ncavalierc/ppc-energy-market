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

    energie = 50
    wallet = 100000
    
    while True:

        print("energie", energie)
        if energie > 75:
            print("PID fils home vente: " + str(os.getpid()))
            print("Vente")
            demande = int(energie / 3)
            m = demande
            w = wallet
            data = str(m)+ "," + str(w) + "," + str(1)
            mq.send(str(data).encode(), type=1)
            demande += 3
            m, demande = mq.receive(type=demande)
            recu = m.decode()
            recu = recu.split(",")
            quantite_recue = int(recu[0])
            prix = int(recu[1])
            wallet += (demande-3) * prix
            energie -= demande - 3
            print("Energie reçue : ", quantite_recue, "Prix unitaire : ", prix)
            maBarrier.wait()

        else:
            print("PID fils home achat: " + str(os.getpid()))
            print("Achat")
            demande = int(10*random.random()) * int(lst.value) + 1
            m = demande
            w = wallet
            data = str(m)+ "," + str(w) + "," + str(0)
            mq.send(str(data).encode(), type=1)
            demande += 3
            m, demande = mq.receive(type=demande)
            recu = m.decode()
            recu = recu.split(",")
            quantite_recue = int(recu[0])
            prix = int(recu[1])
            wallet -= quantite_recue * prix
            energie += quantite_recue
            print("Energie reçue : ", quantite_recue, "Prix unitaire : ", prix)
            maBarrier.wait()


        time.sleep(1)


def weather(lst, lock):
    while True:
        temperature = random.gauss(14,5)
        coef = 0
        if temperature < 10:
            coef = 2
        elif temperature < 20:
            coef = 1
        elif temperature >= 20:
            coef = 0.5

        print("coeff température", coef)

        with lst.get_lock():
                    lst.value = int(coef)
        
        time.sleep(1)
        

try:
    mq = sysv_ipc.MessageQueue(key)
except:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)


if __name__ == "__main__":
    with Manager() as manager:
        
        lst = multiprocessing.Value('i', 1)
        lock = multiprocessing.Lock()

        weather = Process(target=weather, args=(lst, lock))
        weather.start()

        for i in range(5):
            child = Process(target=home, args=(lst,))
            child.start()

        print("PID parent home: " + str(os.getpid())) 
        
        child.join()
