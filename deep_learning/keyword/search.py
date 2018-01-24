# -*- encoding: utf-8 -*-
import time, conn
from multiprocessing import Process, Lock  

def nblockInterval(n,min,max):
    while min <= max:
        protocol = ["http://","https://"]
        for p in protocol:            
            website = conn.selectSeedweb(min)
            if website:
                print "process -> " + str(n) + " | id ->" + str(min) + " | " + str(max) + " | " + p + website  + " | " + time.strftime("%c")
        min+=1   

def f(l,n,min,max):
    l.acquire()
    try:
        nblockInterval(n,min,max)        
    finally:
        l.release()

def nblock():
    n = 1
    process = 10
    block = int(conn.verifyProcess()) / process
    while n <= process:
        lock = Lock()
        Process(target=f, args=(lock,n,block * ( n - 1 ) + 1,block * n)).start()
        n+=1