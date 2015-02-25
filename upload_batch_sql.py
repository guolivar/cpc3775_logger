#!/usr/bin/env python
# Load the libraries
import time # Timing utilities
import psycopg2 # PostgreSQL wrapper
import subprocess # Shell utilities ... compressing data files
# Read the settings from the settings file
settings_file = open("./settings.txt")
# e.g. "/dev/ttyUSB0"
port = settings_file.readline().rstrip('\n')
# path for data files
# e.g. "/home/logger/datacpc3775/"
datapath = settings_file.readline().rstrip('\n') + "SQL/"
# psql connection string
# e.g "user=datauser password=l3tme1n host=penap-data.dyndns.org dbname=didactic port=5432"
db_conn = settings_file.readline().rstrip('\n')
# ID values for the parameters and site (DATA, ERROR, SITE)
# e.g. "408,409,2" == CPCdata,CPCerror,QueenStreet
params = settings_file.readline().rstrip('\n').split(",")
# Close the settings file
settings_file.close()
# Set the time constants
prefix = time.strftime("%Y%m%d%H%M%S",time.gmtime())
try:
	con = psycopg2.connect(db_conn)
except psycopg2.Error, e:
	pass
else:
	subprocess.call(["mv",datapath + "missed_inserts.sql",datapath + "processing.sql"])
	sql_buffer = open(datapath + "processing.sql","r")
	cur = con.cursor()
	for line in sql_buffer:
		cur.execute(line)
	con.commit()
	cur.close()
	con.close()
	subprocess.call(["mv",datapath + "processing.sql",datapath + prefix + "processing.sql"])
	subprocess.call(["gzip",datapath + prefix + "processing.sql"])