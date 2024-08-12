from construct import BitStruct, BitsInteger
from message.model import Message

class Beacon(Message):
    __slots__ = ["data"]

    _beacon_bits_schema = BitStruct(
        "type" / BitsInteger(4),
        "id" / BitsInteger(12),
        "latitude" / BitsInteger(24),
        "longitude" / BitsInteger(24),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return self._build(self.data)
    @classmethod
    def _build(cls, data):
        return cls._beacon_bits_schema.build(data)

    @classmethod
    def parse(cls, data):
        parsed_data = cls._beacon_bits_schema.parse(data)
        if 'latitude' in parsed_data:
            parsed_data['latitude'] = Message.cord_from_24bit(parsed_data['latitude'], -90, 90)
        if 'longitude' in parsed_data:
            parsed_data['longitude'] = Message.cord_from_24bit(parsed_data['longitude'], -180, 180)
        data = dict(parsed_data)
        data.pop('_io', None)
        return data

#
# if __name__ == "__main__":
#     beacon = Beacon(type=15, id=2, latitude=55.55, longitude=-77.77)
#     bytes_beacon = beacon.build()
#     print(bytes_beacon)
#     parsed_beacon = Beacon.parse(bytes_beacon)
#     print(parsed_beacon)