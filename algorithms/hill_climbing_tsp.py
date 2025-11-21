

import time
import random
from models.tour import Tour
from utils.tour_generator import random_tour, nearest_neighbor_tour

def two_opt_swap(cities, i, k):
    """Thực hiện đảo ngược đoạn từ i đến k."""
    new = cities[:i] + list(reversed(cities[i:k + 1])) + cities[k + 1:]
    return new

class HillClimbingSolver:
    def __init__(self, cities, distance_matrix):
        self.cities = cities
        self.distance_matrix = distance_matrix

    def _rotate_to_start(self, tour_cities, start_id):
        """
        Xoay danh sách thành phố sao cho thành phố có start_id nằm đầu tiên.
        """
        if start_id is None:
            return tour_cities
        try:
            # Tìm vị trí của start_id
            idx = next(i for i, c in enumerate(tour_cities) if c.id == start_id)
        except StopIteration:
            return tour_cities

        if idx == 0:
            return tour_cities 
        return tour_cities[idx:] + tour_cities[:idx]

    def run(self, initial_method='random', start_city_id=None, seed=None, max_no_improve=100):
        if seed is not None:
            random.seed(seed)

        # 1. Tạo Tour ban đầu
        if initial_method == 'nn':
            start_node = next((c for c in self.cities if c.id == start_city_id), None)
            current_cities = nearest_neighbor_tour(self.cities, self.distance_matrix, start_node)
        else:
            current_cities = random_tour(self.cities, seed)

        # Xoay ngay từ đầu để đảm bảo điểm xuất phát đúng
        current_cities = self._rotate_to_start(current_cities, start_city_id)

        current_tour = Tour(current_cities, self.distance_matrix)
        best_tour = current_tour
        
        history = [current_tour.distance]
        solution_log = []
        
        # Ghi log trạng thái đầu tiên (Format giống hình mẫu)
        path_str = " -> ".join([c.name for c in current_tour.cities]) + f" -> {current_tour.cities[0].name}"
        solution_log.append((0, current_tour.distance, f"Tour: {path_str}"))

        n = len(current_tour.cities)
        no_improve = 0
        step = 0
        
        start_time = time.time()

        while no_improve < max_no_improve:
            improved = False
            step += 1
            
            # Thuật toán 2-opt
            for i in range(0, n - 1):
                for k in range(i + 1, n):
                    new_cities = two_opt_swap(current_tour.cities, i, k)
                    new_tour = Tour(new_cities, self.distance_matrix)
                    
                    if new_tour.distance < best_tour.distance:
                        # --- TÌM THẤY ĐƯỜNG TỐT HƠN ---
                        
                        # 1. Xoay lại ngay để điểm xuất phát luôn cố định
                        fixed_cities = self._rotate_to_start(new_cities, start_city_id)
                        best_tour = Tour(fixed_cities, self.distance_matrix)
                        
                        current_tour = best_tour
                        improved = True
                        no_improve = 0
                        
                        path_names = [c.name for c in best_tour.cities]
                        path_names.append(path_names[0]) # Quay về điểm đầu
                        path_str = " -> ".join(path_names)
                        
                        # Ghi vào log (Chỉ ghi khi Cải Thiện)
                        solution_log.append((step, best_tour.distance, f"Tour: {path_str}"))
                        break 
                
                if improved:
                    break

            history.append(best_tour.distance)

            if not improved:
                no_improve += 1
                # Không ghi log thất bại nữa (để giống mẫu sạch sẽ)

        elapsed = time.time() - start_time
        
        return best_tour, history, solution_log, elapsed