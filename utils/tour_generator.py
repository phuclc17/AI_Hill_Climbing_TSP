import random
from typing import List
from models.city import City
from utils.distance_matrix import DistanceMatrix


def random_tour(cities: List[City], seed: int = None) -> List[City]:
    """
    Tạo một tour ngẫu nhiên từ danh sách các thành phố.
    
    Args:
        cities (List[City]): Danh sách các thành phố
        seed (int, optional): Seed cho random để tái tạo kết quả
        
    Returns:
        List[City]: Danh sách các thành phố đã được xáo trộn ngẫu nhiên
    """
    if seed is not None:
        random.seed(seed)
    
    cities_copy = list(cities)
    random.shuffle(cities_copy)
    
    return cities_copy


def nearest_neighbor_tour(cities: List[City], distance_matrix: DistanceMatrix, 
                         start_city: City = None) -> List[City]:
    """
    Tạo tour bằng thuật toán Nearest Neighbor (láng giềng gần nhất).
    
    Thuật toán:
    1. Bắt đầu từ một thành phố (ngẫu nhiên hoặc chỉ định)
    2. Luôn chọn thành phố gần nhất chưa được thăm
    3. Lặp lại cho đến khi thăm hết tất cả thành phố
    
    Args:
        cities (List[City]): Danh sách tất cả các thành phố
        distance_matrix (DistanceMatrix): Ma trận khoảng cách
        start_city (City, optional): Thành phố bắt đầu. Nếu None, chọn ngẫu nhiên
        
    Returns:
        List[City]: Tour được tạo theo thuật toán Nearest Neighbor
    """
    if not cities:
        return []
    
    if start_city is None:
        current_city = random.choice(cities)
    else:
        current_city = start_city
    
    tour = [current_city]
    unvisited = set(city.id for city in cities if city.id != current_city.id)
    
    id_to_city = {city.id: city for city in cities}
    
    while unvisited:
        nearest_city_id = distance_matrix.get_nearest_city(current_city.id, unvisited)
        
        if nearest_city_id is None:
            break
        
        nearest_city = id_to_city[nearest_city_id]
        tour.append(nearest_city)
        unvisited.remove(nearest_city_id)
        current_city = nearest_city
    
    return tour


def greedy_tour(cities: List[City], distance_matrix: DistanceMatrix) -> List[City]:

    if not cities:
        return []
    
    edges = []
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distance = distance_matrix.get_distance(cities[i].id, cities[j].id)
            edges.append((distance, cities[i], cities[j]))
    
    edges.sort() 

    graph = {city: [] for city in cities}
    
    for distance, city_a, city_b in edges:
        
        if len(graph[city_a]) < 2 and len(graph[city_b]) < 2:
            graph[city_a].append(city_b)
            graph[city_b].append(city_a)
            
            if sum(len(neighbors) for neighbors in graph.values()) // 2 == len(cities):
                break
    
    start_city = None
    for city, neighbors in graph.items():
        if len(neighbors) == 1:
            start_city = city
            break
    
    if start_city is None:
        start_city = cities[0]
    
    tour = [start_city]
    visited = {start_city}
    current = start_city
    
    while len(tour) < len(cities):
        next_city = None
        for neighbor in graph[current]:
            if neighbor not in visited:
                next_city = neighbor
                break
        
        if next_city is None:
            for city in cities:
                if city not in visited:
                    tour.append(city)
                    visited.add(city)
            break
        
        tour.append(next_city)
        visited.add(next_city)
        current = next_city
    
    return tour


def generate_multiple_tours(cities: List[City], 
                           distance_matrix: DistanceMatrix,
                           num_tours: int = 10,
                           method: str = 'random') -> List[List[City]]:
    """
    Tạo nhiều tour khác nhau.
    
    Args:
        cities (List[City]): Danh sách các thành phố
        distance_matrix (DistanceMatrix): Ma trận khoảng cách
        num_tours (int): Số lượng tour cần tạo
        method (str): Phương pháp tạo tour ('random', 'nn', 'greedy')
        
    Returns:
        List[List[City]]: Danh sách các tour
    """
    tours = []
    
    for i in range(num_tours):
        if method == 'random':
            tour = random_tour(cities, seed=i)
        elif method == 'nn':
            start_city = cities[i % len(cities)]
            tour = nearest_neighbor_tour(cities, distance_matrix, start_city)
        elif method == 'greedy':
            tour = greedy_tour(cities, distance_matrix)
        else:
            tour = random_tour(cities, seed=i)
        
        tours.append(tour)
    
    return tours