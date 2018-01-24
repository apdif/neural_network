# -*- encoding: utf-8 -*-
from deep_learning.keywords import lib_error
import time, conn, langdetect
from ast import literal_eval
from multiprocessing import Process, Lock   

def identify(html): 
    if html.find('<title>') >= 0:
        starthtml = html.find('<title>')
        endhtml = html.find('</title>',starthtml+1)
        text = html[starthtml+len('<title>'):endhtml] 
          
        txttodb = (u'%s' % text).encode('utf-8')
        detectlang = langdetect.detect(literal_eval(u'%s' % repr(text.decode('utf-8')))) 
        possiblelangs = langdetect.detect_langs(literal_eval(u'%s' % repr(text.decode('utf-8'))))
             
        print text
        print txttodb
        print detectlang
        print possiblelangs
        print "---------------"


def get_keyword(j,p):
    list_keyword = ''
    keywods = ['mp3','descargar','download','music','convert','free','gratis']  
    identify(p)    
    

def find_all_keywords(i,p):  
    p, status = lib_error.request_html(i,p)
    if status is True:
        if p is not None:
            get_keyword(i,p)
    return False

def nblockInterval(n,min,max):
    while min <= max:
        protocol = ["http://","https://"]
        for p in protocol:            
            website = conn.selectSeedweb(min)
            if website:
                print "process -> " + str(n) + " | id ->" + str(min) + " | " + str(max) + " | " + p + website  + " | " + time.strftime("%c")
                status = find_all_keywords(min, p + website)
                if status is not False:
                    break
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