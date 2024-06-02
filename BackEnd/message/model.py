from construct import BitStruct, Flag, BitsInteger
from BackEnd.message.strategies import cord_from_24bit, cord_to_24bit

message_bits_schema = BitStruct(
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
        return message_bits_schema.build(self.data)

    @staticmethod
    def parse(data):
        parsed_data = message_bits_schema.parse(data)
        if 'latitude' in parsed_data:
            parsed_data['latitude'] = cord_from_24bit(parsed_data['latitude'], -90, 90)
        if 'longitude' in parsed_data:
            parsed_data['longitude'] = cord_from_24bit(parsed_data['longitude'], -180, 180)
        data = dict(parsed_data)
        data.pop('_io', None)
        return data