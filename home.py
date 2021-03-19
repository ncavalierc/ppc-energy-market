
import os
import sys
import time
import sysv_ipc

key = 706


def user():
    answer = 0
    while answer not in range(1, 100):
        print("CB d'energie voulez vous")
        answer = int(input())
    return answer


try:
    mq = sysv_ipc.MessageQueue(key)
except:
    print("Cannot connect to message queue", key, ", terminating.")
    sys.exit(1)


t = user()


pid = t
m = str(t).encode()
mq.send(m)
pid += 3
m, pid = mq.receive(type=pid)
dt = m.decode()
print("Server response:", dt)
