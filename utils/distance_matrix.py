import math
from typing import List
from models.city import City


class DistanceMatrix:
  
    
    def __init__(self, cities: List[City]):
        """
        Khởi tạo ma trận khoảng cách từ danh sách thành phố.
        
        Args:
            cities (List[City]): Danh sách các đối tượng City
        """
        self.cities = cities
        self.num_cities = len(cities)
        self._matrix = {}
        self._build_matrix()
    
    def _build_matrix(self):
        """
        Xây dựng ma trận khoảng cách giữa tất cả các cặp thành phố.
        Sử dụng dictionary để lưu trữ với key là tuple (id1, id2).
        """
        for i in range(self.num_cities):
            for j in range(i, self.num_cities):
                city_a = self.cities[i]
                city_b = self.cities[j]
                
                if i == j:
                    distance = 0.0
                else:
                    distance = self._calculate_distance(city_a, city_b)
                
                self._matrix[(city_a.id, city_b.id)] = distance
                self._matrix[(city_b.id, city_a.id)] = distance
    
    @staticmethod
    def _calculate_distance(city_a: City, city_b: City) -> float:
     
        lat1 = math.radians(city_a.y)
        lon1 = math.radians(city_a.x)
        lat2 = math.radians(city_b.y)
        lon2 = math.radians(city_b.x)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
  
        earth_radius = 6371.0
        
        return earth_radius * c
    
    def get_distance(self, city_id_a: int, city_id_b: int) -> float:
        """
        Lấy khoảng cách giữa hai thành phố dựa trên ID.
        
        Args:
            city_id_a (int): ID của thành phố thứ nhất
            city_id_b (int): ID của thành phố thứ hai
            
        Returns:
            float: Khoảng cách giữa hai thành phố
        """
        return self._matrix.get((city_id_a, city_id_b), float('inf'))
    
    def get_nearest_city(self, from_city_id: int, unvisited_ids: set) -> int:
        """
        Tìm thành phố gần nhất trong tập các thành phố chưa thăm.
        
        Args:
            from_city_id (int): ID của thành phố xuất phát
            unvisited_ids (set): Tập các ID thành phố chưa thăm
            
        Returns:
            int: ID của thành phố gần nhất
        """
        min_distance = float('inf')
        nearest_id = None
        
        for city_id in unvisited_ids:
            distance = self.get_distance(from_city_id, city_id)
            if distance < min_distance:
                min_distance = distance
                nearest_id = city_id
        
        return nearest_id
    
    def __repr__(self) -> str:
        return f"DistanceMatrix(num_cities={self.num_cities})"