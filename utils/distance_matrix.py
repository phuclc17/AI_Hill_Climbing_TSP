import math
from typing import List, Dict

class DistanceMatrix:
    """
    Simple distance matrix using haversine formula for lat/lon coordinates.
    Stores distances in a dict-of-dicts keyed by city id for O(1) lookup.
    """
    def __init__(self, cities: List[object]):
        # cities: list of objects with attributes `id`, `x` (lon) and `y` (lat)
        self._ids = [c.id for c in cities]
        self._coords = {c.id: (float(c.y), float(c.x)) for c in cities}  # (lat, lon)
        self._matrix: Dict[int, Dict[int, float]] = {}
        self._build()

    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2):
        # Earth radius in kilometers
        R = 6371.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def _build(self):
        for i in self._ids:
            self._matrix[i] = {}
        for i in self._ids:
            lat1, lon1 = self._coords[i]
            for j in self._ids:
                if i == j:
                    self._matrix[i][j] = 0.0
                else:
                    lat2, lon2 = self._coords[j]
                    self._matrix[i][j] = self._haversine(lat1, lon1, lat2, lon2)

    def get_distance(self, id_a: int, id_b: int) -> float:
        return self._matrix[id_a][id_b]
