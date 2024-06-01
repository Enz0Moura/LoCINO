def cord_to_24bit(value, range_min, range_max, bits=24):
    """Converte um valor de coordenada do seu intervalo original para um valor de 24 bits.

    Range para latitude: -90 até 90

    Range para longitude: -180 até 180
    """
    normalized = (value - range_min) / (range_max - range_min)
    return int(normalized * (2 ** bits - 1))


def cord_from_24bit(value, range_min, range_max, bits=24):
    """Converte um valor de coordenada do 24 bits de volta para seu valor original no intervalo.

    Range para latitude: -90 até 90

    Range para longitude: -180 até 180
    """

    normalized = value / (2 ** bits - 1)
    return normalized * (range_max - range_min) + range_min
