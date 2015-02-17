# Load the library
import serial
# Open the serial port and clean the I/O buffer
ser = serial.Serial('/dev/ttyUSB0',11500)
ser.flushInput()
ser.flushOutput()
# Start the logging
while True:
	# Get a line of data from the instrument
	current_line = ser.readLine(None, '/n')
	# Debugging only ... REMOVE IT FOR DEPLOYMENT
	print(current_line)
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
	
