

class City:
    """
    Đại diện cho một thành phố với các thuộc tính cơ bản.
    
    Lớp này được thiết kế để khớp với dữ liệu từ 'data_cities.json'
    và tự động ánh xạ vĩ độ/kinh độ sang (x, y).
    """
    
    def __init__(self, id: int, name: str, latitude: float, longitude: float):
        """
        Khởi tạo một đối tượng Thành phố.

        Args:
            id (int): Mã định danh duy nhất (từ JSON).
            name (str): Tên của thành phố (từ JSON).
            latitude (float): Vĩ độ (từ JSON).
            longitude (float): Kinh độ (từ JSON).
        """
        self.id = int(id)
        self.name = str(name)
        self.x = float(longitude)
        self.y = float(latitude)

    def __repr__(self) -> str:
        """Trả về một biểu diễn chuỗi rõ ràng, hiển thị cả tên."""
        return f"City(id={self.id}, name='{self.name}', x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        """So sánh hai đối tượng City dựa trên id."""
        if isinstance(other, City):
            return self.id == other.id
        return False
        
    def __hash__(self) -> int:
        """Cho phép đối tượng City được sử dụng trong set hoặc làm key của dictionary."""
        return hash(self.id)