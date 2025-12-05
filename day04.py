# day04.py

import copy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y 
        return False

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

def P1(map):
    goodPallets, map_copy = ProcessMap(map)
    return goodPallets

def P2(map):
    goodPallets, map_copy = ProcessMap(map)
    goodPallets_iteration = goodPallets
    while goodPallets_iteration > 0:
        goodPallets_iteration, map_copy = ProcessMap(map_copy)
        goodPallets += goodPallets_iteration
    return goodPallets

def ProcessMap(map):
    map_copy = copy.deepcopy(map)
    goodPallets = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            point = Point(x, y)
            if map[y][x] == '.':
                continue
            adjacent_points = AdjacentPoints(point, map)
            if sum(1 for adj in adjacent_points if map[adj.y][adj.x] == '@') < 4:
                map_copy[y][x] = '.'
                goodPallets += 1
    return goodPallets, map_copy



def IsInMap(map, point):
    return point.y >= 0 and point.y < len(map) and point.x >= 0 and point.x < len(map[point.y])

def ReadAllMap(f):
    map = []
    for line in f:
        map.append(list(line.strip()))
    return map

def AdjacentPoints(point, map):
    adjacent_points = []
    directions = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),          (1, 0),
                  (-1, 1),  (0, 1),  (1, 1)]
    for dx, dy in directions:
        neighbor = Point(point.x + dx, point.y + dy)
        if IsInMap(map, neighbor):
            adjacent_points.append(neighbor)
    return adjacent_points

f = open("resources\day04.txt", "r")
map = ReadAllMap(f)
f.close()
print(f"Day 8/1: {P1(map)}")
print(f"Day 8/2: {P2(map)}")
