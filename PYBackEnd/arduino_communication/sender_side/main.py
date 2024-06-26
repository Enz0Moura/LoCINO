import os
import sys

import serial

from arduino_communication.utils import find_arduino_port
from message.model import Message as MessageModel
from message.schemas import Message as MessageSchema

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def send_message(arduino_port, message):
    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")

        # Inicialização da mensagem
        try:
            msg = MessageModel(
                message_type=message.message_type,
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
            exit(1)

        print(f"Message len: {len(serialized_message)} bytes")

        # Header para facilitar a identificação
        header = b'\xFF\xFF'
        check_sum = MessageModel.generate_checksum(serialized_message)
        message_with_header = header + serialized_message + check_sum

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
                        if ack == "ACK":
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


# Function test
def main():
    arduino_port = find_arduino_port()
    message = MessageSchema(
        message_type=True,
        id=1,
        latitude=50.1234,
        longitude=8.1234,
        group_flag=False,
        record_time=12345,
        max_records=2047,
        hop_count=15,
        channel=3,
        location_time=6789,
        help_flag=2,
        battery=15
    )

    send_message(arduino_port, message)


if __name__ == "__main__":
    main()
