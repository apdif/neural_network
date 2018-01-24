# -*- encoding: utf-8 -*-
import httplib,urllib2, urlparse, time, os, sys, conn
import socket,ssl
from multiprocessing import Process, Lock   

def request_html(i,url): 
    time.sleep(1) 
    try:    
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')]
        html = opener.open(url  ,timeout = 6).read() 
        opener.close()  
        return html.lower().replace("'","\""), True
    except urllib2.URLError as e:
        print "Error " + str(e.reason)
        conn.updateerr(i, "Referrer: " + url + ";\nError: " + str(e.reason))
    except socket.timeout:
        print "Error timeout"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error TimeOut"))
    except socket.error:
        print "Error Socket"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error Socket"))
    except ssl.SSLError:
        print "Error SSLError"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error SSL"))
    except ssl.CertificateError:
        print "Error CertificateError"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error SSl"))
    except httplib.BadStatusLine:
        print "Error httplib BadStatusLine"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error httplib BadStatusLine"))
    except:
        print sys.exc_info()[0]
        os.abort()
    return "Error", False

def find_all_keywords(i,p):  
    p, status = request_html(i,p)
    if status is True:
        if p is not None:
            print "Code HTML"
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