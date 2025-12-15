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

def IsPointInOrOnPolygon(point, polygon_points, sorted_polygon=None):
    """
    Check if a point is inside or on the boundary of a polygon.
    """
    if point in polygon_points:
        return True
    
    if len(polygon_points) < 3:
        return False
    
    # Use pre-sorted polygon if provided
    if sorted_polygon is None:
        # Calculate centroid and sort by angle
        cx = sum(p.x for p in polygon_points) / len(polygon_points)
        cy = sum(p.y for p in polygon_points) / len(polygon_points)
        
        import math
        def angle_from_centroid(p):
            return math.atan2(p.y - cy, p.x - cx)
        
        sorted_polygon = sorted(polygon_points, key=angle_from_centroid)
    
    n = len(sorted_polygon)
    
    # Check if point is on any polygon edge
    for i in range(n):
        p1 = sorted_polygon[i]
        p2 = sorted_polygon[(i + 1) % n]
        
        # Check if point is on the line segment p1-p2
        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        
        if min_x <= point.x <= max_x and min_y <= point.y <= max_y:
            # Check collinearity using cross product
            cross = (point.y - p1.y) * (p2.x - p1.x) - (point.x - p1.x) * (p2.y - p1.y)
            if abs(cross) < 1e-9:  # Point is on the line
                return True
    
    # Ray casting for inside check
    intersections = 0
    for i in range(n):
        p1 = sorted_polygon[i]
        p2 = sorted_polygon[(i + 1) % n]
        
        if (p1.y > point.y) != (p2.y > point.y):
            x_intersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x
            if point.x < x_intersection:
                intersections += 1
    
    return intersections % 2 == 1

def IsRectangleContained(rectangle, points, max_point):
    """
    Rectangle is valid if:
    1. All corners are inside or on the polygon boundary
    2. All rectangle edges stay inside the polygon (important for concave polygons)
    
    Optimized to pre-sort polygon once, then check every point on edges for accuracy.
    """
    # Pre-sort polygon once
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    
    import math
    def angle_from_centroid(p):
        return math.atan2(p.y - cy, p.x - cx)
    
    sorted_polygon = sorted(points, key=angle_from_centroid)
    
    # Get the four corners
    corners = [
        Point(rectangle.min_x, rectangle.min_y),
        Point(rectangle.min_x, rectangle.max_y),
        Point(rectangle.max_x, rectangle.min_y),
        Point(rectangle.max_x, rectangle.max_y)
    ]
    
    # Check all corners are inside or on boundary
    for corner in corners:
        if not IsPointInOrOnPolygon(corner, points, sorted_polygon):
            return False
    
    # Check every point along all four edges for accuracy
    
    # Top edge: from (min_x, max_y) to (max_x, max_y)
    for x in range(rectangle.min_x, rectangle.max_x + 1):
        if not IsPointInOrOnPolygon(Point(x, rectangle.max_y), points, sorted_polygon):
            return False
    
    # Bottom edge: from (min_x, min_y) to (max_x, min_y)
    for x in range(rectangle.min_x, rectangle.max_x + 1):
        if not IsPointInOrOnPolygon(Point(x, rectangle.min_y), points, sorted_polygon):
            return False
    
    # Left edge: from (min_x, min_y) to (min_x, max_y)
    for y in range(rectangle.min_y, rectangle.max_y + 1):
        if not IsPointInOrOnPolygon(Point(rectangle.min_x, y), points, sorted_polygon):
            return False
    
    # Right edge: from (max_x, min_y) to (max_x, max_y)
    for y in range(rectangle.min_y, rectangle.max_y + 1):
        if not IsPointInOrOnPolygon(Point(rectangle.max_x, y), points, sorted_polygon):
            return False
    
    return True
    

f = open(f"resources\day{day_no:02}.txt", "r")
points, max_point = GetPoints(f)
f.close()
print(f"Day {day_no}/1: {P1(points)}")
print(f"Day {day_no}/2: {P2(points, max_point)}")
