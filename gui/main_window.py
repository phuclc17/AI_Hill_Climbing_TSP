# File: gui/main_window.py
# (Phiên bản đầy đủ, đã sửa lỗi SyntaxError, NameError và RuntimeError)

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QTextEdit, QLabel, QGroupBox, 
                             QFormLayout, QComboBox, QSpinBox, 
                             QDoubleSpinBox, QPushButton, QSplitter,
                             QStackedWidget, QMessageBox) # Đã import đầy đủ
from PyQt5.QtCore import Qt, pyqtSignal

# Import Matplotlib (để vẽ biểu đồ)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Import các file logic
#
from utils.data_loader import DataLoader
from utils.distance_matrix import DistanceMatrix
from models.city import City
from models.tour import Tour

# --- Lớp PlotCanvas (trước đây là plot_widgets.py) ---
# (Đã sửa lại logic vẽ để fix RuntimeError)
class PlotCanvas(QWidget):
    """
    Widget tùy chỉnh để nhúng Matplotlib vào PyQt5.
    Giờ nó sẽ tạo và giữ 'axes' (trục vẽ) của riêng mình.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Tạo ra một 'axes' (trục vẽ) ngay từ đầu
        self.axes = self.figure.add_subplot(111) 
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def clear_plot(self):
        """Xóa sạch nội dung của trục vẽ."""
        self.axes.clear()
        self.canvas.draw()

# --- Lớp CurrentRunTab (trước đây là tabs/current_run_tab.py) ---
# (Đã sửa lại logic vẽ để fix RuntimeError)
class CurrentRunTab(QWidget):
    """
    Tab hiển thị 2 biểu đồ của lần chạy hiện tại.
    Giờ nó sẽ nhận DỮ LIỆU và tự vẽ.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        
        self.map_canvas = PlotCanvas(self)
        self.convergence_canvas = PlotCanvas(self)

        splitter.addWidget(self.map_canvas)
        splitter.addWidget(self.convergence_canvas)
        splitter.setSizes([600, 400])
        main_layout.addWidget(splitter)
        
        self.clear_plots() # Xóa placeholder
        
    def update_map(self, cities: list, tour: Tour | None):
        """
        Hàm này nhận DỮ LIỆU (cities, tour) và tự vẽ.
        """
        ax = self.map_canvas.axes # Lấy trục vẽ
        ax.clear()
        
        # Vẽ tất cả các thành phố (dưới dạng điểm)
        all_x = [c.x for c in cities]
        all_y = [c.y for c in cities]
        ax.plot(all_x, all_y, 'bo', label='Thành phố', markersize=5)
        
        # Vẽ đường đi (tour)
        if tour:
            # Lấy danh sách tọa độ theo đúng thứ tự tour
            tour_cities = tour.cities
            tour_x = [c.x for c in tour_cities] + [tour_cities[0].x] # Nối về điểm đầu
            tour_y = [c.y for c in tour_cities] + [tour_cities[0].y]
            
            ax.plot(tour_x, tour_y, 'r-', label=f'Đường đi ({tour.distance:.2f} km)')
            
            # Thêm tên thành phố
            for city in tour_cities:
                if hasattr(city, 'name'):
                    ax.text(city.x, city.y, f' {city.name}', fontsize=8)
                
        ax.set_title("Bản đồ Đường đi")
        ax.set_xlabel("Longitude (X)")
        ax.set_ylabel("Latitude (Y)")
        ax.legend()
        ax.grid(True)
        self.map_canvas.canvas.draw()
        
    def update_convergence(self, history: list):
        """
        Hàm này nhận DỮ LIỆU (history) và tự vẽ.
        """
        ax = self.convergence_canvas.axes # Lấy trục vẽ
        ax.clear()
        
        if history:
            ax.plot(history, 'b-')
        
        ax.set_title("Biểu đồ Hội tụ")
        ax.set_xlabel("Vòng lặp (Iteration / Restart)")
        ax.set_ylabel("Quãng đường Tốt nhất (km)")
        ax.grid(True)
        self.convergence_canvas.canvas.draw()

    def clear_plots(self):
        self.map_canvas.clear_plot()
        self.convergence_canvas.clear_plot()

