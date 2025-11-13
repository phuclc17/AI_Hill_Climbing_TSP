import abc
from typing import List

from models.city import City
from models.tour import Tour
from utils.distance_matrix import DistanceMatrix

class BaseTspSolver(abc.ABC):
    """
    Lớp cơ sở trừu tượng (Abstract Base Class) cho tất cả các thuật toán giải TSP.
    Định nghĩa cấu trúc chung mà tất cả các solver phải tuân theo.
    """
    
    def __init__(self, cities: List[City], distance_matrix: DistanceMatrix):
        """
        Khởi tạo solver với dữ liệu cơ bản.

        Args:
            cities (List[City]): Danh sách tất cả các đối tượng City.
            distance_matrix (DistanceMatrix): Ma trận khoảng cách đã tính.
        """
        self.all_cities = cities
        self.distance_matrix = distance_matrix
        self.num_cities = len(cities)
        
        # Tất cả các solver đều sẽ tìm ra một 'best_tour'
        self.best_tour: Tour | None = None
        self.best_distance: float = float('inf')
        
    @abc.abstractmethod
    def solve(self, **kwargs):
        """
        Phương thức trừu tượng, các lớp con (HC, PSO) BẮT BUỘC
        phải định nghĩa phương thức này.
        
        Nó phải trả về một tuple: (best_tour, best_distance, history)
        """
        raise NotImplementedError
        
    def __repr__(self) -> str:
        # Trả về tên của lớp con (ví dụ: "PSOSolver")
        return self. __class__.__name__