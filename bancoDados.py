import os
import psycopg2

con = psycopg2.connect(
    host=os.environ['pgServerJB'], 
    database=os.environ['pgBaseJB'],
    user=os.environ['pgUserJB'], 
    password=os.environ['pgPassJB']
)
cur = con.cursor()
