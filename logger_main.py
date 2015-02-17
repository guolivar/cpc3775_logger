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
# Start the logging
while True:
	# Get a line of data from the instrument
	while True:
		c = ser.read(1)
		print(c)
		if c:
			line += c
			if line[-leneol:] == eol:
				break
			else:
				break
	# Debugging only ... REMOVE IT FOR DEPLOYMENT
	print(line)
	break
	# Parse the data line
	
	# Add timestamp
	
	# Make the line pretty for the file
	
	# Save it to the appropriate file
	
	# Is it the top of the minute?
		# YES! --> generate the psql statement
		
		# Update the database
	# NO 
		# Get more data
	# Is it the last minute of the day?
	# YES! compress previous day's file
	
print('I\'m done')
