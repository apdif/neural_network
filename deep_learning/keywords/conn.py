# -*- coding: UTF-8 -*-
import _mysql

def conection(enquery):
    db = _mysql.connect(host="localhost",user="root",passwd="",db="system_crawler")
    db.query(enquery)
    r = db.store_result()
    if enquery.upper().startswith('SELECT'): 
        datas = r.fetch_row(0)
        db.commit()
        return datas
    else: 
        datas = None 

def verifyProcess():  
    query = "SELECT COUNT(*) FROM seedweb"
    return conection(query)[0][0]

def selectSeedweb(i):  
    query = "SELECT domain FROM seedweb WHERE id = %s " % (i) #AND verify = 2
    results = conection(query)
    if len(results) > 0:
        return results[0][0]
    return False

def updateerr(i,e):   
    query = "UPDATE seedweb SET verify = 3, error_txt = '%s', modified_date = now() WHERE id = %s " % (e,i)
    conection(query)
        