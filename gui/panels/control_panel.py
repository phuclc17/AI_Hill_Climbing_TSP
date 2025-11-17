

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
                             QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
                             QTabWidget)
from PyQt5.QtCore import pyqtSignal

class ControlPanel(QWidget):
    """
    Widget điều khiển chính, chứa tất cả các panel nhập liệu và tham số.
    """
    
    # Định nghĩa các tín hiệu (signals) mà các nút bấm sẽ phát ra
    run_signal = pyqtSignal()
    load_data_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()

    def _init_ui(self):
        # Layout chính của panel này là layout dọc
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- 1. Panel Nhập liệu (Input Panel) ---
        input_group = QGroupBox("1. Tải Dữ Liệu")
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)
        
        self.load_data_button = QPushButton("Tải data_cities.json")
        self.load_data_button.clicked.connect(self.load_data_signal.emit) # Kết nối nút
        input_layout.addWidget(self.load_data_button)
        
        main_layout.addWidget(input_group)

        # --- 2. Panel Thuật toán (Algorithm Panel) ---
        algo_group = QGroupBox("2. Chọn Thuật Toán")
        algo_layout = QFormLayout()
        algo_group.setLayout(algo_layout)
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Hill Climbing (HC)", "PSO"])
        algo_layout.addRow("Thuật toán:", self.algo_combo)
        
        main_layout.addWidget(algo_group)

        # --- 3. Panel Tham số (Parameter Panel) ---
        # Sử dụng QTabWidget để tách biệt tham số của HC và PSO
        self.param_tabs = QTabWidget()
        
        hc_widget = self._create_hc_panel()
        pso_widget = self._create_pso_panel()
        
        self.param_tabs.addTab(hc_widget, "Tham số HC")
        self.param_tabs.addTab(pso_widget, "Tham số PSO")
        
        main_layout.addWidget(self.param_tabs)

        # --- 4. Panel Điều khiển (Control Panel) ---
        control_group = QGroupBox("4. Chạy")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)

        self.run_button = QPushButton("BẮT ĐẦU CHẠY")
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.run_button.clicked.connect(self.run_signal.emit) # Kết nối nút
        control_layout.addWidget(self.run_button)

        main_layout.addWidget(control_group)

        # Thêm một "spacer" để đẩy mọi thứ lên trên
        main_layout.addStretch(1)

    def _create_hc_panel(self) -> QWidget:
        """Tạo panel chứa tham số cho Hill Climbing."""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)

        self.hc_restarts_spinbox = QSpinBox()
        self.hc_restarts_spinbox.setRange(1, 10000)
        self.hc_restarts_spinbox.setValue(50)
        
        layout.addRow("Số lần Restart:", self.hc_restarts_spinbox)
        return widget

    def _create_pso_panel(self) -> QWidget:
        """Tạo panel chứa tham số cho PSO."""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)

        self.pso_swarm_spinbox = QSpinBox()
        self.pso_swarm_spinbox.setRange(10, 1000)
        self.pso_swarm_spinbox.setValue(30)
        
        self.pso_iter_spinbox = QSpinBox()
        self.pso_iter_spinbox.setRange(10, 10000)
        self.pso_iter_spinbox.setValue(100)
        
        self.pso_w_spinbox = QDoubleSpinBox()
        self.pso_w_spinbox.setRange(0.1, 1.0)
        self.pso_w_spinbox.setValue(0.7)
        self.pso_w_spinbox.setSingleStep(0.1)

        self.pso_c1_spinbox = QDoubleSpinBox()
        self.pso_c1_spinbox.setRange(0.1, 3.0)
        self.pso_c1_spinbox.setValue(1.5)
        self.pso_c1_spinbox.setSingleStep(0.1)

        self.pso_c2_spinbox = QDoubleSpinBox()
        self.pso_c2_spinbox.setRange(0.1, 3.0)
        self.pso_c2_spinbox.setValue(1.5)
        self.pso_c2_spinbox.setSingleStep(0.1)

        layout.addRow("Số hạt (Swarm size):", self.pso_swarm_spinbox)
        layout.addRow("Số vòng lặp (Iterations):", self.pso_iter_stopinbox)
        layout.addRow("Hệ số W (Quán tính):", self.pso_w_spinbox)
        layout.addRow("Hệ số C1 (Nhận thức):", self.pso_c1_spinbox)
        layout.addRow("Hệ số C2 (Xã hội):", self.pso_c2_spinbox)
        
        return widget
        
    def get_parameters(self) -> dict:
        """Lấy tất cả tham số từ GUI để truyền cho thuật toán."""
        algo = self.algo_combo.currentText()
        params = {"algorithm": algo}
        
        if "HC" in algo:
            params['num_restarts'] = self.hc_restarts_spinbox.value()
        elif "PSO" in algo:
            params['swarm_size'] = self.pso_swarm_spinbox.value()
            params['num_iterations'] = self.pso_iter_spinbox.value()
            params['w'] = self.pso_w_spinbox.value()
            params['c1'] = self.pso_c1_spinbox.value()
            params['c2'] = self.pso_c2_spinbox.value()
            
        return params