
import sys
import time
import sysv_ipc
import threading

key = 706
# ipcrm -Q 666
# pour kill la message queue
energie = 12


def worker(mq, m):
    print("Starting thread:", threading.current_thread().name)
    pid = int(m.decode())
    t = pid + 3
    if pid > energie:
        message = energie
    if pid <= energie:
        message = m
    message = str(message).encode()
    #pid = int(m.decode())
    #t = pid + 3
    mq.send(message, type=t)
    print(t)
    print("Ending thread:", threading.current_thread().name)


if __name__ == "__main__":
    print("Starting thread:", threading.current_thread().name)

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    print("Starting energy market.")

    threads = []
    while True:
        m, t = mq.receive()

        p = threading.Thread(target=worker, args=(mq, m))
        p.start()
        threads.append(p)
        break

    print("Terminating energy market.")
    print("Ending thread:", threading.current_thread().name)
