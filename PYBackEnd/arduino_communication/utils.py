import serial
import serial.tools.list_ports

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description or 'Mega' in port.description or 'VID:PID' in port.hwid:
            return port.device
    return None