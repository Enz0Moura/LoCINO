import serial
from construct import BitStruct, Flag, BitsInteger
from message.strategies import cord_to_24bit, cord_from_24bit

# Definição da estrutura da mensagem
message_schema = BitStruct(
    "message_type" / Flag,
    "id" / BitsInteger(15),
    "latitude" / BitsInteger(24),
    "longitude" / BitsInteger(24),
    "group_flag" / Flag,
    "record_time" / BitsInteger(16),
    "max_records" / BitsInteger(11),
    "hop_count" / BitsInteger(4),
    "channel" / BitsInteger(2),
    "location_time" / BitsInteger(16),
    "help_flag" / BitsInteger(2),
    "battery" / BitsInteger(4),
)

class Message:
    def __init__(self, **kwargs):
        if 'latitude' in kwargs:
            kwargs['latitude'] = cord_to_24bit(kwargs['latitude'], -90, 90)
        if 'longitude' in kwargs:
            kwargs['longitude'] = cord_to_24bit(kwargs['longitude'], -180, 180)
        self.data = kwargs

    def build(self):
        return message_schema.build(self.data)

    @staticmethod
    def parse(data):
        parsed_data = message_schema.parse(data)
        if 'latitude' in parsed_data:
            parsed_data['latitude'] = cord_from_24bit(parsed_data['latitude'], -90, 90)
        if 'longitude' in parsed_data:
            parsed_data['longitude'] = cord_from_24bit(parsed_data['longitude'], -180, 180)
        data = dict(parsed_data)
        data.pop('_io', None)
        return data

# Exemplo de uso
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

# Envia a mensagem serializada via porta serial
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    ser.write(serialized_message)
    print("Mensagem enviada: ", serialized_message)
