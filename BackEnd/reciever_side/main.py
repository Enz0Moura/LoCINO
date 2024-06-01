from BackEnd.message.model import Message
import serial

def receive_and_store_message():
    arduino_port = find_arduino()
    if arduino_port:
        print(f"Arduino encontrado na porta: {arduino_port}")

        with serial.Serial(arduino_port, 9600, timeout=5) as ser:
            while True:
                response = ser.read(34)  # 2 bytes de cabeçalho + 32 bytes de dados
                if response:
                    print("Mensagem recebida do Arduino:", response)

                    # Desserializar a mensagem
                    received_data = Message.parse(response[2:])  # Ignorar o cabeçalho
                    print("Mensagem desserializada:", received_data)
                    
                    # Armazena a mensagem
                    with open('received_messages.txt', 'a') as file:
                        file.write(str(received_data) + '\n')
    else:
        print("Arduino não encontrado")

if __name__ == "__main__":
    receive_and_store_message()