import os
import sys
import time
from datetime import datetime, timedelta

import serial
from arduino_communication.utils import find_arduino_port, store_message
from message.model import Message as MessageModel
from message.schemas import Message as MessageSchema
from beacon.model import Beacon as BeaconModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BEACONLEN = 10
message_len = 21

def send_command(arduino_port, command):
    print(f"Enviando comando: {command}")

    with serial.Serial(arduino_port, 9600, timeout=5) as ser:
        ser.dtr = False
        response = ser.read_until(b"Sistema iniciado. Aguardando comandos.\r\n")
        print(f"Resposta inicial do Arduino: {response.decode('utf-8').strip()}")
        buffer = b''
        while True:
            if ser.in_waiting > 0:
                buffer += ser.read(ser.in_waiting)
def receive_and_store_message(arduino_port, use_my_sql=False):
    global message_len
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")
        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            buffer = b''
            ser.read_until(b"Sistema iniciado. Aguardando comandos.\r\n")
            ser.write(('R' + '\n').encode())
            while True:
                if ser.in_waiting > 0:
                    buffer += ser.read(ser.in_waiting)
                    while len(buffer) >= message_len:
                        header_index = buffer.find(b'\xFF\xFF')
                        if header_index == -1:
                            buffer = b''
                            continue
                        elif header_index > 0:
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
                                success = MessageModel.vef_checksum(message, received_checksum)
                                print(
                                    f"{'Error' if not success else 'Success'} handling message. Checksum {'differs.' if not success else 'is equal.'}")

                                store_message(parsed_data, success, use_my_sql)
                                return 1
                            else:
                                print("Incorrect Header, ignoring message:",
                                      ' '.join(format(x, '02X') for x in response))
                                store_message(None, False, use_my_sql)
                                return 1

def send_beacon(arduino_port):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")
        try:
            beacon = BeaconModel(type=3, id=2, latitude=55.55, longitude=-77.77)
            serialized_beacon = beacon.build()
        except Exception as e:
            print(f"Error on creating or serializing message: {e}")
            return

        header = b'\xFF\xFF'
        beacon_with_header = header + serialized_beacon

        print(f"Message with header len: {len(beacon_with_header)} bytes")

        try:
            with serial.Serial(arduino_port, 9600, timeout=2) as ser:
                ser.read_until(b"Sistema iniciado. Aguardando comandos.\r\n")
                ser.write('B'.encode())
                ser.write(beacon_with_header)
                print("Beacon sent: ", beacon_with_header)

                response = b''
                while True:
                    response += ser.read(ser.in_waiting or 1)
                    if b"ACK Received." in response:
                        print("Confirmation received: handshake started")
                        return True
                    elif b"Timeout waiting for beacon, restarting..." in response:
                        print("No confirmation received")
                        return False
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
    else:
        print("Arduino not found")
        return

def send_message(arduino_port, message):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

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
            print(f"Error on creating or serializing message: {e}")
            return

        header = b'\xFF\xFF'
        check_sum = MessageModel.generate_checksum(serialized_message)
        message_with_header = header + serialized_message + check_sum
        print(f"Message with header len: {len(message_with_header)} bytes")

        try:
            with serial.Serial(arduino_port, 9600, timeout=2) as ser:
                ser.read_until(b"Sistema iniciado. Aguardando comandos.\r\n")
                ser.write('M'.encode())
                while True:
                    ready_message = ser.readline().decode('utf-8', errors='ignore').strip()
                    if ready_message == "READY":
                        break
                    else:
                        print(f"Waiting READY, received: {ready_message}")

                ser.write(message_with_header)
                print("Message sent: ", message_with_header)

                while True:
                    ack = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"Received: {ack}")
                    if "ACK" in ack:
                        print("Confirmation received: message sent")
                        break
                    else:
                        print("No confirmation received or incorrect confirmation")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
    else:
        print("Arduino not found")

def listen_beacon(arduino_port):
    global BEACONLEN
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        try:
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
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
    else:
        print("Arduino not found")
        return None

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
        # user_input = input("Send message or beacon? (1 for message, 2 for beacon, 3 to exit)\n")
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
        # send_command(arduino_port, 'M')  # Command to wait for message
        # receive_and_store_message(arduino_port)
        # time.sleep(5)
        if send_beacon(arduino_port):
            receive_and_store_message(arduino_port)
            time.sleep(5)
            send_message(arduino_port, message)
            coordinate_index = (coordinate_index + 1) % len(coordinates)
        # elif user_input == "2":
        #     #send_beacon(arduino_port)
        #     receive_and_store_message(arduino_port)
        # elif user_input == '3':
        #     break
        # else:
        #     print("Invalid input")

if __name__ == "__main__":
    main()