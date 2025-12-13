# advent of code 2025 - day 9
from ast import While
from itertools import combinations
day_no = 9


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


class CoupleOfPoints:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.area = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
        self.calculatedv1 = Point( p1.x if p1.x < p2.x else p2.x, p2.y if p1.y < p2.y else p1.y)
        self.calculatedv2 = Point( p2.x if p1.x < p2.x else p1.x, p1.y if p1.y < p2.y else p2.y)    
        self.min_x = min(p1.x, p2.x)
        self.max_x = max(p1.x, p2.x)
        self.min_y = min(p1.y, p2.y)
        self.max_y = max(p1.y, p2.y)


    def __eq__(self, other):
        if isinstance(other, CoupleOfPoints):
            return self.p1 == other.p1 and self.p2 == other.p2
        return False

    def __lt__(self, other):
        return self.area < other.area

    def __iter__(self):
        yield self.p1
        yield self.p2

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __repr__(self):
        return f"CoupleOfPoints(p1={self.p1}, p2={self.p2}, area={self.area})"

    def V1Directions(self):
        if self.calculatedv1.x == self.min_x:
            if self.calculatedv1.y == self.min_y:
                return [MoveUp, MoveRight]
            else:
                return [MoveDown, MoveRight]
        else:
            if self.calculatedv1.y == self.min_y:
                return [MoveUp, MoveLeft]
            else:
                return [MoveDown, MoveLeft]
            
    def V2Directions(self):
        if self.calculatedv2.x == self.min_x:
            if self.calculatedv2.y == self.min_y:
                return [MoveUp, MoveRight]
            else:
                return [MoveDown, MoveRight]
        else:
            if self.calculatedv2.y == self.min_y:
                return [MoveUp, MoveLeft]
            else:
                return [MoveDown, MoveLeft]


def P1(points):
    couples = []
    for a in combinations(range(len(points)), 2):
        couples.append(CoupleOfPoints(points[a[0]], points[a[1]]))
    return max(couples).area


def P2(points, max_point):
    couples = []
    for a in combinations(range(len(points)), 2):
        couples.append(CoupleOfPoints(points[a[0]], points[a[1]]))
    couples = sorted(couples, reverse=True)
    for rectangle in couples:
        if IsRectangleContained(rectangle, points, max_point):
            return rectangle.area
    return 0


def GetPoints(f):
    points = []
    max_x = 0
    max_y = 0
    for line in f:
        parts = line.strip().split(',')
        x, y = map(int, parts)
        points.append(Point(x, y))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return points, Point(max_x, max_y)

def FindPointsByX(points, x_value ):
    return [p for p in points if p.x == x_value]

def FindPointsByY(points, y_value ):
    return [p for p in points if p.y == y_value]

def MoveUp(point, max_point):
    if point.y < max_point.y:
        return Point(point.x, point.y + 1), True
    return point, False

def MoveDown(point):
    if point.y > 0:
        return Point(point.x, point.y - 1), True
    return point, False

def MoveLeft(point):
    if point.x > 0:
        return Point(point.x - 1, point.y), True
    return point, False

def MoveRight(point, max_point):
    if point.x < max_point.x:
        return Point(point.x + 1, point.y), True
    return point, False

def IsBetween(point, p1, p2):
    if p1.x == p2.x:
        return point.x == p1.x and min(p1.y, p2.y) <= point.y <= max(p1.y, p2.y)
    elif p1.y == p2.y:
        return point.y == p1.y and min(p1.x, p2.x) <= point.x <= max(p1.x, p2.x)
    return False

def IsRectangleContained(rectangle, points, max_point):  
    if rectangle.max_x == rectangle.min_x:
        return True
    direction =  rectangle.V1Directions()[0]
    current_point = rectangle.calculatedv1
    intersections = 0
    if direction == MoveUp:
        #for delta_y in range(rectangle.max_y - rectangle.min_y + 1):
        while True:
            current_point, moved = MoveUp(current_point, max_point)
            if not moved:
                break
            segment_points = FindPointsByY(points, current_point.y)
            if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
                intersections += 1
        if intersections != 1:
            return False
    current_point = rectangle.calculatedv1
    intersections = 0
    if direction == MoveDown:
        #for delta_y in range(rectangle.max_y - rectangle.min_y + 1):
        while True:
            current_point, moved = MoveDown(current_point)
            if not moved:
                break
            segment_points = FindPointsByY(points, current_point.y)
            if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
                intersections += 1
        if intersections != 1:
            return False
    # current_point = rectangle.calculatedv1
    
    # intersections = 0
    # if direction == MoveLeft:
    #     for delta_x in range(rectangle.max_x - rectangle.min_x + 1):
    #         current_point, moved = MoveLeft(current_point)
    #         if not moved:
    #             break
    #         segment_points = FindPointsByX(points, current_point.x)
    #         if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
    #             intersections += 1
    #     if intersections != 1:
    #         return False
    # current_point = rectangle.calculatedv1
    # intersections = 0   
    # if direction == MoveRight:
    #     for delta_x in range(rectangle.max_x - rectangle.min_x + 1):
    #         current_point, moved = MoveRight(current_point, max_point)
    #         if not moved:
    #             break
    #         segment_points = FindPointsByX(points, current_point.x)
    #         if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
    #             intersections += 1
    #     if intersections != 1:
    #         return False
        
    current_point = rectangle.calculatedv2
    direction =  rectangle.V2Directions()[0]
    intersections = 0
    if direction == MoveUp:
        for delta_y in range(rectangle.max_y - rectangle.min_y + 1):
            current_point, moved = MoveUp(current_point, max_point)
            if not moved:
                break
            segment_points = FindPointsByY(points, current_point.y)
            if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
                intersections += 1
        if intersections != 1:
            return False
    current_point = rectangle.calculatedv1
    intersections = 0
    if direction == MoveDown:
        for delta_y in range(rectangle.max_y - rectangle.min_y + 1):
            current_point, moved = MoveDown(current_point)
            if not moved:
                break
            segment_points = FindPointsByY(points, current_point.y)
            if len(segment_points)>0 and IsBetween(current_point, segment_points[0], segment_points[-1]):
                intersections += 1
        if intersections != 1:
            return False
    return True
    

f = open(f"resources\day{day_no:02}.txt", "r")
points, max_point = GetPoints(f)
f.close()
print(f"Day {day_no}/1: {P1(points)}")
print(f"Day {day_no}/2: {P2(points, max_point)}")
