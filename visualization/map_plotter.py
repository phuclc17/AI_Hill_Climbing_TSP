import matplotlib.pyplot as plt
from typing import List, Optional, Dict
from models.city import City
from models.tour import Tour


class MapPlotter:
    """
    Lớp chịu trách nhiệm vẽ bản đồ tour TSP.
    """
    
    @staticmethod
    def plot_tour(tour: Tour, 
                  city_names: Optional[Dict[int, str]] = None,
                  title: str = "TSP Tour",
                  figsize: tuple = (12, 10),
                  show_labels: bool = True,
                  show_distance: bool = True) -> plt.Figure:
        """
        Vẽ một tour TSP trên bản đồ.
        
        Args:
            tour (Tour): Đối tượng Tour cần vẽ
            city_names (Dict, optional): Dictionary ánh xạ id -> tên thành phố
            title (str): Tiêu đề của bản đồ
            figsize (tuple): Kích thước figure
            show_labels (bool): Có hiển thị tên thành phố không
            show_distance (bool): Có hiển thị tổng khoảng cách không
            
        Returns:
            plt.Figure: Figure object của matplotlib
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        cities = tour.cities
        
        for i in range(len(cities)):
            city_a = cities[i]
            city_b = cities[(i + 1) % len(cities)]  
            
            ax.plot([city_a.x, city_b.x], 
                   [city_a.y, city_b.y],
                   'b-', linewidth=1.5, alpha=0.6, zorder=1)
        
        x_coords = [city.x for city in cities]
        y_coords = [city.y for city in cities]
        
        ax.scatter(x_coords, y_coords, 
                  c='red', s=100, zorder=3, 
                  edgecolors='darkred', linewidths=2)
        
        start_city = cities[0]
        ax.scatter([start_city.x], [start_city.y], 
                  c='green', s=200, zorder=4, 
                  marker='*', edgecolors='darkgreen', linewidths=2,
                  label='Start')
        
        if show_labels:
            for city in cities:
                if city_names and city.id in city_names:
                    label = city_names[city.id]
                elif hasattr(city, 'name') and city.name:
                    label = city.name
                else:
                    label = f"City {city.id}"
                
                ax.annotate(label, 
                           (city.x, city.y),
                           xytext=(5, 5), 
                           textcoords='offset points',
                           fontsize=9,
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='yellow', 
                                   alpha=0.7),
                           zorder=5)
        
        if show_distance:
            title_text = f"{title}\nTotal Distance: {tour.distance:.2f} km"
        else:
            title_text = title
        
        ax.set_title(title_text, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_cities_only(cities: List[City],
                        city_names: Optional[Dict[int, str]] = None,
                        title: str = "Cities Map",
                        figsize: tuple = (12, 10)) -> plt.Figure:
        """
        Vẽ các thành phố mà không có đường nối.
        
        Args:
            cities (List[City]): Danh sách các thành phố
            city_names (Dict, optional): Dictionary ánh xạ id -> tên thành phố
            title (str): Tiêu đề
            figsize (tuple): Kích thước figure
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x_coords = [city.x for city in cities]
        y_coords = [city.y for city in cities]
        
        ax.scatter(x_coords, y_coords, 
                  c='blue', s=100, zorder=3,
                  edgecolors='darkblue', linewidths=2)
        
        for city in cities:
            if city_names and city.id in city_names:
                label = city_names[city.id]
            elif hasattr(city, 'name') and city.name:
                label = city.name
            else:
                label = f"City {city.id}"
            
            ax.annotate(label, 
                       (city.x, city.y),
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=9,
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='lightblue', 
                               alpha=0.7))
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_multiple_tours(tours: List[Tour],
                          tour_labels: Optional[List[str]] = None,
                          city_names: Optional[Dict[int, str]] = None,
                          title: str = "Multiple Tours Comparison",
                          figsize: tuple = (15, 10)) -> plt.Figure:
        """
        Vẽ nhiều tour trên cùng một bản đồ để so sánh.
        
        Args:
            tours (List[Tour]): Danh sách các tour
            tour_labels (List[str], optional): Tên của từng tour
            city_names (Dict, optional): Dictionary ánh xạ id -> tên thành phố
            title (str): Tiêu đề
            figsize (tuple): Kích thước figure
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
        
        for idx, tour in enumerate(tours):
            color = colors[idx % len(colors)]
            label = tour_labels[idx] if tour_labels and idx < len(tour_labels) else f"Tour {idx+1}"
            
            cities = tour.cities
            
            for i in range(len(cities)):
                city_a = cities[i]
                city_b = cities[(i + 1) % len(cities)]
                
                ax.plot([city_a.x, city_b.x], 
                       [city_a.y, city_b.y],
                       color=color, linewidth=1.5, alpha=0.5, 
                       label=label if i == 0 else "")
        
        all_cities = tours[0].cities
        x_coords = [city.x for city in all_cities]
        y_coords = [city.y for city in all_cities]
        
        ax.scatter(x_coords, y_coords, 
                  c='black', s=80, zorder=3,
                  edgecolors='white', linewidths=1.5)
        
        for city in all_cities:
            if city_names and city.id in city_names:
                label = city_names[city.id]
            elif hasattr(city, 'name') and city.name:
                label = city.name
            else:
                label = str(city.id)
            
            ax.annotate(label, 
                       (city.x, city.y),
                       xytext=(3, 3), 
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.2', 
                               facecolor='white', 
                               alpha=0.7))
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_tour_evolution(tours: List[Tour],
                           indices: List[int],
                           city_names: Optional[Dict[int, str]] = None,
                           title: str = "Tour Evolution",
                           figsize: tuple = (18, 12)) -> plt.Figure:
        """
        Vẽ quá trình tiến hóa của tour qua các iteration.
        
        Args:
            tours (List[Tour]): Danh sách các tour tại các iteration khác nhau
            indices (List[int]): Danh sách các iteration tương ứng
            city_names (Dict, optional): Dictionary ánh xạ id -> tên thành phố
            title (str): Tiêu đề chính
            figsize (tuple): Kích thước figure
            
        Returns:
            plt.Figure: Figure object
        """
        n_tours = len(tours)
        n_cols = 3
        n_rows = (n_tours + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for idx, (tour, iteration) in enumerate(zip(tours, indices)):
            row = idx // n_cols
            col = idx % n_cols
            ax = axes[row, col]
            
            cities = tour.cities
            
            for i in range(len(cities)):
                city_a = cities[i]
                city_b = cities[(i + 1) % len(cities)]
                
                ax.plot([city_a.x, city_b.x], 
                       [city_a.y, city_b.y],
                       'b-', linewidth=1, alpha=0.6)
            
            x_coords = [city.x for city in cities]
            y_coords = [city.y for city in cities]
            
            ax.scatter(x_coords, y_coords, 
                      c='red', s=50, zorder=3)
            
            ax.set_title(f"Iteration {iteration}\nDistance: {tour.distance:.2f} km",
                        fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Longitude', fontsize=8)
            ax.set_ylabel('Latitude', fontsize=8)
        
        for idx in range(n_tours, n_rows * n_cols):
            row = idx // n_cols
            col = idx % n_cols
            axes[row, col].axis('off')
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig