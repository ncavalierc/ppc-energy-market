
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Manager

key = 666

def user(lst):
    print("PID fils home: " + str(os.getpid()))
    '''
    choix = 0
    answer = 0
    print("Que voulez-vous faire ?")
    print("1. Vendre")
    print("2. Acheter")
    choix = 2
    if choix == 1:
        print("toto")
    elif choix == 2:
        while answer not in range(1, 100):
            print("Combien d'énergie voulez vous")
            answer = 5
        return answer
    '''
    energie = 0
    wallet = 100
    
    demande = 5

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


try:
    mq = sysv_ipc.MessageQueue(key)
except:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)


if __name__ == "__main__":
    while True:
        with Manager() as manager:
            lst = manager.list()

            child = Process(target=user, args=(lst,))
            child.start()

            print("PID parent home: " + str(os.getpid())) 

            child.join()
        print("fini")
