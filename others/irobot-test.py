import serial
import serial.tools.list_ports

list = serial.tools.list_ports.comports();
for i in range(len(list)):
    print list[i][0]
