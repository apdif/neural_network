# -*- coding: UTF-8 -*-
from deep_learning.keywords import lib_error
import time, conn, langdetect, re, sys
from ast import literal_eval
from multiprocessing import Process, Lock   

from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
 
def delete_chr(text):
    chr_esp = ['*','\n','\t','.',',','\'','_','\"',"-",'  ']
    for n in chr_esp:
        while text.find(n) >= 0:
            text = text.replace(n,' ')
    return text

def index_words(code_html):
    lemmatizer = WordNetLemmatizer()
    soup = BeautifulSoup(code_html.replace('>','>*'),"html5lib")
    text = delete_chr(soup.get_text(strip=True))     
    tokens = [t for t in text.split()] 
    patron = re.compile(r"^([a-zA-Z]+)$")   #[a-zA-Z] OR \w
    new_tokens = []
    delete_tokens = []
    for i in tokens:
        if patron.search(i):
            new_tokens.append(lemmatizer.lemmatize(i, pos="v"))
        else:
            delete_tokens.append(i)
    clean_tokens = new_tokens[:]    
    for token in new_tokens:
        if token in stopwords.words():
            clean_tokens.remove(token)         
    freq = nltk.FreqDist(clean_tokens)
    return freq

def find_contents(text,str):
    search_keywords = re.compile('name.*.'+ str +'.*.content.*\"(?P<contents>.*)"')
    if search_keywords.search(text):
        get_keywords = search_keywords.search(text)
        return get_keywords.group('contents')
    return False

def get_keyword(j,p):
    print identify(p)  
    text_meta = ""
    meta = p
    while meta.find("<meta") > 0:
        start_meta_title = meta.find("<meta")
        end_meta_title = meta.find(">", start_meta_title)
        text_find = meta[start_meta_title:end_meta_title + 1]
        str_find = ["keywords","description","title"]
        for xyz in str_find:
            if find_contents(text_find,xyz):
                text_meta = find_contents(text_find,xyz) + " " + text_meta
        meta = meta[end_meta_title:]
    if index_words(text_meta):
        freq = index_words(text_meta)
    else:
        start = p.find("<body")
        end = p.find('/body>',start)
        freq = index_words(p[start:end + 6])
        
    print freq.most_common(10)
    print len(freq)
    #freq.plot(20,cumulative=False) 
    keywods = ['mp3','descargar','download','music','convert','free','gratis']
    print "-----------------------------"

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