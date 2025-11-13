import random
from typing import List

def random_tour(cities: List[object], seed: int | None = None) -> List[object]:
    """Return a random permutation (copy) of the cities."""
    seq = cities[:]  # shallow copy
    if seed is not None:
        random.Random(seed).shuffle(seq)
    else:
        random.shuffle(seq)
    return seq

def nearest_neighbor_tour(cities: List[object], distance_matrix, start_index: int = 0) -> List[object]:
    """
    Build a tour using the nearest neighbor heuristic.
    `cities` is a list of City objects. `distance_matrix` provides get_distance(id_a,id_b).
    """
    if not cities:
        return []

    id_to_city = {c.id: c for c in cities}
    unvisited = set(c.id for c in cities)
    start_city = cities[start_index]
    path = [start_city]
    unvisited.remove(start_city.id)
    current_id = start_city.id

    while unvisited:
        # find nearest unvisited
        next_id = min(unvisited, key=lambda uid: distance_matrix.get_distance(current_id, uid))
        path.append(id_to_city[next_id])
        unvisited.remove(next_id)
        current_id = next_id

    return path
