import json
from typing import List, Dict, Tuple
from models.city import City


class DataLoader:
  
    
    @staticmethod
    def load_cities_from_json(filepath: str) -> List[City]:
   
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        cities = []
        
        for location in data.get('locations', []):
        
            city = City(
                id=location['id'],
                name=location['name'],
                latitude=location['latitude'],
                longitude=location['longitude']
            )
            cities.append(city)
            
        return cities
    
    @staticmethod
    def get_city_names(filepath: str) -> Dict[int, str]:
        
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        city_names = {}
        for location in data.get('locations', []):
            city_names[location['id']] = location['name']
            
        return city_names
    
    @staticmethod
    def load_cities_with_names(filepath: str) -> Tuple[List[City], Dict[int, str]]:
        """
        Load cả danh sách City và dictionary tên thành phố cùng lúc.
        
        Args:
            filepath (str): Đường dẫn tới file JSON
            
        Returns:
            Tuple[List[City], Dict[int, str]]: (Danh sách City, Dictionary tên thành phố)
        """
        cities = DataLoader.load_cities_from_json(filepath)
        city_names = DataLoader.get_city_names(filepath)
        
        return cities, city_names
    
    @staticmethod
    def export_tour_to_json(tour, filepath: str, city_names: Dict[int, str] = None):
        """
        Xuất kết quả tour ra file JSON.
        
        Args:
            tour: Đối tượng Tour
            filepath (str): Đường dẫn file xuất ra
            city_names (Dict, optional): Dictionary ánh xạ id -> tên thành phố
        """
        tour_data = {
            "total_distance": round(tour.distance, 2),
            "num_cities": len(tour.cities),
            "path": []
        }
        
        for idx, city in enumerate(tour.cities):
            city_info = {
                "order": idx + 1,
                "id": city.id,
                "latitude": city.y,
                "longitude": city.x
            }
            
            if city_names and city.id in city_names:
                city_info["name"] = city_names[city.id]
            elif hasattr(city, 'name') and city.name:
                city_info["name"] = city.name
            
            tour_data["path"].append(city_info)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(tour_data, file, indent=2, ensure_ascii=False)
        
        print(f"Tour đã được xuất ra file: {filepath}")
    
    @staticmethod
    def export_comparison_results(results: Dict[str, Dict], filepath: str):
        """
        Xuất kết quả so sánh các thuật toán ra file JSON.
        
        Args:
            results (Dict): Dictionary chứa kết quả của các thuật toán
                          Format: {"Algorithm1": {"distance": 100, "time": 5.2}, ...}
            filepath (str): Đường dẫn file xuất ra
        """
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
        
        print(f"Kết quả so sánh đã được xuất ra file: {filepath}")