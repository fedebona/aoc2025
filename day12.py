# advent of code 2025 - Day 12
day_no = 12


class Map:
    def __init__(self, height, width, expectedShapes):
        self.expectedShapes = expectedShapes
        self.height = height
        self.width = width

    def __repr__(self):
        return f"Map({self.height}, {self.width}, {self.expectedShapes})"


def rotate_shape(shape):
    #90 degrees clockwise rotation
    if not shape or not shape[0]:
        return shape
    rows = len(shape)
    cols = len(shape[0])
    rotated = []
    for c in range(cols):
        new_row = ''
        for r in range(rows - 1, -1, -1):
            new_row += shape[r][c] if c < len(shape[r]) else '.'
        rotated.append(new_row)
    return rotated

def get_all_rotations(shape):
    # Generate all rotations of a shape
    rotations = []
    current = shape
    seen = set()
    
    for _ in range(4):
        normalized = tuple(current)
        if normalized not in seen:
            seen.add(normalized)
            rotations.append(current)
        current = rotate_shape(current)
    
    return rotations

def get_shape_cells(shape):
    # Get coordinates of solid cells (#) in a shape, normalized to (0,0)
    cells = []
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell == '#':
                cells.append((r, c))
    
    if not cells:
        return []
    
    # Normalize to start from (0, 0)
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return [(r - min_r, c - min_c) for r, c in cells]

def find_first_empty(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '.':
                return (r, c)
    return None

def can_place_at(grid, cells, start_row, start_col):
    # Check if shape cells can be placed at position
    for dr, dc in cells:
        r, c = start_row + dr, start_col + dc
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return False
        if grid[r][c] != '.':
            return False
    return True

def place_cells(grid, cells, start_row, start_col, mark):
    for dr, dc in cells:
        grid[start_row + dr][start_col + dc] = mark

def solve_map_backtrack(grid, shapes_to_place, all_shape_cells, attempts=[0]):
    attempts[0] += 1
    if attempts[0] > 100000:  # Safety limit
        return False
    
    # Check if all shapes have been placed
    if not shapes_to_place:
        return True
    
    # Get the first shape to place
    shape_id, count = shapes_to_place[0]
    remaining = shapes_to_place[1:] if count == 1 else [(shape_id, count - 1)] + shapes_to_place[1:]
    
    # Try all rotations of this shape
    for cells in all_shape_cells[shape_id]:
        # Try all positions in the grid
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if can_place_at(grid, cells, r, c):
                    # Place the shape
                    place_cells(grid, cells, r, c, str(shape_id))
                    
                    # Recursively solve
                    if solve_map_backtrack(grid, remaining, all_shape_cells, attempts):
                        return True
                    
                    # Backtrack
                    place_cells(grid, cells, r, c, '.')
    
    return False

def P1(shapes, maps):
    # Precompute normalized cells for all rotations of each shape
    all_shape_cells = {}
    for shape_id, shape in shapes.items():
        rotations = get_all_rotations(shape)
        all_shape_cells[shape_id] = [get_shape_cells(rot) for rot in rotations]
        # Remove empty or duplicate rotations
        all_shape_cells[shape_id] = [cells for cells in all_shape_cells[shape_id] if cells]
    
    solved_count = 0
    
    for idx, map_obj in enumerate(maps):           
        # Build list of shapes to place
        shapes_to_place = [
            (shape_id, count) 
            for shape_id, count in enumerate(map_obj.expectedShapes)
            if count > 0 and shape_id in all_shape_cells
        ]
        
        # Early check: does total shape area fit in map area?
        total_shape_area = sum(
            len(all_shape_cells[shape_id][0]) * count 
            for shape_id, count in shapes_to_place
        )
        map_area = map_obj.width * map_obj.height
        
        if total_shape_area > map_area:
            continue  # Can't possibly fit

        grid = [['.' for _ in range(map_obj.width)] for _ in range(map_obj.height)]
        
        # Try to solve this map
        attempts = [0]
        if solve_map_backtrack(grid, shapes_to_place, all_shape_cells, attempts):
            solved_count += 1
        #print(f"Map {idx}: {attempts[0]} attempts, {'SOLVED' if attempts[0] <= 100000 else 'TIMEOUT'}")
    
    return solved_count


def P2(shapes, maps):

    return


def ReadMap(f):
    shapes = {}
    maps = []
    shape = []
    shapeId = -1
    for line in f:
        if not line.strip():
            continue
        if ":" in line:
            a, b = line.strip().split(':')
            if b:
                w, h = a.split('x')
                maps.append(Map(int(h), int(w), [int(x)
                            for x in b.strip().split(' ')]))
            else:
                if shapeId > -1:
                    shapes[shapeId] = shape
                    shape = []
                shapeId = int(a)

        else:
            shape.append(line.strip())
        shapes[shapeId] = shape
    return shapes, maps


f = open(f"resources\day{day_no:02}.txt", "r")
shapes, maps = ReadMap(f)
f.close()
print(f"Day {day_no}/1: {P1(shapes, maps)}")
print(f"Day {day_no}/2: {P2(shapes, maps)}")
