
import json
from typing import List
from models.city import City


class DataLoader:
    """
    Lớp chịu trách nhiệm load dữ liệu thành phố từ file JSON.
    """
    
    @staticmethod
    def load_cities_from_json(filepath: str) -> List[City]:
        """
        Đọc file JSON chứa thông tin các thành phố và chuyển đổi 
        thành danh sách các đối tượng City.
        
        Args:
            filepath (str): Đường dẫn tới file JSON
            
        Returns:
            List[City]: Danh sách các đối tượng City
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        cities = []
        
        for location in data.get('locations', []):
            city = City(
                id=location['id'],
                x=location['longitude'],  
                y=location['latitude']     
            )
            cities.append(city)
            
        return cities
    
    @staticmethod
    def get_city_names(filepath: str) -> dict:
        """
        Lấy mapping giữa ID và tên thành phố.
        
        Args:
            filepath (str): Đường dẫn tới file JSON
            
        Returns:
            dict: Dictionary với key là id, value là tên thành phố
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        city_names = {}
        for location in data.get('locations', []):
            city_names[location['id']] = location['name']
            
        return city_names