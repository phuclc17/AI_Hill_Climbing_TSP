class City:
 
    def __init__(self, id: int, x: float, y: float):
        """Khởi tạo một đối tượng Thành phố."""
        self.id = id
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        """Trả về một biểu diễn chuỗi rõ ràng của đối tượng City."""
        return f"City(id={self.id}, x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        """So sánh hai đối tượng City dựa trên id."""
        if isinstance(other, City):
            return self.id == other.id
        return False
        
    def __hash__(self) -> int:
        """Cho phép đối tượng City được sử dụng trong set hoặc làm key của dictionary."""
        return hash(self.id)