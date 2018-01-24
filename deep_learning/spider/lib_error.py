import httplib,urllib2, time, os, sys, conn
import socket,ssl

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
    except httplib.BadStatusLine:
        print "Error httplib BadStatusLine"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error httplib BadStatusLine"))
    except httplib.IncompleteRead:
        print "Error httplib BadStatusLine"
        conn.updateerr(i,str("Referrer: " + url + ";\nError: Error httplib IncompleteRead"))
    except:
        print sys.exc_info()[0]
        os.abort()
    return "Error", False