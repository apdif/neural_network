# -*- encoding: utf-8 -*-
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