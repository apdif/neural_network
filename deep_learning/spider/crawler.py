# -*- encoding: utf-8 -*-
import urllib2, urlparse, time, os, sys, conn, re
import socket,ssl
from multiprocessing import Process, Lock   

def request_html(i,url): 
    time.sleep(1) 
    try:    
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')]
        html = opener.open(url  ,timeout = 6).read() 
        opener.close()  
        conn.updateverify(i)
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
    except:
        print "Error: " + sys.exc_info()[0]
        conn.updateerr(i,str("Referrer: " + url + ";\nError: " + sys.exc_info()[0]))
        os.abort()
    return "Error", False
        
def get_url(url):
    url = url.replace("www.","").replace("http://","").replace("https://","")     
    conn.addSeedweb(url) 
    return url
        
def get_next_link(p, tags):
    start_link = p.find(tags)
    start_quote = p.find('"',start_link)
    end_quote = p.find('"',start_quote + 1)
    url = p[start_quote + 1: end_quote]
    if urlparse.urljoin(url, '/')[:-1].lower().find(" ") < 0:
        return urlparse.urljoin(url, '/')[:-1],end_quote
    return "",end_quote

def find_all_links(i,p):  
    urls = []
    p, status = request_html(i,p)
    if status is True:
        if p is not None:
            links_extract = ["href=", "src="]
            for tags in links_extract:
                while p.find(tags) > 0:
                    url, end_quote = get_next_link(p, tags)
                    if url not in urls:
                        if 'http' in url:
                            urls.append(url)
                            get_url(urlparse.urljoin(url, '/')[:-1])
                    if len(p) == len(p[end_quote:]):
                        break
                    p = p[end_quote:]                
        return urls
    return False

def nblockInterval(n,min,max):
    while min <= max:
        protocol = ["http://","https://"]
        for p in protocol:            
            website = conn.selectSeedweb(min)
            if website:
                print "process -> " + str(n) + " | id ->" + str(min) + " | " + str(max) + " | " + p + website  + " | " + time.strftime("%c")
                urls = find_all_links(min, p + website)
                if urls is not False:  
                    print urls
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