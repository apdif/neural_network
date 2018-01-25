# -*- coding: UTF-8 -*-
import httplib,urllib2, time, os, sys, conn
import socket,ssl

def delete_words(title):
    title = title.replace('\'','').replace('|','').replace('"','')
    while title.find('  ') >= 0:
        title = title.replace('  ',' ')
    return title

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
        var_error = "Error " + str(e.reason)
        conn.updateerr(i, delete_words(str(e.reason)))
    except socket.timeout:
        var_error = "Error timeout"
        conn.updateerr(i,"Error: Error TimeOut")
    except socket.error:
        var_error = "Error Socket"
        conn.updateerr(i,"Error: Error Socket")
    except ssl.SSLError:
        var_error = "Error SSLError"
        conn.updateerr(i,"Error: Error SSL")
    except ssl.CertificateError:
        var_error = "Error CertificateError"
        conn.updateerr(i,"Error: Error SSl")
    except httplib.BadStatusLine:
        var_error = "Error httplib BadStatusLine"
        conn.updateerr(i,"Error httplib BadStatusLine")
    except httplib.IncompleteRead:
        var_error = "Error httplib BadStatusLine"
        conn.updateerr(i,"Error httplib IncompleteRead")
    except:
        print sys.exc_info()[0]
        conn.updateerr(i,"Break")
        os.abort()
    return var_error, False