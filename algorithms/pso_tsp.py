import random
import copy 

from models.tour import Tour 
from algorithms.base_tsp_solver import BaseTspSolver

class Particle:
    def __init__(self, initial_tour: Tour):
        self.current_tour = initial_tour
        self.current_distance = self.current_tour.distance
        
        # pbest: Vị trí cá nhân tốt nhất
        self.pbest_tour = self.current_tour.copy()
        self.pbest_distance = self.current_distance
        
        # velocity: Vận tốc (danh sách các phép hoán vị)
        self.velocity = []

    def update_pbest(self):
        self.current_distance = self.current_tour.distance
        if self.current_distance < self.pbest_distance:
            self.pbest_distance = self.current_distance
            self.pbest_tour = self.current_tour.copy()

class PSOSolver(BaseTspSolver): 
    def __init__(self, cities, distance_matrix, swarm_size, num_iterations, w, c1, c2):
        # Gọi __init__ của lớp cha
        super().__init__(cities, distance_matrix)
        
        # Các thuộc tính riêng của PSO
        self.swarm_size = swarm_size
        self.num_iterations = num_iterations
        self.w = w   # Quán tính
        self.c1 = c1 # Nhận thức (pbest)
        self.c2 = c2 # Xã hội (gbest)
        
        self.swarm = []

        print("--- Khởi tạo PSOSolver ---")
        print(f"Tham số: w={w}, c1={c1}, c2={c2}")

    def _create_random_tour(self) -> Tour:
        cities_copy = list(self.all_cities)
        random.shuffle(cities_copy)
        return Tour(cities_copy, self.distance_matrix)

    def _initialize_swarm(self):
        print("Đang khởi tạo bầy đàn...")
        self.swarm = []
        for _ in range(self.swarm_size):
            random_tour = self._create_random_tour()
            particle = Particle(random_tour)
            self.swarm.append(particle)
            
            if particle.pbest_distance < self.best_distance:
                self.best_distance = particle.pbest_distance
                self.best_tour = particle.pbest_tour.copy()
        
        print(f"Khởi tạo hoàn tất. gbest ban đầu: {self.best_distance:.2f}")

    def _find_swaps(self, tour_a: Tour, tour_b: Tour):
        # Phép "trừ" (velocity = tour_b - tour_a)
        swaps = []
        temp_cities = list(tour_a.cities)
        target_cities = tour_b.cities
        
        city_to_index_map = {city: i for i, city in enumerate(temp_cities)}

        for i in range(self.num_cities):
            if temp_cities[i].id != target_cities[i].id:
                city_should_be_here = target_cities[i]
                current_index_of_target = city_to_index_map[city_should_be_here]
                city_at_i = temp_cities[i]

                temp_cities[i], temp_cities[current_index_of_target] = temp_cities[current_index_of_target], temp_cities[i]
                
                city_to_index_map[city_at_i] = current_index_of_target
                city_to_index_map[city_should_be_here] = i
                
                swaps.append((i, current_index_of_target))
                
        return swaps

    def _apply_swaps(self, tour: Tour, swaps) -> Tour:
        # Phép "cộng" (new_tour = tour + velocity)
        new_cities = list(tour.cities)
        for i, j in swaps:
            if 0 <= i < len(new_cities) and 0 <= j < len(new_cities):
                new_cities[i], new_cities[j] = new_cities[j], new_cities[i]
            else:
                print(f"Cảnh báo: Phép hoán vị không hợp lệ ({i}, {j})")
                
        return Tour(new_cities, self.distance_matrix)

    def _sample_swaps(self, swaps, probability_factor):
        # Nhân vận tốc với hệ số (w, c1*r1, c2*r2)
        if not swaps:
            return []
        
        k = int(len(swaps) * probability_factor)
        k = max(0, min(k, len(swaps))) 
        
        return random.sample(swaps, k)

    def solve(self, **kwargs):
        if not self.all_cities:
            print("Lỗi: Chưa có thành phố nào.")
            return None, 0, [] 

        self._initialize_swarm()
        
        print("\nBắt đầu quá trình tối ưu...")
        convergence_history = [self.best_distance]

        for i in range(self.num_iterations):
            
            # Cập nhật gbest (best_tour)
            best_particle_in_iteration = min(self.swarm, key=lambda p: p.current_distance)
            if best_particle_in_iteration.current_distance < self.best_distance:
                self.best_distance = best_particle_in_iteration.current_distance
                self.best_tour = best_particle_in_iteration.current_tour.copy()

            for particle in self.swarm:
                
                # --- Công thức cập nhật PSO ---
                # v(t+1) = w*v(t) + c1*r1*(pbest - x(t)) + c2*r2*(gbest - x(t))
                
                inertia_swaps = self._sample_swaps(particle.velocity, self.w)
                
                r1 = random.random()
                pbest_diff_swaps = self._find_swaps(particle.current_tour, particle.pbest_tour)
                cognitive_swaps = self._sample_swaps(pbest_diff_swaps, self.c1 * r1)

                r2 = random.random()
                gbest_diff_swaps = self._find_swaps(particle.current_tour, self.best_tour)
                social_swaps = self._sample_swaps(gbest_diff_swaps, self.c2 * r2)

                # Vận tốc mới v(t+1)
                particle.velocity = inertia_swaps + cognitive_swaps + social_swaps

                # Vị trí mới x(t+1) = x(t) + v(t+1)
                particle.current_tour = self._apply_swaps(particle.current_tour, particle.velocity)
                
                particle.update_pbest()

            convergence_history.append(self.best_distance)
            
            if (i + 1) % 10 == 0:
                print(f"Vòng {i+1}/{self.num_iterations} - gbest: {self.best_distance:.2f}")
        
        print("\n--- Tối ưu hoàn tất! ---")
        if self.best_tour:
            print(f"Quãng đường ngắn nhất (gbest): {self.best_distance:.2f}")
            print(f"Chu trình tốt nhất (id): {[city.id for city in self.best_tour.cities]}")
        else:
            print("Không tìm thấy chu trình tốt nhất.")
            
        return self.best_tour, self.best_distance, convergence_history