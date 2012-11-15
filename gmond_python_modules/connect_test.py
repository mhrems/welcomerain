import serial
import time

PORT_NUM = range(10)


def getPort(index):
    try:
    	return '/dev/ttyUSB%s'%(index)
    except:
	return False

for index in PORT_NUM:
    print index
    port =  getPort(index)
    if not port:
	print 'error'
	continue
    else:
    	print port
    	ser = serial.Serial(port=port,timeout=1)
    	ser.write('S')
    	print ser.readline()
#    ser.close()
    time.sleep(2)
