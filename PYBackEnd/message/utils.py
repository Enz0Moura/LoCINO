from math import pi
from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS = 6371.000
EARTH_CIRCUNFERENCE = EARTH_RADIUS * pi * 2
KM_PER_DEGREE = EARTH_CIRCUNFERENCE / 360


def calculate_distance(lat1, long1, lat2, long2):
    global KM_PER_DEGREE

    distance = sqrt(((lat2 - lat1) ** 2) + ((long2 - long1) ** 2)) * KM_PER_DEGREE
    return distance


def haversine(lat1, long1, lat2, long2):
    global EARTH_RADIUS
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    delta_lat = lat2 - lat1
    delta_long = long2 - long1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance


def calculate_total_distance(points, use_haversine=False):
    total_distance = 0.0
    for i in range(len(points) - 1):
        lat1, long1 = points[i]
        lat2, long2 = points[i + 1]

        total_distance += calculate_distance(lat1, long1, lat2, long2) if not use_haversine else haversine(lat1, long1,
                                                                                                           lat2, long2)
    return total_distance


# if __name__ == '__main__':
#     dist1 = calculate_distance(-20.1435, -44.8912, -20.0739, -44.5734)
#     print(f"A distância é {dist1:.2f}KM")
#
#     dist2 = haversine(-20.1435, -44.8912, -20.0739, -44.5734)
#     print("*" * 30)
#     print(f"Haversine\nA distância é {dist2:.2f}KM")
