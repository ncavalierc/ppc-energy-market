
import sys
import time
import sysv_ipc
import threading
import concurrent.futures

# ipcrm -Q 666
# pour kill la message queue
key = 666
energie = 10000
prix = 50
prix_1 = 50
jour = 0
maBarrier = threading.Barrier(5)
jour_0 = 10
jour_J = 0

def worker(mq, m):
    global energie
    global jour
    global jour_0
    global jour_J
    global prix
    global prix_1
    print("Starting thread:", threading.current_thread().name)
    data = m.decode()
    data = data.split(",")
    demande = int(data[0])
    money = int(data[1])
    etat = int(data[2])
    print("Requete du home : " + str(demande))
    if money > prix * demande:
        t = demande + 3
        print("-------market------", t)
        message = demande
    else:
        message = demande / prix
    
    message = str(message)
    prix_encoded = str(prix)
    data = str(message) + "," + str(prix_encoded)
    mq.send(data.encode(), type=t)

    if etat == 0:
        jour_J += demande
    if etat == 1:
        jour_J -= demande

    maBarrier.wait()
    
    print("Ending thread:", threading.current_thread().name)

    if maBarrier.wait() == 0:
        print("Quantité de demande : ", jour_J)
        '''if jour_J == 0:
            jour_J = 1
        if jour_0 == 0:
            jour_0 = 1'
            '''

        print("jour J", jour_J)
        print("Prix : ", prix)
        prix += int(0.1 * jour_J)
        print("Prix : ", prix)
        
        
        '''if jour_J > jour_0:
            rapport = (jour_J / jour_0) / 50
            tmp = prix
            prix = int(prix_1 + prix_1 * abs(rapport))
            prix_1 = tmp
        elif jour_J < jour_0:
            rapport = (jour_0 / jour_J) / 50
            tmp = prix
            prix = int(prix_1 - prix_1 * abs(rapport))
            prix_1 = tmp'''
        

        jour_0 = jour_J
        jour_J = 0
        jour += 1
        print("Jour : ", jour)
    
    
if __name__ == "__main__":
    print("Starting thread parent:", threading.current_thread().name)

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    print("Starting energy market.")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        while True:
            m, t = mq.receive(type=1)
            executor.submit(worker, mq, m)

    print("Terminating energy market.")
    print("Ending thread parent :", threading.current_thread().name)
