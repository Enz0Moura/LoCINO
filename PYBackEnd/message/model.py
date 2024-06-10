from construct import BitStruct, Flag, BitsInteger


class Message:
    __slots__ = ["data"]

    _message_bits_schema = BitStruct(
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

    def __init__(self, **kwargs):
        if 'latitude' in kwargs:
            kwargs['latitude'] = Message.__cord_to_24bit(kwargs['latitude'], -90, 90)
        if 'longitude' in kwargs:
            kwargs['longitude'] = Message.__cord_to_24bit(kwargs['longitude'], -180, 180)
        self.data = kwargs

    @classmethod
    def __cord_from_24bit(cls, value, range_min, range_max, bits=24):
        """Converte um valor de coordenada do 24 bits de volta para seu valor original no intervalo.

          Range para latitude: -90 até 90

          Range para longitude: -180 até 180
          """

        normalized = value / (2 ** bits - 1)
        return normalized * (range_max - range_min) + range_min

    @classmethod
    def __cord_to_24bit(cls, value, range_min, range_max, bits=24):
        """Converte um valor de coordenada do seu intervalo original para um valor de 24 bits.

            Range para latitude: -90 até 90

            Range para longitude: -180 até 180
            """
        normalized = (value - range_min) / (range_max - range_min)
        return int(normalized * (2 ** bits - 1))

    def build(self):
        return self._build(self.data)

    @classmethod
    def _build(cls, data):
        return cls._message_bits_schema.build(data)

    @classmethod
    def parse(cls, data):
        parsed_data = cls._message_bits_schema.parse(data)
        if 'latitude' in parsed_data:
            parsed_data['latitude'] = Message.__cord_from_24bit(parsed_data['latitude'], -90, 90)
        if 'longitude' in parsed_data:
            parsed_data['longitude'] = Message.__cord_from_24bit(parsed_data['longitude'], -180, 180)
        data = dict(parsed_data)
        data.pop('_io', None)
        return data
