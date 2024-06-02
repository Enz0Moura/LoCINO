import os
import serial
import serial.tools.list_ports

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description or 'Mega' in port.description or 'VID:PID' in port.hwid:
            return port.device
    return None

def store_message(received_data):
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_directory = os.path.join(project_root, 'db')


    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    file_path = os.path.join(db_directory, 'received_messages.txt')

    with open(file_path, 'a') as file:
        file.write(str(received_data) + '\n')
        file.flush()
        os.fsync(file.fileno())