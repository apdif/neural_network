# -*- coding: UTF-8 -*-
from deep_learning.keywords import lib_error
import time, conn, langdetect, re
from ast import literal_eval
from multiprocessing import Process, Lock   

def identify(html): 
    txttodb = 'Untitled'
    detectlang = 'es'
    possiblelangs = ''
    if html.find('<title>') >= 0:
        starthtml = html.find('<title>')
        endhtml = html.find('</title>',starthtml+1)
        text = html[starthtml+len('<title>'):endhtml] 
        origin = lib_error.delete_words(text)
        print origin
        try:
            txttodb = lib_error.delete_words(u'%s' % repr(text))
            detectlang = langdetect.detect(txttodb)   
            possiblelangs = langdetect.detect_langs(txttodb)   
        except:
            detectlang = 'NA'
            possiblelangs = 'NA'
        return txttodb,detectlang,possiblelangs 
 
def get_keyword(j,p):
    list_keyword = ''
    keywods = ['mp3','descargar','download','music','convert','free','gratis']  
    print identify(p)    
    

def find_all_keywords(i,p,n,m):  
    website = p
    p, status = lib_error.request_html(i,p)
    if status is True:
        print "process -> " + str(n) + " | id ->" + str(i) + " | " + str(m) + " | " + website + " | " + time.strftime("%c") + " | Correct"
        if p is not None:
            get_keyword(i,p)
            return True
    print "process -> " + str(n) + " | id ->" + str(i) + " | " + str(m) + " | " + website + " | " + time.strftime("%c") + " | " + p
    return False

def nblockInterval(n,min,max):
    while min <= max:
        protocol = ["http://","https://"]
        for p in protocol:            
            website = conn.selectSeedweb(min)
            if website:
                status = find_all_keywords(min, p + website, n, max)
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