from typing import List, Tuple
import math

# Function to calculate the distance between two points using the Haversine formula
def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    
    :param coord1: Tuple containing the latitude and longitude of the first point (lat1, lon1)
    :param coord2: Tuple containing the latitude and longitude of the second point (lat2, lon2)
    :return: Distance between the two points in kilometers
    """
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Function to calculate the total distance of a route given a list of coordinates
def total_route_distance(route: List[Tuple[float, float]]) -> float:
    """
    Calculate the total distance of a route given a list of coordinates.
    
    :param route: List of tuples containing the latitude and longitude of each point in the route
    :return: Total distance of the route in kilometers
    """
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += haversine_distance(route[i], route[i + 1])
    return total_distance

# Function to calculate the average speed given the total distance and total time
def average_speed(total_distance: float, total_time: float) -> float:
    """
    Calculate the average speed given the total distance and total time.
    
    :param total_distance: Total distance traveled in kilometers
    :param total_time: Total time taken in hours
    :return: Average speed in kilometers per hour
    """
    if total_time == 0:
        return 0.0
    return total_distance / total_time

# Function to find the fastest segment in a route given a list of segment times
def fastest_segment(segment_times: List[float]) -> float:
    """
    Find the fastest segment in a route given a list of segment times.
    
    :param segment_times: List of times taken for each segment in seconds
    :return: Fastest segment time in seconds
    """
    if not segment_times:
        return 0.0
    return min(segment_times)

# Function to find the fastest known time (FKT) for a given route
def fastest_known_time(route_times: List[float]) -> float:
    """
    Find the fastest known time (FKT) for a given route.
    
    :param route_times: List of times taken for the route in seconds
    :return: Fastest known time in seconds
    """
    if not route_times:
        return 0.0
    return min(route_times)
