import os
import sys
import time
from datetime import datetime, timedelta

import serial
from arduino_communication.receiver_side.main import receive_and_store_message
from arduino_communication.utils import find_arduino_port
from message.model import Message as MessageModel
from message.schemas import Message as MessageSchema
from arduino_communication.receiver_side.main import send_command
from beacon.model import Beacon as BeaconModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BEACONLEN = 10

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

def send_message(arduino_port, message):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        # Inicialização da mensagem
        try:
            msg = MessageModel(
                type=message.type,
                id=message.id,
                latitude=message.latitude,
                longitude=message.longitude,
                group_flag=message.group_flag,
                record_time=message.record_time,
                max_records=message.max_records,
                hop_count=message.hop_count,
                channel=message.channel,
                location_time=message.location_time,
                help_flag=message.help_flag,
                battery=message.battery,
            )
            serialized_message = msg.build()

        except Exception as e:
            raise Exception(f"Error on creating or serializing message: {e}")

        print(f"Message len: {len(serialized_message)} bytes")
        # Header para facilitar a identificação
        header = b'\xFF\xFF'
        check_sum = MessageModel.generate_checksum(serialized_message)
        message_with_header = header + serialized_message + check_sum
        print(f"Message with header len: {len(message_with_header)} bytes")

        try:
            # Envia a mensagem serializada via porta serial
            with serial.Serial(arduino_port, 9600, timeout=2) as ser:
                while True:
                    ready_message = ser.readline().decode('utf-8', errors='ignore').strip()
                    if ready_message == "READY":
                        break
                    else:
                        print(f"Waiting READY, received: {ready_message}")

                ser.write(message_with_header)
                print("Message sent: ", message_with_header)

                # Esperando confirmação do Arduino
                try:
                    while True:
                        ack = ser.readline().decode('utf-8', errors='ignore').strip()
                        print(f"Received: {ack}")
                        if ack.find("ACK") != -1:
                            print("Confirmation received: message sent")
                            break
                        else:
                            print("No confirmation received or incorrect confirmation")
                except serial.SerialTimeoutException:
                    print("Timeout: No confirmation received")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
    else:
        print("Arduino not found")


def listen_beacon(arduino_port):
    global BEACONLEN
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            buffer = b''
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    buffer += data
                    print(buffer)

                    if b"Beacon Received" in buffer:
                        return 1

                    if len(buffer) > 1000:
                        buffer = buffer[-1000:]
            return None
    else:
        print("Arduino not found")


# Function test
def main():
    arduino_port = find_arduino_port()
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=5)
    coordinates = [
        (-22.5118074, -43.1788471),
        (-22.5099877, -43.1753572),
        (-22.5087312, -43.1723941),
        (-22.5071419, -43.1694926)
    ]
    coordinate_index = 0

    memory = [MessageSchema(
        type=True,
        id=2,
        latitude=-22.509997449415415,
        longitude=-43.18229837292253,
        group_flag=False,
        record_time=int(time.time() - ((1 * 60 * 60) + (5 * 60))),
        max_records=255,
        hop_count=15,
        channel=3,
        location_time=0,
        help_flag=2,
        battery=3),
        MessageSchema(
            type=True,
            id=2,
            latitude=-22.510304703568117,
            longitude=-43.184186648149826,
            group_flag=False,
            record_time=int(time.time() - (1 * 60 * 60)),
            max_records=255,
            hop_count=15,
            channel=3,
            location_time=0,
            help_flag=2,
            battery=3)
    ]

    while True:
        user_input = "1" #input("Send message?\n")
        if user_input == "1":
            lat, long = coordinates[coordinate_index]
            message = MessageSchema(
                type=True,
                id=1,
                latitude=lat,
                longitude=long,
                group_flag=False,
                record_time=int(time.time()),
                max_records=255,
                hop_count=15,
                channel=3,
                location_time=0,
                help_flag=2,
                battery=3
            )
            send_message(arduino_port, message)
            time.sleep(5)
            receive_and_store_message(arduino_port)
            coordinate_index = (coordinate_index + 1) % len(coordinates)
        if user_input == '3':
            break
        # time.sleep(60)

#TODO: Olhar com mais detalhes a troca de ack após receber o beacon
#TODO: posso usar paralelismo?
if __name__ == "__main__":
    main()
