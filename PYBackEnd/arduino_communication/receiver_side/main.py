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
                response = b''
                while b"Sending Beacon" not in response:
                    response += ser.read(ser.in_waiting or 1)
                ser.write(beacon_with_header)
                print("Beacon sent: ", beacon_with_header)

                # Esperando confirmação do Arduino
                try:
                    # while b"No confirmation received" not in response and b"ACK" not in response:
                    #     response += ser.read(ser.in_waiting or 1)
                    while True:
                        response += ser.read(ser.in_waiting or 1)
                    print("Waiting for ACK")
                    if b"No confirmation received" in response:
                        print("No confirmation received")
                        return None
                    elif b"ACK" in response:
                        print("Confirmation received: handshake started")
                        return 1


                except serial.SerialTimeoutException:
                    print("Timeout: No confirmation received")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")

    else:
        print("Arduino not found")
        return


def receive_and_store_message(arduino_port, use_my_sql=False):
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
                            continue
                        elif header_index > 0:
                            # Se encontrar o cabeçalho mas não estiver no início, remova bytes anteriores
                            buffer = buffer[header_index:]
                        if len(buffer) >= message_len:
                            response = buffer[:message_len]
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

                            store_message(parsed_data, success, use_my_sql)
                            return 1
                        else:
                            print("Incorrect Header, ignoring message:",
                                  ' '.join(format(x, '02X') for x in response))
                            store_message(None, False, use_my_sql)
                            return 1

            else:
                return 0
    else:
        print("Arduino not found")


def main():
    arduino_port = find_arduino_port()
    # ack = 0
    # while (ack == 0):
    #     ack = send_beacon(arduino_port)
    #     if ack == 0:
    #         time.sleep(5)

    receive_and_store_message(arduino_port, use_my_sql=False)


if __name__ == "__main__":
    main()
