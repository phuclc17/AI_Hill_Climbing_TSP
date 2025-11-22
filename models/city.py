

class City:

    
    def __init__(self, id: int, name: str, latitude: float, longitude: float):
  
        self.id = int(id)
        self.name = str(name)
        self.x = float(longitude)
        self.y = float(latitude)

    def __repr__(self) -> str:

        return f"City(id={self.id}, name='{self.name}', x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:

        if isinstance(other, City):
            return self.id == other.id
        return False
        
    def __hash__(self) -> int:

        return hash(self.id)