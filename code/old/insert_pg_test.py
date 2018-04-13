#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None

con = psycopg2.connect("dbname='blockwise' user='postgres' password='purplerain'")   
    
cur = con.cursor()
  
cur.execute("INSERT INTO blockadvisor_location(location_id, business_name, address, street_number, street_name, rank, review_count, rating) VALUES(500000, 'Judy Place', '4727 13th Street NW', '4727','13th Street NW', 0, 0, 0)")
    
con.commit()
    
con.close()
