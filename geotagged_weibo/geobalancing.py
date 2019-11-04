#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import string
import re
import psycopg2
import numpy as np



def _retrieve_record():
    '''
    retrieve record from database for checking duplicates
    '''
    conn_string = "host='localhost' dbname='geotag' user='postgres' password='postgres'"
    # print the connection string we will use to connect
    #print "Retrieve records: connecting to database\n    ->%s" % (conn_string)
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    select_sql = "SELECT gid, np FROM grids where nodes is null limit 1000"
    #print select_sql
 
    cursor.execute(select_sql)
 
    # retrieve the records from the database
    records = cursor.fetchall()
 
    return records

def _update_record(node, wid):
    conn_string = "host='localhost' dbname='geotag' user='postgres' password='postgres'"
    # print the connection string we will use to connect
    #print "Update records: connecting to database to update \n	->%s" % (conn_string)
    
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
    
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    
    try:
        sql = "UPDATE grids SET nodes = %s WHERE gid = \'%s\';"%(node, wid)
        #print sql
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    conn.close()




if __name__ == "__main__":

    
    avgposts = 22893
    numposts = 0
    currentnode = 0
    for n in range(10000):
        
        records = _retrieve_record()
        for record in records:
            wid = record[0]
            np = record[1]
            # print "found record"
            numposts += np
            if numposts < avgposts:
                _update_record(currentnode, wid)
            else:
                currentnode += 1
                _update_record(currentnode, wid)
                numposts = 0

    print "it's done!"

