# -*- coding: UTF-8 -*-
import lib_error
import urlparse, time, conn
from multiprocessing import Process, Lock   
       
def get_url(url):
    url = url.replace("www.","").replace("http://","").replace("https://","")     
    conn.addSeedweb(url) 
    return url
        
def get_next_link(p, tags):
    start_link = p.find(tags)
    start_quote = p.find('"',start_link)
    end_quote = p.find('"',start_quote + 1)
    url = p[start_quote + 1: end_quote].replace('\\','')
    if urlparse.urljoin(url, '/')[:-1].lower().find(" ") < 0:
        return urlparse.urljoin(url, '/')[:-1],end_quote
    return "",end_quote

def find_all_links(i,p,n,m):  
    urls = []
    website = p
    p, status = lib_error.request_html(i,p)
    if status is True:
        print "process -> " + str(n) + " | id ->" + str(i) + " | " + str(m) + " | " + website + " | " + time.strftime("%c") + " | Correct"
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
    print "process -> " + str(n) + " | id ->" + str(i) + " | " + str(m) + " | " + website + " | " + time.strftime("%c") + " | " + p
    return False

def nblockInterval(n,min,max):
    while min <= max:
        protocol = ["http://","https://"]
        for p in protocol:            
            website = conn.selectSeedweb(min)
            if website:
                status = find_all_links(min, p + website, n, max)
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
