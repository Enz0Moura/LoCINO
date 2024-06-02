import serial
from PYBackEnd.message.model import Message
from PYBackEnd.arduino_communication.utils import find_arduino_port
from PYBackEnd.message.schemas import Message as MessageSchema
def send_message(arduino_port, message):
    if arduino_port:
        print(f"Arduino encontrado na porta: {arduino_port}")

        # Inicialização da mensagem
        try:
            msg = Message(
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
            print(f"Erro ao criar ou serializar a mensagem: {e}")
            exit(1)

        print(f"Tamanho da mensagem: {len(serialized_message)} bytes")

        # Header para facilitar a identificação
        header = b'\xFF\xFF'
        message_with_header = header + serialized_message

        try:
            # Envia a mensagem serializada via porta serial
            with serial.Serial(arduino_port, 9600, timeout=2) as ser:
                while True:
                    ready_message = ser.readline().decode('utf-8', errors='ignore').strip()
                    if ready_message == "READY":
                        break
                    else:
                        print(f"Aguardando READY, recebido: {ready_message}")

                ser.write(message_with_header)
                print("Mensagem enviada: ", message_with_header)

                # Esperando confirmação do Arduino
                try:
                    while True:
                        ack = ser.readline().decode('utf-8', errors='ignore').strip()
                        print(f"Recebido: {ack}")
                        if ack == "ACK":
                            print("Confirmação recebida: Mensagem enviada com sucesso")
                            break
                        else:
                            print("Nenhuma confirmação recebida ou confirmação incorreta")

                except serial.SerialTimeoutException:
                    print("Timeout: Nenhuma confirmação recebida")
        except serial.SerialException as e:
            print(f"Erro na comunicação serial: {e}")
    else:
        print("Arduino não encontrado")

#testando a função

if __name__ == "__main__":
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