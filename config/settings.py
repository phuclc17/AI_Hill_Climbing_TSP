# File: config/settings.py

import os

# --- Đường dẫn (Paths) ---
# Lấy thư mục gốc của dự án (ví dụ: '.../HILL_CLIMBING_TSP/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đường dẫn đến file dữ liệu (dựa trên data_cities.json)
DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "data_cities.json")

# Đường dẫn đến file lưu lịch sử (dùng cho run_history.py)
HISTORY_FILE_PATH = os.path.join(BASE_DIR, "comparison", "run_history.json")


# --- Tham số HC (Defaults) ---
# Dựa trên các tham số trong hill_climbing_tsp.py
HC_DEFAULT_METHOD = 'nn'
HC_DEFAULT_SEED = 42
HC_DEFAULT_MAX_NO_IMPROVE = 100


# --- Tham số PSO (Defaults) ---
# Dựa trên các tham số trong pso_tsp.py
PSO_DEFAULT_SWARM_SIZE = 30
PSO_DEFAULT_ITERATIONS = 100
PSO_DEFAULT_W = 0.7
PSO_DEFAULT_C1 = 1.5
PSO_DEFAULT_C2 = 1.5