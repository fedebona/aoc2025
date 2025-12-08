# advent of code 2025 - day 08
from functools import reduce
from itertools import combinations
day_no = 8


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"


class CoupleOfPoints:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.distance = ((p1.x - p2.x) ** 2 + (p1.y - p2.y)
                         ** 2 + (p1.z - p2.z) ** 2) ** 0.5

    def __eq__(self, other):
        if isinstance(other, CoupleOfPoints):
            return self.p1 == other.p1 and self.p2 == other.p2
        return False

    def __lt__(self, other):
        return self.distance < other.distance

    def __iter__(self):
        yield self.p1
        yield self.p2

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __repr__(self):
        return f"CoupleOfPoints(p1={self.p1}, p2={self.p2}, distance={self.distance})"


def P1(points, iterations=10):
    couples = []
    for a in combinations(range(len(points)), 2):
        couples.append(CoupleOfPoints(points[a[0]], points[a[1]]))
    couples.sort()
    circuits = []
    for i in range(iterations):
        # print(couples[i])
        theSet = {couples[i].p1, couples[i].p2}
        found = False
        indexes_found = []
        for iterator in range(len(circuits)):
            if not circuits[iterator].isdisjoint(theSet):
                circuits[iterator] = circuits[iterator].union(theSet)
                found = True
                indexes_found.append(iterator)
        if not found:
            circuits.append(theSet)
        else:
            # merge all found circuits
            first_index = indexes_found[0]
            for idx in sorted(indexes_found[1:], reverse=True):
                circuits[first_index] = circuits[first_index].union(
                    circuits[idx])
                del circuits[idx]
    sizes = sorted((len(circuit) for circuit in circuits), reverse=True)
    top3 = sizes[:3]
    return reduce(multiply, top3)


def P2(points):
    couples = []
    for a in combinations(range(len(points)), 2):
        couples.append(CoupleOfPoints(points[a[0]], points[a[1]]))
    couples.sort()
    circuits = []
    i = 0
    while True:
        # print(couples[i])
        theSet = {couples[i].p1, couples[i].p2}
        found = False
        indexes_found = []
        for iterator in range(len(circuits)):
            if not circuits[iterator].isdisjoint(theSet):
                circuits[iterator] = circuits[iterator].union(theSet)
                found = True
                indexes_found.append(iterator)
        if not found:
            circuits.append(theSet)
        else:
            # merge all found circuits
            first_index = indexes_found[0]
            for idx in sorted(indexes_found[1:], reverse=True):
                circuits[first_index] = circuits[first_index].union(
                    circuits[idx])
                del circuits[idx]
        if max(len(circuit) for circuit in circuits) == len(points):
            break
        i += 1
    return couples[i].p1.x * couples[i].p2.x


def multiply(x, y):
    return x * y


def GetPoints(f):
    points = []
    for line in f:
        parts = line.strip().split(',')
        x, y, z = map(int, parts)
        points.append(Point(x, y, z))
    return points


f = open(f"resources\day{day_no:02}.txt", "r")
points = GetPoints(f)
f.close()
print(f"Day {day_no}/1: {P1(points,1000)}")
print(f"Day {day_no}/2: {P2(points)}")
