# File: gui/solver_thread.py

import time
import traceback
from PyQt5.QtCore import QThread, pyqtSignal

# Import các thuật toán
from algorithms.hill_climbing_tsp import HillClimbingSolver
from algorithms.pso_tsp import PSOSolver
from models.tour import Tour

class SolverThread(QThread):
    """
    Luồng xử lý chạy thuật toán trong nền (Background Thread).
    Giúp giao diện không bị treo (not responding) khi thuật toán tính toán.
    """
    
    # Tín hiệu gửi kết quả về GUI khi chạy xong:
    # - object: Best Tour (đối tượng Tour)
    # - list: History (danh sách quãng đường qua các vòng lặp)
    # - list: Solution Log (danh sách các bước cải thiện: [(step, dist, detail), ...])
    # - float: Elapsed Time (thời gian chạy tính bằng giây)
    result_signal = pyqtSignal(object, list, list, float)
    
    # Tín hiệu gửi log text về GUI (để hiện dòng chữ đang chạy...)
    log_signal = pyqtSignal(str)

    def __init__(self, algo_name, params, cities, distance_matrix):
        super().__init__()
        self.algo_name = algo_name
        self.params = params
        self.cities = cities
        self.distance_matrix = distance_matrix

    def run(self):
        self.log_signal.emit(f"⏳ [THREAD] Đang khởi tạo {self.algo_name}...")
        
        start_time = time.perf_counter()
        best_tour = None
        history = []
        solution_log = []
        
        try:
            # --- TRƯỜNG HỢP 1: HILL CLIMBING ---
            if "Hill" in self.algo_name:
                solver = HillClimbingSolver(self.cities, self.distance_matrix)
                
                # Lấy tham số từ dictionary (với giá trị mặc định an toàn)
                method = self.params.get('initial_method', 'random')
                seed = self.params.get('seed', 42)
                no_improve = self.params.get('max_no_improve', 100)
                start_city_id = self.params.get('start_city_id', None) # Tham số mới
                
                # Chạy thuật toán (Hàm run của HC đã được sửa để trả về 4 giá trị)
                #
                best_tour, history, solution_log, _ = solver.run(
                    initial_method=method, 
                    start_city_id=start_city_id,
                    seed=seed, 
                    max_no_improve=no_improve
                )

            # --- TRƯỜNG HỢP 2: PSO (PARTICLE SWARM OPTIMIZATION) ---
            elif "PSO" in self.algo_name:
                # Lấy tham số PSO
                swarm_size = self.params.get('swarm_size', 30)
                iterations = self.params.get('num_iterations', 100)
                w = self.params.get('w', 0.7)
                c1 = self.params.get('c1', 1.5)
                c2 = self.params.get('c2', 1.5)
                
                solver = PSOSolver(self.cities, self.distance_matrix, 
                                   swarm_size, iterations, w, c1, c2)
                
                # PSO trả về 3 giá trị: tour, distance, history (list float)
                #
                best_tour, best_dist, history = solver.solve()
                
                # --- TẠO SOLUTION LOG GIẢ LẬP CHO PSO ---
                # Vì PSO hiện tại chưa trả về log chi tiết từng bước hoán vị,
                # ta tạo một log tóm tắt dựa trên history để hiển thị lên bảng GUI.
                solution_log = []
                if history:
                    current_best = history[0]
                    solution_log.append((0, current_best, "Khởi tạo bầy đàn"))
                    
                    for i, dist in enumerate(history):
                        # Chỉ ghi lại những lần có sự cải thiện
                        if dist < current_best:
                            current_best = dist
                            solution_log.append((i, dist, "Cập nhật gBest mới"))
            
            # --- KẾT THÚC ---
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            # Gửi toàn bộ dữ liệu về Main Window
            self.result_signal.emit(best_tour, history, solution_log, elapsed_time)
            
        except Exception as e:
            # Bắt lỗi nếu có gì đó sai sót trong thuật toán để không crash app
            error_msg = f"LỖI THUẬT TOÁN: {str(e)}"
            self.log_signal.emit(error_msg)
            print(traceback.format_exc()) # In chi tiết lỗi ra terminal để debug