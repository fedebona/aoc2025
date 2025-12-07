# advent of code 2025 - day 7
day_no = 7

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
    beams = {StartingBeam(map)}
    hits = 0
    while Quote(beams) < len(map) - 1:
        beams, hits = MoveNext(beams, map, hits)
    return hits

def P2(map):
    return sum ([int(s) for s in map[len(map)-1] if s !='.'])

def ReadAllMap(f):
    map = []
    for line in f:
        map.append(list(line.strip()))
    return map

def StartingBeam(map):
    startingIndex = map[0].index("S")
    map[0][startingIndex] = 1
    return Point(startingIndex, 0)

def Quote(beams):
    return(list(beams)[0].y)

def MoveNext(beams, map, hits):
    new_beams = set()
    for beam in beams:
        nextvalue = map[beam.y + 1][beam.x]
        if nextvalue == '.':
            new_beams.add(Point(beam.x, beam.y + 1))
            map[beam.y + 1][beam.x] = map[beam.y][beam.x]        
        elif nextvalue == '^':
            hits += 1
            if beam.x > 0:
                new_beams.add(Point(beam.x - 1, beam.y + 1))
                if map[beam.y + 1][beam.x - 1] == '.':
                    map[beam.y + 1][beam.x - 1] = 0
                map[beam.y + 1][beam.x - 1]  += map[beam.y][beam.x]
            if beam.x < len(map[beam.y]) - 1:
                new_beams.add(Point(beam.x + 1, beam.y + 1))
                if map[beam.y + 1][beam.x + 1] == '.':
                    map[beam.y + 1][beam.x + 1] = 0
                map[beam.y + 1][beam.x + 1]  += map[beam.y][beam.x]
        else:
            map[beam.y + 1][beam.x] += map[beam.y][beam.x]
    return new_beams, hits

f = open(f"resources\day{day_no:02}.txt", "r")
map = ReadAllMap(f)
f.close()
print(f"Day {day_no}/1: {P1(map)}")
print(f"Day {day_no}/2: {P2(map)}")
