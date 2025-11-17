# File: main.py
# (Nằm ở thư mục gốc của dự án)

import sys
import os # <-- 1. THÊM DÒNG NÀY

# --- 2. THÊM 3 DÒNG NÀY ---
# Thêm thư mục gốc của dự án vào đường dẫn (sys.path)
# Điều này giúp Python tìm thấy các module (gui, models, utils...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ---------------------------

from PyQt5.QtWidgets import QApplication

# Bây giờ các lệnh import này sẽ hoạt động
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Tạo và hiển thị cửa sổ chính
    window = MainWindow()
    window.show()
    
    # Bắt đầu vòng lặp sự kiện của ứng dụng
    sys.exit(app.exec_())