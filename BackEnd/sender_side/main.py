import serial
from BackEnd.message.model import Message

arduino_port = 'COM4'  # Verifique se esta é a porta correta

if arduino_port:
    print(f"Arduino encontrado na porta: {arduino_port}")

    # Inicialização da mensagem
    try:
        msg = Message(
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
        serialized_message = msg.build()
    except Exception as e:
        print(f"Erro ao criar ou serializar a mensagem: {e}")
        exit(1)

    # Verifique o tamanho da mensagem
    print(f"Tamanho da mensagem: {len(serialized_message)} bytes")

    # Adicione um cabeçalho para facilitar a identificação
    header = b'\xFF\xFF'
    message_with_header = header + serialized_message

    try:
        # Envia a mensagem serializada via porta serial
        with serial.Serial(arduino_port, 9600, timeout=2) as ser:
            # Espera pela mensagem "READY" do Arduino
            while True:
                ready_message = ser.readline().decode('utf-8', errors='ignore').strip()
                if ready_message == "READY":
                    break
                else:
                    print(f"Aguardando READY, recebido: {ready_message}")

            ser.write(message_with_header)
            print("Mensagem enviada: ", message_with_header)

            # Espera pela confirmação do Arduino
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