# --- Cửa sổ chính (MainWindow) ---
class MainWindow(QMainWindow):
    """
    Cửa sổ chính của ứng dụng.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP AI Solver (Hill Climbing vs PSO)")
        self.setGeometry(100, 100, 1400, 800)
        
        # Biến trạng thái
        self.cities: List[City] = []
        self.distance_matrix: DistanceMatrix | None = None
        
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        left_panel_widget = self._create_left_panel()
        left_panel_widget.setMaximumWidth(400)
        
        right_widget = self._create_right_panel()

        main_layout.addWidget(left_panel_widget)
        main_layout.addWidget(right_widget, stretch=1)

    def _create_left_panel(self) -> QWidget:
        left_panel_widget = QWidget()
        left_layout = QVBoxLayout(left_panel_widget)

        # --- Panel Input ---
        input_group = QGroupBox("1. Tải Dữ Liệu")
        input_layout = QVBoxLayout(input_group)
        self.load_button = QPushButton("Tải data_cities.json")
        input_layout.addWidget(self.load_button)
        
        # --- Panel Algorithm ---
        algo_group = QGroupBox("2. Chọn Thuật Toán")
        algo_layout = QFormLayout(algo_group)
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Hill Climbing", "PSO"])
        algo_layout.addRow("Thuật toán:", self.algo_combo)

        # --- Panel Parameter ---
        param_group = QGroupBox("3. Tham Số Thuật Toán")
        param_layout = QVBoxLayout(param_group)
        self.param_stack = QStackedWidget()
        self.hc_param_widget = self._create_hc_panel()
        self.pso_param_widget = self._create_pso_panel()
        self.param_stack.addWidget(self.hc_param_widget) # Index 0
        self.param_stack.addWidget(self.pso_param_widget) # Index 1
        param_layout.addWidget(self.param_stack)

        # --- Panel Control ---
        control_group = QGroupBox("4. Chạy/Dừng")
        control_layout = QVBoxLayout(control_group)
        self.run_button = QPushButton("BẮT ĐẦU CHẠY")
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.stop_button = QPushButton("DỪNG")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white;")
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.run_button)
        control_layout.addWidget(self.stop_button)

        left_layout.addWidget(input_group)
        left_layout.addWidget(algo_group)
        left_layout.addWidget(param_group)
        left_layout.addWidget(control_group)
        left_layout.addStretch(1) 
        
        return left_panel_widget

    def _create_right_panel(self) -> QWidget:
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.tab_widget = QTabWidget()
        self.current_run_tab = CurrentRunTab()
        # self.comparison_tab = QWidget() # Placeholder
        # self.history_tab = QWidget()    # Placeholder
        
        self.tab_widget.addTab(self.current_run_tab, "Lần chạy hiện tại")
        
        log_layout = QVBoxLayout()
        log_layout.addWidget(QLabel("Nhật ký (Log):"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        right_layout.addWidget(self.tab_widget, stretch=3) 
        right_layout.addLayout(log_layout, stretch=1)
        
        return right_widget

    def _create_hc_panel(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        self.hc_method_combo = QComboBox()
        self.hc_method_combo.addItems(["nn", "random"])
        self.hc_seed_spinbox = QSpinBox()
        self.hc_seed_spinbox.setRange(0, 99999); self.hc_seed_spinbox.setValue(42)
        self.hc_no_improve_spinbox = QSpinBox()
        self.hc_no_improve_spinbox.setRange(10, 100000); self.hc_no_improve_spinbox.setValue(100)
        
        layout.addRow("Tour ban đầu:", self.hc_method_combo)
        layout.addRow("Random Seed:", self.hc_seed_spinbox)
        layout.addRow("Max No Improve:", self.hc_no_improve_spinbox)
        return widget

    def _create_pso_panel(self) -> QWidget:
        widget = QWidget()
        layout = QFormLayout(widget)
        self.pso_swarm_spinbox = QSpinBox()
        self.pso_swarm_spinbox.setRange(10, 1000); self.pso_swarm_spinbox.setValue(30)
        self.pso_iter_spinbox = QSpinBox()
        self.pso_iter_spinbox.setRange(10, 10000); self.pso_iter_spinbox.setValue(100)
        self.pso_w_spinbox = QDoubleSpinBox()
        self.pso_w_spinbox.setRange(0.1, 1.0); self.pso_w_spinbox.setValue(0.7); self.pso_w_spinbox.setSingleStep(0.1)
        self.pso_c1_spinbox = QDoubleSpinBox()
        self.pso_c1_spinbox.setRange(0.1, 3.0); self.pso_c1_spinbox.setValue(1.5); self.pso_c1_spinbox.setSingleStep(0.1)
        self.pso_c2_spinbox = QDoubleSpinBox()
        self.pso_c2_spinbox.setRange(0.1, 3.0); self.pso_c2_spinbox.setValue(1.5); self.pso_c2_spinbox.setSingleStep(0.1)

        layout.addRow("Số hạt:", self.pso_swarm_spinbox)
        layout.addRow("Số vòng lặp:", self.pso_iter_spinbox)
        layout.addRow("W (Quán tính):", self.pso_w_spinbox)
        layout.addRow("C1 (Nhận thức):", self.pso_c1_spinbox)
        layout.addRow("C2 (Xã hội):", self.pso_c2_spinbox)
        return widget

    def _connect_signals(self):
        self.load_button.clicked.connect(self.on_load_data)
        self.algo_combo.currentIndexChanged.connect(self.param_stack.setCurrentIndex)
        self.run_button.clicked.connect(self.on_run)

    def log(self, message: str):
        self.log_text.append(message)
        print(message) 

    def on_load_data(self):
        filepath = "data/data_cities.json" #
        self.log(f"Đang tải dữ liệu từ '{filepath}'...")
        try:
            #
            self.cities = DataLoader.load_cities_from_json(filepath)
            if not self.cities:
                raise FileNotFoundError("Không tìm thấy 'locations' trong file.")
            
            #
            self.distance_matrix = DistanceMatrix(self.cities) 
            self.log(f"Tải thành công {len(self.cities)} thành phố.")
            self.log(f"Thành phố đầu tiên: {self.cities[0].name}") #
            
            # Tải xong, vẽ các thành phố lên bản đồ
            self.current_run_tab.update_map(self.cities, None)
            
        except Exception as e:
            self.log(f"LỖI: {e}")
            QMessageBox.critical(self, "Lỗi Tải Dữ Liệu", str(e))

    def on_run(self):
        if not self.cities:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng 'Tải data_cities.json' trước.")
            return
            
        algo_name = self.algo_combo.currentText()
        
        # --- ĐÃ SỬA LỖI SYNTAXERROR TẠI ĐÂY ---
        params = {}
        if "PSO" in algo_name:
            params = {
                'swarm_size': self.pso_swarm_spinbox.value(),
                'num_iterations': self.pso_iter_spinbox.value(),
                'w': self.pso_w_spinbox.value(),
                'c1': self.pso_c1_spinbox.value(),
                'c2': self.pso_c2_spinbox.value(),
            }
        else: # Hill Climbing
            params = {
                'initial_method': self.hc_method_combo.currentText(),
                'seed': self.hc_seed_spinbox.value(),
                'max_no_improve': self.hc_no_improve_spinbox.value(),
            }
        # --- HẾT PHẦN SỬA LỖI ---
        
        self.log("="*30)
        self.log(f"BẮT ĐẦU CHẠY: {algo_name}")
        self.log(f"Tham số: {params}")
        
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.load_button.setEnabled(False)

        # TODO: Khởi tạo và chạy SolverThread
        self.log("... Thuật toán đang chạy (Giả lập) ...")
        
        # --- Giả lập kết quả để test GUI ---
        
        # 1. Giả lập kết quả DATA (không phải Figure)
        #
        # (Sử dụng tour_generator.py để tạo tour ngẫu nhiên)
        from utils.tour_generator import random_tour
        random_cities = random_tour(self.cities)
        fake_tour = Tour(random_cities, self.distance_matrix) 
        fake_history = [fake_tour.distance, fake_tour.distance-50, fake_tour.distance-120]
        
        # 2. Cập nhật GUI (Truyền data, không truyền figure)
        self.current_run_tab.update_map(self.cities, fake_tour) 
        self.current_run_tab.update_convergence(fake_history)
        
        # --- Hết Giả lập ---
        
        self.log("--- HOÀN THÀNH (GIẢ LẬP) ---")
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.load_button.setEnabled(True)