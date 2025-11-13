
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.city import City
    from utils.distance_matrix import DistanceMatrix 


class Tour:
    """
    Đại diện cho một giải pháp (một đường đi) hoàn chỉnh trong bài toán TSP.
    (Giữ nguyên logic cốt lõi của bạn)
    """
    
    def __init__(self, cities: List['City'], distance_matrix: 'DistanceMatrix'):
        """
        Khởi tạo một Tour. (Giữ nguyên)
        """
        self.cities: List['City'] = cities[:]
        self.distance_matrix: 'DistanceMatrix' = distance_matrix
        self.distance: float = self._calculate_total_distance()

    def _calculate_total_distance(self) -> float:
        """
        Hàm nội bộ để tính tổng quãng đường của tour. (Giữ nguyên)
        """
        if not self.cities:
            return 0.0

        total_distance = 0.0
        num_cities = len(self.cities)

        for i in range(num_cities):
            city_a = self.cities[i]
            city_b = self.cities[i - 1] if i > 0 else self.cities[-1]
            total_distance += self.distance_matrix.get_distance(city_a.id, city_b.id)
            
        return total_distance

    def copy(self) -> 'Tour':
        """
        Tạo và trả về một bản sao (copy) của đối tượng Tour này. (Giữ nguyên)
        """
        new_tour = Tour(self.cities, self.distance_matrix)
        new_tour.distance = self.distance 
        return new_tour

    def __len__(self) -> int:
        """Trả về số lượng thành phố trong tour. (Giữ nguyên)"""
        return len(self.cities)

    def __getitem__(self, index: int) -> 'City':
        """Cho phép truy cập thành phố bằng chỉ số. (Giữ nguyên)"""
        return self.cities[index]

    def __repr__(self) -> str:
        """
        *** HÀM ĐÃ ĐƯỢC CẢI THIỆN ***
        Trả về một biểu diễn chuỗi của Tour, hiển thị TÊN thành phố.
        """
        # Kiểm tra xem city có thuộc tính 'name' không, nếu không thì dùng 'id'
        def get_city_display(city):
            if hasattr(city, 'name') and city.name:
                return city.name
            return str(city.id)

        # Hiển thị 5 thành phố đầu tiên để dễ debug
        path_preview = " -> ".join(get_city_display(city) for city in self.cities[:5])
        if len(self.cities) > 5:
            path_preview += "..."
            
        return f"Tour(distance={self.distance:.2f}, path=[{path_preview}])"