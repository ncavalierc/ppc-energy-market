
import sys
import time
import sysv_ipc
import threading
import concurrent.futures

key = 666
# ipcrm -Q 666
# pour kill la message queue
energie = 10000
prix = 2

def worker(mq, m):
    global energie
    print("Starting thread:", threading.current_thread().name)
    data = m.decode()
    data = data.split(",")
    print(data)
    demande = int(data[0])
    money = int(data[1])
    print("Requete de : " + str(demande))
    if money > prix * demande:
        t = demande + 3
        message = demande
    else:
        message = demande / prix
    
    
    message = str(message)
    prix_encoded = str(prix)
    data = str(message) + "," + str(prix_encoded)
    mq.send(data.encode(), type=t)
    print("Ending thread:", threading.current_thread().name)


if __name__ == "__main__":
    print("Starting thread:", threading.current_thread().name)

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    print("Starting energy market.")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
        while True:
            m, t = mq.receive()
            executor.submit(worker, mq, m)

    print("Terminating energy market.")
    print("Ending thread:", threading.current_thread().name)
