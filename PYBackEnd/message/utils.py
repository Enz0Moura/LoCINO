from datetime import datetime
from math import pi
from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS = 6371.000
EARTH_CIRCUNFERENCE = EARTH_RADIUS * pi * 2
KM_PER_DEGREE = EARTH_CIRCUNFERENCE / 360


def calculate_distance(lat1, long1, lat2, long2):
    global KM_PER_DEGREE

    distance = sqrt(((lat2 - lat1) ** 2) + ((long2 - long1) ** 2)) * KM_PER_DEGREE * 1000  # Distancia em m
    return distance


def haversine(lat1, long1, lat2, long2):
    global EARTH_RADIUS
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    delta_lat = lat2 - lat1
    delta_long = long2 - long1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS * c * 1000  # Calcula a distancia em m
    return distance


def calculate_total_distance(points, use_haversine=False):
    total_distance = 0.0
    for i in range(len(points) - 1):
        lat1, long1 = points[i]
        lat2, long2 = points[i + 1]

        total_distance += calculate_distance(lat1, long1, lat2, long2) if not use_haversine else haversine(lat1, long1,
                                                                                                           lat2, long2)
    return total_distance


def calculate_total_distance_and_time(points, use_haversine=False):
    total_distance = 0.0
    total_time = 0.0

    for i in range(len(points) - 1):
        lat1, long1, time1 = points[i]
        lat2, long2, time2 = points[i + 1]

        distance = haversine(lat1, long1, lat2, long2) if use_haversine else calculate_distance(lat1, long1, lat2,
                                                                                                long2)
        total_distance += distance

        time_diff = (time2 - time1).total_seconds()
        total_time += time_diff

    return total_distance, total_time


def calculate_average_speed(points, use_haversine=False):
    total_distance, total_time = calculate_total_distance_and_time(points, use_haversine)
    if total_time == 0:
        return 0
    return total_distance / total_time


def calculate_destination(lat, long, distance_km, azimuth):
    km_per_degree_long = KM_PER_DEGREE * cos(radians(lat))
    delta_lat = (distance_km / KM_PER_DEGREE) * cos(radians(azimuth))
    delta_long = (distance_km / km_per_degree_long) * sin(radians(azimuth))
    return (lat + delta_lat, long + delta_long)

def calculate_displacement_area(average_speed_m_s, initial_point, last_timestamp, step_degrees=10):
    current_timestamp = datetime.now()
    elapsed_time_seconds = (current_timestamp - last_timestamp).total_seconds()
    max_distance_meters = average_speed_m_s * elapsed_time_seconds
    max_distance_km = max_distance_meters / 1000

    initial_point = (initial_point[0], initial_point[1])

    displacement_points = []
    for azimuth in range(0, 360, step_degrees):
        displacement_points.append(calculate_destination(initial_point[0], initial_point[1], max_distance_km, azimuth))

    displacement_area_m2 = pi * (max_distance_meters ** 2)
    return displacement_points, displacement_area_m2, max_distance_meters

if __name__ == '__main__':
    # List of points (latitude, longitude, datetime) simulating a trail
    trail_points = [
        (-20.1435, -44.8912, datetime(2024, 7, 31, 20, 0, 0)),
        (-20.1345, -44.8800, datetime(2024, 7, 31, 21, 10, 0))
    ]

    average_speed = calculate_average_speed(trail_points, use_haversine=False)
    print(f"The average speed on the trail is {average_speed:.2f} m/s")

    initial_point = (-20.1435, -44.8912)
    last_timestamp = datetime(2024, 7, 31, 21, 10, 0)
    displacement_area, displacement_area_m2, max_distance_meters = calculate_displacement_area(average_speed,
                                                                                               initial_point,
                                                                                               last_timestamp,
                                                                                               step_degrees=10)
    print("Possible displacement area (points of the circle):")
    for point in displacement_area:
        print(point)
    print("Possible displacement area (M²")
    print(displacement_area_m2)
    print(f"Max distance meters: \n{max_distance_meters}")