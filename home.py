
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Manager

key = 666
energie = 0

def user(lst):
    print("PID fils home: " + str(os.getpid()))
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

                t = user(lst)
                print(lst)
                pid = t
                m = str(t).encode()
                mq.send(m)
                pid += 3
                m, pid = mq.receive(type=pid)
                dt = m.decode()
                print("Energie reçue :", dt)

                child.join()
