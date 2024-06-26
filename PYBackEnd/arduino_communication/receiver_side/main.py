import os
import sys

import serial

from PYBackEnd.arduino_communication.utils import find_arduino_port, store_message
from PYBackEnd.message.model import Message as MessageModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def receive_and_store_message(arduino_port):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            buffer = b''
            while True:
                if ser.in_waiting > 0:
                    buffer += ser.read(ser.in_waiting)
                    while len(buffer) >= 17:
                        # Procura pelo cabeçalho na mensagem
                        header_index = buffer.find(b'\xFF\xFF')
                        if header_index == -1:
                            # Se não encontrar o cabeçalho, limpe o buffer para evitar dados antigos
                            buffer = b''
                        elif header_index > 0:
                            # Se encontrar o cabeçalho mas não estiver no início, remova bytes anteriores
                            buffer = buffer[header_index:]
                        if len(buffer) >= 17:
                            response = buffer[:17]
                            buffer = buffer[17:]

                            print("Received message from Arduino:", ' '.join(format(x, '02X') for x in response))

                            if response[:2] == b'\xFF\xFF':
                                message = response[2:25]
                                recieved_checksum = response[25:27]
                                parsed_data = MessageModel.parse(message)  # Ignorar o cabeçalho
                                print(f"Deserialized message:{parsed_data}\nCheck Sum: {recieved_checksum}")
                                sucess = True
                                if not MessageModel.vef_checksum(message):
                                    print("Error handling message. Checksum differs.")
                                    sucess = False
                                store_message(parsed_data, sucess)
                            else:
                                print("Incorrect Header, ignoring message:",
                                      ' '.join(format(x, '02X') for x in response))
    else:
        print("Arduino not found")


def main():
    arduino_port = find_arduino_port()
    receive_and_store_message(arduino_port)


if __name__ == "__main__":
    main()
