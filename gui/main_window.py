# File: gui/main_window.py

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QTextEdit, QLabel, QGroupBox, 
                             QFormLayout, QComboBox, QSpinBox, 
                             QDoubleSpinBox, QPushButton, QSplitter,
                             QStackedWidget, QMessageBox, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QSlider)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from utils.data_loader import DataLoader
from utils.distance_matrix import DistanceMatrix
from models.city import City
from models.tour import Tour
from gui.solver_thread import SolverThread

# --- DARK THEME STYLESHEET ---
DARK_STYLESHEET = """
QMainWindow { background-color: #1e1e2e; color: #cdd6f4; }
QWidget { color: #cdd6f4; }
QGroupBox { font-weight: bold; border: 1px solid #313244; border-radius: 6px; margin-top: 12px; padding-top: 10px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; color: #89b4fa; }
QPushButton { background-color: #313244; border: none; border-radius: 4px; padding: 8px; color: #cdd6f4; font-weight: bold; }
QPushButton:hover { background-color: #45475a; }
QPushButton:pressed { background-color: #585b70; }
QPushButton#btn_run { background-color: #a6e3a1; color: #1e1e2e; }
QPushButton#btn_run:hover { background-color: #94e2d5; }
QPushButton:disabled { background-color: #45475a; color: #7f849c; }
QTabWidget::pane { border: 1px solid #313244; background: #1e1e2e; }
QTabBar::tab { background: #313244; color: #a6adc8; padding: 8px 16px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
QTabBar::tab:selected { background: #89b4fa; color: #1e1e2e; font-weight: bold; }
QTableWidget { background-color: #181825; gridline-color: #313244; color: #cdd6f4; border: none; }
QHeaderView::section { background-color: #313244; padding: 4px; border: none; color: #cdd6f4; }
QTextEdit { background-color: #181825; border: 1px solid #313244; color: #a6adc8; font-family: Consolas; }
QComboBox, QSpinBox, QDoubleSpinBox { background-color: #313244; border: 1px solid #45475a; padding: 4px; border-radius: 4px; color: #cdd6f4; }
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView { background-color: #1e1e2e; color: #cdd6f4; selection-background-color: #89b4fa; selection-color: #1e1e2e; border: 1px solid #45475a; }
QSlider::groove:horizontal { border: 1px solid #45475a; height: 8px; background: #313244; margin: 2px 0; border-radius: 4px; }
QSlider::handle:horizontal { background: #89b4fa; border: 1px solid #89b4fa; width: 18px; height: 18px; margin: -7px 0; border-radius: 9px; }
"""

class PlotCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#1e1e2e')
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    def clear_plot(self):
        self.axes.clear()
        self.axes.set_facecolor('#181825')
        self.canvas.draw()

class DashboardTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self.map_canvas = PlotCanvas(self)
        self.conv_canvas = PlotCanvas(self)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.map_canvas)
        splitter.addWidget(self.conv_canvas)
        splitter.setSizes([700, 500])
        layout.addWidget(splitter)

    def update_map(self, cities, tour):
        ax = self.map_canvas.axes
        ax.clear()
        ax.set_facecolor('#181825')
        x = [c.x for c in cities]
        y = [c.y for c in cities]
        ax.scatter(x, y, c='#89b4fa', s=60, zorder=3, label='Thành phố')
        for c in cities: ax.text(c.x, c.y, f"  {c.name}", color='#bac2de', fontsize=9)
        if tour:
            tx = [c.x for c in tour.cities] + [tour.cities[0].x]
            ty = [c.y for c in tour.cities] + [tour.cities[0].y]
            ax.plot(tx, ty, c='#f38ba8', linewidth=2, zorder=2, label=f'{tour.distance:.1f} km')
            start = tour.cities[0]
            ax.scatter([start.x], [start.y], c='#a6e3a1', s=150, marker='*', zorder=4, label='Bắt đầu')
        ax.set_title(f"Bản đồ Tour ({len(cities)} thành phố)", color='white', pad=10)
        ax.set_xlabel("Kinh độ", color='#a6adc8'); ax.set_ylabel("Vĩ độ", color='#a6adc8')
        ax.tick_params(colors='#a6adc8')
        for spine in ax.spines.values(): spine.set_edgecolor('#45475a')
        ax.grid(color='#313244', linestyle='--')
        ax.legend(facecolor='#1e1e2e', edgecolor='#45475a', labelcolor='#cdd6f4')
        self.map_canvas.canvas.draw()

    def update_conv(self, history):
        ax = self.conv_canvas.axes
        ax.clear()
        ax.set_facecolor('#181825')
        if history:
            ax.plot(history, c='#a6e3a1', linewidth=2)
            min_val = min(history)
            ax.set_title(f"Lịch sử Tối ưu hóa (Tốt nhất: {min_val:.2f} km)", color='white', pad=10)
        else: ax.set_title("Lịch sử Tối ưu hóa", color='white')
        ax.set_xlabel("Số lần lặp", color='#a6adc8'); ax.set_ylabel("Khoảng cách (km)", color='#a6adc8')
        ax.tick_params(colors='#a6adc8')
        for spine in ax.spines.values(): spine.set_edgecolor('#45475a')
        ax.grid(color='#313244', linestyle='--')
        self.conv_canvas.canvas.draw()

class ComparisonTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Thuật toán", "Khoảng cách (km)", "Thời gian (s)", "Số bước", "Đánh giá"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        btn_clear = QPushButton("Xóa bảng so sánh")
        btn_clear.clicked.connect(lambda: self.table.setRowCount(0))
        layout.addWidget(btn_clear)

    def add_result(self, algo_name, distance, time, iterations):
        row = self.table.rowCount()
        self.table.insertRow(row)
        def create_item(text):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            return item
        self.table.setItem(row, 0, create_item(algo_name))
        self.table.setItem(row, 1, create_item(f"{distance:.2f}"))
        self.table.setItem(row, 2, create_item(f"{time:.4f}"))
        self.table.setItem(row, 3, create_item(str(iterations)))
        stars = "⭐⭐⭐⭐⭐"
        if distance > 4000: stars = "⭐⭐⭐⭐"
        if distance > 6000: stars = "⭐⭐⭐"
        if distance > 8000: stars = "⭐⭐"
        self.table.setItem(row, 4, create_item(stars))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Solver Pro - Hill Climbing & PSO (Dynamic Data)")
        self.setGeometry(50, 50, 1400, 850)
        self.setStyleSheet(DARK_STYLESHEET)
        self.all_cities = []; self.cities = []; self.distance_matrix = None; self.solver_thread = None 
        self._init_ui()
        self.load_data_automatically()

    def _init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        layout = QHBoxLayout(main)

        # === SIDEBAR ===
        sidebar = QWidget()
        sidebar.setFixedWidth(320)
        side_layout = QVBoxLayout(sidebar)
        
        grp_data = QGroupBox("📍 DỮ LIỆU ĐẦU VÀO")
        l_data = QVBoxLayout(grp_data)
        self.lbl_city_count = QLabel("Đang tải...")
        l_data.addWidget(self.lbl_city_count)
        self.slider_cities = QSlider(Qt.Horizontal); self.slider_cities.setMinimum(4)
        self.slider_cities.valueChanged.connect(self.on_city_count_changed)
        l_data.addWidget(QLabel("Số lượng thành phố:"))
        l_data.addWidget(self.slider_cities)
        side_layout.addWidget(grp_data)

        grp_algo = QGroupBox("⚙️ CẤU HÌNH")
        l_algo = QFormLayout(grp_algo)
        self.combo_algo = QComboBox()
        self.combo_algo.addItems(["Hill Climbing", "PSO"])
        self.combo_algo.currentIndexChanged.connect(self.on_algo_changed)
        l_algo.addRow("Thuật toán:", self.combo_algo)
        
        self.combo_start_city = QComboBox() # Đây là biến mới
        l_algo.addRow("Điểm Xuất Phát:", self.combo_start_city)
        # -------------------------------------------------------

        self.stack_params = QStackedWidget()
        
        # HC Params
        w_hc = QWidget()
        l_hc = QFormLayout(w_hc)
        l_hc.setContentsMargins(0,0,0,0)
        self.hc_method = QComboBox(); self.hc_method.addItems(["random", "nn"])
        self.hc_seed = QSpinBox(); self.hc_seed.setValue(42); self.hc_seed.setRange(0, 99999)
        self.hc_improve = QSpinBox(); self.hc_improve.setValue(100); self.hc_improve.setRange(10, 50000)
        l_hc.addRow("Khởi tạo:", self.hc_method)
        l_hc.addRow("Seed:", self.hc_seed)
        l_hc.addRow("Max No Improve:", self.hc_improve)
        
        # PSO Params
        w_pso = QWidget()
        l_pso = QFormLayout(w_pso)
        l_pso.setContentsMargins(0,0,0,0)
        self.pso_swarm = QSpinBox(); self.pso_swarm.setValue(30); self.pso_swarm.setRange(10, 500)
        self.pso_iter = QSpinBox(); self.pso_iter.setValue(100); self.pso_iter.setRange(10, 5000)
        self.pso_w = QDoubleSpinBox(); self.pso_w.setValue(0.7); self.pso_w.setSingleStep(0.1)
        self.pso_c1 = QDoubleSpinBox(); self.pso_c1.setValue(1.5); self.pso_c1.setSingleStep(0.1)
        self.pso_c2 = QDoubleSpinBox(); self.pso_c2.setValue(1.5); self.pso_c2.setSingleStep(0.1)
        l_pso.addRow("Swarm Size:", self.pso_swarm)
        l_pso.addRow("Iterations:", self.pso_iter)
        l_pso.addRow("W:", self.pso_w); l_pso.addRow("C1:", self.pso_c1); l_pso.addRow("C2:", self.pso_c2)

        self.stack_params.addWidget(w_hc)
        self.stack_params.addWidget(w_pso)
        l_algo.addRow(self.stack_params)
        side_layout.addWidget(grp_algo)

        self.btn_run = QPushButton("BẮT ĐẦU CHẠY")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setFixedHeight(40)
        self.btn_run.clicked.connect(self.on_run)
        side_layout.addWidget(self.btn_run)
        
        grp_res = QGroupBox("🏆 KẾT QUẢ")
        l_res = QFormLayout(grp_res)
        self.lbl_best_dist = QLabel("--- km")
        self.lbl_best_dist.setStyleSheet("color: #a6e3a1; font-size: 16px; font-weight: bold;")
        self.lbl_time = QLabel("--- s")
        l_res.addRow("Tốt nhất:", self.lbl_best_dist)
        l_res.addRow("Thời gian:", self.lbl_time)
        side_layout.addWidget(grp_res)
        side_layout.addStretch()

        # === MAIN CONTENT ===
        content = QWidget()
        cont_layout = QVBoxLayout(content)
        self.tabs = QTabWidget()
        self.tab_dash = DashboardTab()
        self.tab_matrix = QTableWidget()
        self.tab_compare = ComparisonTab()
        self.tabs.addTab(self.tab_dash, "📊 Trực quan hóa")
        self.tabs.addTab(self.tab_matrix, "🔢 Ma trận khoảng cách")
        self.tabs.addTab(self.tab_compare, "⚖️ So sánh")
        self.log_box = QTextEdit()
        self.log_box.setFixedHeight(180)
        self.log_box.setReadOnly(True)
        cont_layout.addWidget(self.tabs, stretch=3)
        cont_layout.addWidget(QLabel("📝 NHẬT KÝ GIẢI PHÁP (LOG)"))
        cont_layout.addWidget(self.log_box, stretch=1)
        layout.addWidget(sidebar)
        layout.addWidget(content)

    def load_data_automatically(self):
        try:
            self.all_cities = DataLoader.load_cities_from_json("data/data_cities.json")
            total = len(self.all_cities)
            if total < 4: raise ValueError("Data < 4 cities")
            self.slider_cities.setMaximum(total)
            self.slider_cities.setValue(total)
            self.on_city_count_changed(total)
            self.log(f"[SYSTEM] Đã tải dữ liệu gốc: {total} thành phố.", "green")
        except Exception as e:
            self.log(f"[ERROR] {e}", "red")

    def on_city_count_changed(self, count):
        self.cities = self.all_cities[:count]
        self.distance_matrix = DistanceMatrix(self.cities)
        self.lbl_city_count.setText(f"{count} thành phố")
        
        self.combo_start_city.clear()
        self.combo_start_city.addItem("Ngẫu nhiên", None)
        for c in self.cities:
            self.combo_start_city.addItem(c.name, c.id)
            
        self.tab_dash.update_map(self.cities, None)
        self.populate_matrix_table()

    def populate_matrix_table(self):
        n = len(self.cities)
        self.tab_matrix.setRowCount(n)
        self.tab_matrix.setColumnCount(n)
        headers = [c.name for c in self.cities]
        self.tab_matrix.setHorizontalHeaderLabels(headers)
        self.tab_matrix.setVerticalHeaderLabels(headers)
        for i in range(n):
            for j in range(n):
                dist = self.distance_matrix.get_distance(self.cities[i].id, self.cities[j].id)
                item = QTableWidgetItem(f"{dist:.1f}")
                item.setTextAlignment(Qt.AlignCenter)
                if i==j: item.setBackground(QColor('#313244'))
                self.tab_matrix.setItem(i, j, item)

    def on_algo_changed(self, idx):
        self.stack_params.setCurrentIndex(idx)

    def log(self, msg, color="white"):
        hex_color = {"green": "#a6e3a1", "red": "#f38ba8", "blue": "#89b4fa", "white": "#cdd6f4"}.get(color, color)
        self.log_box.append(f'<span style="color:{hex_color}">{msg}</span>')

    def on_run(self):
        if not self.cities: return
        algo = self.combo_algo.currentText()
        params = {}
        
        # --- LẤY ĐIỂM XUẤT PHÁT CHUNG ---
        start_id = self.combo_start_city.currentData()
        # ---------------------------------

        if "Hill" in algo:
            params = {
                'initial_method': self.hc_method.currentText(),
                'start_city_id': start_id, # Truyền cho HC
                'seed': self.hc_seed.value(),
                'max_no_improve': self.hc_improve.value()
            }
        else:
            params = {
                'start_city_id': start_id, # Truyền cho PSO 
                'swarm_size': self.pso_swarm.value(),
                'num_iterations': self.pso_iter.value(),
                'w': self.pso_w.value(),
                'c1': self.pso_c1.value(),
                'c2': self.pso_c2.value()
            }

        self.btn_run.setEnabled(False)
        self.slider_cities.setEnabled(False)
        self.log_box.clear()
        
        start_name = self.combo_start_city.currentText()
        self.log(f"🚀 Chạy {algo} | Xuất phát: {start_name}", "blue")
        
        self.thread = SolverThread(algo, params, self.cities, self.distance_matrix)
        self.thread.result_signal.connect(self.on_finish)
        self.thread.log_signal.connect(lambda s: self.log(f"  >> {s}", "#a6adc8"))
        self.thread.start()

    def on_finish(self, best, history, sol_log, elapsed):
        self.btn_run.setEnabled(True)
        self.slider_cities.setEnabled(True)
        self.lbl_best_dist.setText(f"{best.distance:.1f} km")
        self.lbl_time.setText(f"{elapsed:.4f} s")
        self.tab_dash.update_map(self.cities, best)
        self.tab_dash.update_conv(history)
        self.tab_compare.add_result(self.combo_algo.currentText(), best.distance, elapsed, len(history))
        self.log("-" * 40, "white")
        self.log(f"🏁 HOÀN THÀNH! Best: {best.distance:.2f} km", "green")
        self.log(f"★ Số lần lặp: {len(history)}", "green")
        self.log("📜 NHẬT KÝ CẢI THIỆN (TÓM TẮT):", "#f9e2af")
        if len(sol_log) > 50:
             for item in sol_log[:10]: self.log(f"[{item[0]}] {item[1]:.2f} km | {item[2]}", "white")
             self.log(f"... (Ẩn {len(sol_log)-20} bước trung gian) ...", "#a6adc8")
             for item in sol_log[-10:]: self.log(f"[{item[0]}] {item[1]:.2f} km | {item[2]}", "white")
        else:
             for step, dist, desc in sol_log: self.log(f"[{step}] {dist:.2f} km | {desc}", "white")
        
        path = " -> ".join([c.name for c in best.cities])
        self.log(f"📍 Lộ trình: {path} -> {best.cities[0].name}", "#89b4fa")
        self.tabs.setCurrentIndex(0)