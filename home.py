
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Manager
import multiprocessing
import random

key = 666

def user(lst):
    print("PID fils home: " + str(os.getpid()))

    energie = 0
    wallet = 100000
    
    while True:
        demande = int(10*random.random()) * int(lst.value)
        m = demande
        w = wallet
        data = str(m)+ "," + str(w)
        print("1", data)
        mq.send(str(data).encode(), type=1)
        print("2")
        demande += 3
        m, demande = mq.receive(type=demande)
        print("3")
        recu = m.decode()
        recu = recu.split(",")
        print("4", recu)
        quantite_recue = int(recu[0])
        prix = int(recu[1])
        wallet -= quantite_recue * prix
        energie += quantite_recue
        print("Energie reçue : ", quantite_recue, "Prix unitaire : ", prix)
        time.sleep(1)

def temperature(lst, lock):
    temperature = random.gauss(14,6)
    coef = 0
    if temperature < 10:
        coef = 2
    elif temperature < 20:
        coef = 1
    elif temperature >= 20:
        coef = 0.5

    print("coeff", coef)

    with lst.get_lock():
                lst.value = int(coef)


try:
    mq = sysv_ipc.MessageQueue(key)
except:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)


if __name__ == "__main__":
    with Manager() as manager:
        
        lst = multiprocessing.Value('i', 0)
        lock = multiprocessing.Lock()

        weather = Process(target=temperature, args=(lst, lock))
        weather.start()

        for i in range(5):
            child = Process(target=user, args=(lst,))
            child.start()

        print("PID parent home: " + str(os.getpid())) 
            
        print("fini")
        child.join()
