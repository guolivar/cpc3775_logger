# Load the library
import serial
# Hacks to work with custom end of line
eol = b'\r'
leneol = len(eol)
line = bytearray()
# Open the serial port and clean the I/O buffer
ser = serial.Serial('/dev/ttyUSB0',115200)
ser.flushInput()
ser.flushOutput()
# Set the time constants
rec_time=time.gmtime()
timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
prev_minute=rec_time[4]
# Start the logging
while True:
	# Request a data line from the instrument
	ser.write('rall')
	# Get the line of data from the instrument
	while True:
		c = ser.read(1)
		line += c
		if line[-leneol:] == eol:
			break
	# Debugging only ... REMOVE IT FOR DEPLOYMENT
	print(line)
	# Parse the data line
	# Set the time for the record
	rec_time=time.gmtime()
	timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
	# SAMPLE LINE ONLY
	line = '3.15E+01,0000,39.0,14.0,40.0,33.0,98.8,54.9,0.054,31,FULL (2475)'
	split_indx=line.find(',')
	concentration = eval(line[:split_indx])
	error_message = line[split_indx+1:]
	# Make the line pretty for the file
	file_line = timestamp+','+line
	# Save it to the appropriate file
	
	# Is it the top of the minute?
	if rec_time[4] == prev_minute:
		# YES! --> generate the psql statement
		
		# Update the database
	# NO 
		# Get more data
	# Is it the last minute of the day?
	# YES! compress previous day's file
	
print('I\'m done')
