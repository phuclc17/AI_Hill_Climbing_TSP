"""
Simple Hill-Climbing (2-opt) TSP solver with a CLI runner.

Usage (from repo root):
    python -m algorithms.hill_climbing_tsp --data data/data_cities.json --method nn --seed 42

This implementation uses only the Python standard library.
"""
import argparse
import json
import os
import sys
import time
from typing import List

# Ensure project root is on sys.path when running the script directly so
# imports like `models.city` and `utils.*` resolve correctly.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from models.city import City
from models.tour import Tour
from utils.distance_matrix import DistanceMatrix
from utils.tour_generator import random_tour, nearest_neighbor_tour


def two_opt_swap(cities: List[City], i: int, k: int) -> List[City]:
    new = cities[:i] + list(reversed(cities[i:k + 1])) + cities[k + 1:]
    return new


class HillClimbingSolver:
    def __init__(self, cities: List[City], distance_matrix: DistanceMatrix):
        self.cities = cities
        self.distance_matrix = distance_matrix

    def run(self, initial_method: str = 'random', seed: int | None = None, max_no_improve: int = 1000):
        if initial_method == 'nn':
            current_cities = nearest_neighbor_tour(self.cities, self.distance_matrix)
        else:
            current_cities = random_tour(self.cities, seed)

        current = Tour(current_cities, self.distance_matrix)
        best = current

        n = len(current.cities)
        no_improve = 0

        start_time = time.time()

        while no_improve < max_no_improve:
            improved = False
            # simple 2-opt first-improvement
            for i in range(0, n - 1):
                for k in range(i + 1, n):
                    candidate_cities = two_opt_swap(current.cities, i, k)
                    candidate = Tour(candidate_cities, self.distance_matrix)
                    if candidate.distance < best.distance:
                        best = candidate
                        current = candidate
                        improved = True
                        no_improve = 0
                        break
                if improved:
                    break

            if not improved:
                no_improve += 1

        elapsed = time.time() - start_time
        return best, elapsed


def load_cities_from_json(path: str) -> List[City]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    locations = data.get('locations', [])
    cities = []
    for item in locations:
        cid = int(item.get('id'))
        # City expects (id, x, y) — we map x=longitude, y=latitude
        x = float(item.get('longitude'))
        y = float(item.get('latitude'))
        cities.append(City(cid, x, y))
    return cities


def main():
    parser = argparse.ArgumentParser(description='Hill-Climbing TSP solver (2-opt)')
    parser.add_argument('--data', '-d', default='data/data_cities.json', help='Path to cities JSON')
    parser.add_argument('--method', '-m', choices=['random', 'nn'], default='nn', help='Initial tour method')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--no-improve', type=int, default=100, help='Stop after this many non-improving iterations')
    args = parser.parse_args()

    cities = load_cities_from_json(args.data)
    if not cities:
        print('No cities found in data file')
        return

    dm = DistanceMatrix(cities)
    solver = HillClimbingSolver(cities, dm)

    best, elapsed = solver.run(initial_method=args.method, seed=args.seed, max_no_improve=args.no_improve)

    print('Result:')
    print(f'  Cities: {len(best.cities)}')
    print(f'  Distance (km): {best.distance:.2f}')
    print(f'  Time (s): {elapsed:.3f}')
    print('  Path (ids):')
    print('    ' + ' -> '.join(str(c.id) for c in best.cities))


if __name__ == '__main__':
    main()
