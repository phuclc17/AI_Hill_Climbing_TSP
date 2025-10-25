# File: models/tour.py

from typing import List, TYPE_CHECKING

# Sử dụng TYPE_CHECKING để tránh lỗi import vòng (circular import)
# nếu DistanceMatrix cũng import City hoặc Tour
if TYPE_CHECKING:
    from models.city import City
    from utils.distance_matrix import DistanceMatrix


class Tour:
    """
    Đại diện cho một giải pháp (một đường đi) hoàn chỉnh trong bài toán TSP.
    
    Lớp này lưu trữ một thứ tự các thành phố và tự động tính toán 
    tổng quãng đường của nó bằng cách sử dụng một DistanceMatrix đã được 
    tính toán trước để đảm bảo hiệu suất cao.
    """
    
    def __init__(self, cities: List['City'], distance_matrix: 'DistanceMatrix'):
        """
        Khởi tạo một Tour.

        Args:
            cities (List[City]): Một danh sách các đối tượng City theo đúng
                                 thứ tự của đường đi.
            distance_matrix (DistanceMatrix): Một đối tượng đã tính toán
                                              trước tất cả các khoảng cách.
        """
        # Tạo một bản sao nông của danh sách để tránh thay đổi 
        # danh sách gốc khi Tour này bị thay đổi (ví dụ: 2-opt)
        self.cities: List['City'] = cities[:]
        
        self.distance_matrix: 'DistanceMatrix' = distance_matrix
        
        # Tự động tính toán và lưu trữ quãng đường khi khởi tạo
        self.distance: float = self._calculate_total_distance()

    def _calculate_total_distance(self) -> float:
        """
        Hàm nội bộ để tính tổng quãng đường của tour.
        Sử dụng DistanceMatrix để tra cứu O(1) thay vì tính toán lại.
        
        Returns:
            float: Tổng quãng đường của tour.
        """
        if not self.cities:
            return 0.0

        total_distance = 0.0
        num_cities = len(self.cities)

        for i in range(num_cities):
            # Lấy thành phố hiện tại
            city_a = self.cities[i]
            
            # Lấy thành phố tiếp theo (hoặc thành phố đầu tiên nếu là thành phố cuối)
            city_b = self.cities[i - 1] if i > 0 else self.cities[-1]
            
            # Tra cứu khoảng cách từ matrix (nhanh hơn nhiều so với tính sqrt)
            total_distance += self.distance_matrix.get_distance(city_a.id, city_b.id)
            
        return total_distance

    def copy(self) -> 'Tour':
        """
        Tạo và trả về một bản sao (copy) của đối tượng Tour này.
        
        Đây là hàm cực kỳ quan trọng cho các thuật toán tìm kiếm 
        (như HC, PSO) để khám phá các giải pháp mới mà không
        làm hỏng giải pháp hiện tại.

        Returns:
            Tour: Một đối tượng Tour mới có cùng thứ tự thành phố 
                  và cùng tham chiếu đến distance_matrix.
        """
        # Chúng ta chỉ cần sao chép nông danh sách `cities`, 
        # vì bản thân các đối tượng City không thay đổi.
        # `distance_matrix` được chia sẻ, không cần sao chép.
        new_tour = Tour(self.cities, self.distance_matrix)
        
        # Tối ưu: Không cần tính toán lại quãng đường nếu đã biết
        new_tour.distance = self.distance 
        
        return new_tour

    def __len__(self) -> int:
        """Trả về số lượng thành phố trong tour."""
        return len(self.cities)

    def __getitem__(self, index: int) -> 'City':
        """Cho phép truy cập thành phố bằng chỉ số (ví dụ: tour[0])."""
        return self.cities[index]

    def __repr__(self) -> str:
        """Trả về một biểu diễn chuỗi của Tour."""
        # Hiển thị 5 thành phố đầu tiên để dễ debug
        path_preview = " -> ".join(str(city.id) for city in self.cities[:5])
        if len(self.cities) > 5:
            path_preview += "..."
            
        return f"Tour(cities={path_preview}, distance={self.distance:.2f})"