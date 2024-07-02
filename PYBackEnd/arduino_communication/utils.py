import os
import serial
import serial.tools.list_ports
from PYBackEnd.models.insert_main import insert_message_result

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'Arduino' in port.description or 'Mega' in port.description or 'VID:PID' in port.hwid:
            return port.device
    return None


def store_message(received_data, success=True):
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_directory = os.path.join(project_root, 'db')

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    insert_message_result(success, received_data)
