# Load the libraries
import serial # Serial communications
import time # Timing utilities
import psycopg2 # PostgreSQL wrapper

# Set the time constants
rec_time=time.gmtime()
timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
prev_minute=rec_time[4]
prev_file = time.strftime("%Y%m%d.txt",rec_time)
# Set the minute averaging variable
min_concentration=0
n_concentration = 0
# Set the pre/post SQL statement values
insert_statement = """INSERT INTO data.fixedmeasurements 
(parameterid,value,siteid,recordtime) 
VALUES (%s,%s,%s,timestamptz %s);"""
# Read the settings from the settings file
settings_file = open("./settings.txt")
# e.g. "/dev/ttyUSB0"
port = settings_file.readline().rstrip('\n')
# path for data files
# e.g. "/home/logger/datacpc3775/"
datapath = settings_file.readline().rstrip('\n')
# psql connection string
# e.g "user=datauser password=l3tme1n host=penap-data.dyndns.org dbname=didactic port=5432"
db_conn = settings_file.readline().rstrip('\n')
# ID values for the parameters and site (DATA, ERROR, SITE)
# e.g. "408,409,2" == CPCdata,CPCerror,QueenStreet
params = settings_file.readline().rstrip('\n').split(",")
# Close the settings file
settings_file.close()
# Hacks to work with custom end of line
eol = b'\r'
leneol = len(eol)
bline = bytearray()
# Open the serial port and clean the I/O buffer
ser = serial.Serial(port,115200)
ser.flushInput()
ser.flushOutput()
# Start the logging
while True:
	# Request a data line from the instrument
	ser.write('rall\r')
	# Get the line of data from the instrument
	while True:
		c = ser.read(1)
		bline += c
		if bline[-leneol:] == eol:
			break
	# Parse the data line
	line = bline.decode("utf-8")
	# Set the time for the record
	rec_time_s = int(time.time())
	rec_time=time.gmtime()
	timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
	# SAMPLE LINE ONLY
	# line = "3.15E+01,0000,39.0,14.0,40.0,33.0,98.8,54.9,0.054,31,FULL (2475)"
	split_indx=line.find(',')
	concentration = eval(line[:split_indx])
	min_concentration += concentration
	n_concentration += 1
	error_message = line[split_indx+1:]
	# Make the line pretty for the file
	file_line = timestamp+','+line
	# Save it to the appropriate file
	current_file = open(datapath+time.strftime("%Y%m%d.txt",rec_time))
	current_file.write(file_line+"\n")
	current_file.flush()
	current_file.close()
	line = ""
	bline = bytearray()
	# Is it the top of the minute?
	if rec_time[4] != prev_minute:
		# YES! --> generate the psql statement
		# Average for the minute with what we have
		min_concentration = min_concentration / n_concentration
		# Connect to the database
		con = psycopg2.connect(db_conn)
		cur = con.cursor()
		# Insert the DATA record
		cur.execute(insert_statement,
		(params[0],min_concentration,params[2]),timestamp))
		# Insert the ERROR record
		cur.execute(insert_statement,
		(params[1],line[split_indx:],params[2],timestamp))
		# Commit and close connection to the database
		con.commit()
		cur.close()
		con.close()
		# Reinitialize the cummulative variables
		min_concentration = 0
		n_concentration = 0
	# Is it the last minute of the day?
	if current_file != prev_file:
		subprocess.call(["gzip",prev_file])
		prev_file = current_file
	# Wait until the next second
	while int(time.time())<=rec_time_s:
		#wait a few miliseconds
		time.sleep(0.05)	
print('I\'m done')
