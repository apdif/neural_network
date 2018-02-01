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
 
def delete_chr(text,str):
    while text.find(str) >= 0:
        text = text.replace(str,' ')
    return text


def get_keyword(j,p):
    lemmatizer = WordNetLemmatizer()
    #Identify lenguage
    print identify(p) 
    #extract only the content between the tag <body> and </body>   
    start = p.find("<body")
    end = p.find('/body>',start)
    #delete all the tag of html
    soup = BeautifulSoup(p[start:end + 6].replace('>','>*'),"html5lib")
    text = soup.get_text(strip=True)
    #find and delete the special characters
    chr_esp = ['*','\n','\t','.',',','\'','_','\"',"-",'  ']
    for n in chr_esp:
        text = delete_chr(text,n)
    #split the text
    tokens = [t for t in text.split()] 
    #delete words with special characters
    patron = re.compile(r"^([a-zA-Z]+)$")   #[a-zA-Z] OR \w
    new_tokens = []
    delete_tokens = []
    for i in tokens:
        if patron.search(i):
            new_tokens.append(lemmatizer.lemmatize(i, pos="v"))
        else:
            delete_tokens.append(i)
    #clean 
    clean_tokens = new_tokens[:]    
    for token in new_tokens:
        if token in stopwords.words():
            clean_tokens.remove(token) 
    #create the frequence        
    freq = nltk.FreqDist(clean_tokens)
    print freq.most_common(len(freq))
    print "-------------------------------------------------------------------"
    time.sleep(1)
    #create a graph
    #freq.plot(20,cumulative=False) 
    #Search keywords
    #keywods = ['mp3','descargar','download','music','convert','free','gratis']

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