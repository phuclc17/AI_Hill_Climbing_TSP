
import json
import os
import datetime
from typing import List, Dict, Any

# Import đường dẫn file từ config
from config.settings import HISTORY_FILE_PATH

class RunHistory:
    """
    Quản lý việc đọc và ghi lịch sử các lần chạy thuật toán.
    """
    
    @staticmethod
    def load_history() -> List[Dict[str, Any]]:
        """Tải toàn bộ lịch sử chạy từ file JSON."""
        if not os.path.exists(HISTORY_FILE_PATH):
            return []
        try:
            with open(HISTORY_FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Lỗi: File lịch sử {HISTORY_FILE_PATH} bị hỏng.")
            return []

    @staticmethod
    def save_run(run_result: Dict[str, Any]):
        """
        Thêm một kết quả chạy mới vào file lịch sử.
        
        Args:
            run_result (Dict): Một dict chứa thông tin về lần chạy 
                               (ví dụ: algo, params, distance, time).
        """
        history = RunHistory.load_history()
        
        # Thêm thông tin thời gian
        run_result["timestamp"] = datetime.datetime.now().isoformat()
        history.append(run_result)
        
        try:
            with open(HISTORY_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Lỗi khi lưu lịch sử: {e}")