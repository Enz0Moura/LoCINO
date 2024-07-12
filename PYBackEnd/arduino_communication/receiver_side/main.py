import os
import sys
import time

import serial
from arduino_communication.utils import find_arduino_port, store_message
from beacon.model import Beacon as BeaconModel
from message.model import Message as MessageModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
message_len = 21


def send_beacon(arduino_port):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")
        try:
            beacon = BeaconModel(type=3, id=2, latitude=55.55, longitude=-77.77)
            serialized_beacon = beacon.build()
        except Exception as e:
            raise Exception(f"Error on creating or serializing message: {e}")

        header = b'\xFF\xFF'

        beacon_with_header = header + serialized_beacon

        print(f"Message with header len: {len(beacon_with_header)} bytes")

        try:
            # Envia a mensagem serializada via porta serial
            with serial.Serial(arduino_port, 9600, timeout=2) as ser:
                while True:
                    ready_message = ser.readline().decode('utf-8', errors='ignore').strip()
                    if ready_message == "READY":
                        break
                    else:
                        print(f"Waiting READY, received: {ready_message}")

                ser.write(beacon_with_header)
                print("Beacon sent: ", beacon_with_header)

                # Esperando confirmação do Arduino
                try:
                    while True:
                        ack = ser.readline().decode('utf-8', errors='ignore').strip()
                        print(f"Received: {ack}")
                        if ack == "ACK":
                            print("Confirmation received: handshake started")
                            return 1
                        else:
                            print("No confirmation received")
                            return 0

                except serial.SerialTimeoutException:
                    print("Timeout: No confirmation received")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")

    else:
        print("Arduino not found")
        return


def receive_and_store_message(arduino_port):
    global message_len
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            buffer = b'\xFF\xFF'
            ser.write(buffer)
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
                                message = response[2:(message_len - 2)]
                                received_checksum = response[(message_len - 2):message_len]
                                parsed_data = MessageModel.parse(message)
                                print(f"Deserialized message:{parsed_data}\nCheck Sum: {received_checksum}")
                                success = False if not MessageModel.vef_checksum(message, received_checksum) else True
                                print(
                                    f"{'Error' if not success else 'Success'} handling message. Checksum {'differs.' if not success else 'is equal.'}")

                                store_message(parsed_data, success, use_my_sql=True)
                            else:
                                print("Incorrect Header, ignoring message:",
                                      ' '.join(format(x, '02X') for x in response))
                                store_message(None, False, use_my_sql=True)
    else:
        print("Arduino not found")


def main():
    arduino_port = find_arduino_port()
    ack = 0
    while (ack == 0):
        ack = send_beacon(arduino_port)
        if ack == 0:
            time.sleep(5)

    receive_and_store_message(arduino_port)


if __name__ == "__main__":
    main()
