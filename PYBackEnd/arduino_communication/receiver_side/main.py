import json
import os
import sys

import serial

from arduino_communication.utils import find_arduino_port, store_message
from message.model import Message as MessageModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
message_len = 21
def receive_and_store_message(arduino_port):
    global message_len
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            buffer = b''
            while True:
                if ser.in_waiting > 0:
                    buffer += ser.read(ser.in_waiting)
                    while len(buffer) >= message_len:
                        header_index = buffer.find(b'\xFF\xFF')
                        if header_index == -1:
                            # Se não encontrar o cabeçalho, limpe o buffer para evitar dados antigos
                            buffer = b''
                        elif header_index > 0:
                            # Se encontrar o cabeçalho mas não estiver no início, remova bytes anteriores
                            buffer = buffer[header_index:]
                        if len(buffer) >= message_len:
                            response = buffer[:message_len]
                            buffer = buffer[message_len:]

                            print("Received message from Arduino:", ' '.join(format(x, '02X') for x in response))

                            if response[:2] == b'\xFF\xFF':
                                print(response)
                                message = response[2:(message_len-2)]
                                received_checksum = response[(message_len - 2):message_len]
                                parsed_data = MessageModel.parse(message)
                                print(f"Deserialized message:{parsed_data}\nCheck Sum: {received_checksum}")
                                success = False if not MessageModel.vef_checksum(message, received_checksum) else True
                                print(f"{'Error' if not success else 'Success'} handling message. Checksum {'differs.' if not success else 'is equal.'}")
                                store_message(json.dumps(parsed_data), success)
                            else:
                                print("Incorrect Header, ignoring message:",
                                      ' '.join(format(x, '02X') for x in response))
                                store_message(None, False, use_my_sql=True)
    else:
        print("Arduino not found")


def main():
    arduino_port = find_arduino_port()
    receive_and_store_message(arduino_port)


if __name__ == "__main__":
    main()
