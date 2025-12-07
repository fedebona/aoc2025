# advent of code 2025 - day 6
from functools import reduce


day_no = 6

def P1(grid):
    operations = grid [-1]
    results = []
    for col in range(len(operations)):
        op = operations[col]
        # process operation 
        if op == "*":
            result = 1
            for row in range(len(grid)-1):
                result *= int(grid[row][col])
        elif op == "+":
            result = 0
            for row in range(len(grid)-1):
                result += int(grid[row][col])
        results.append(result)
    return sum(results)

def P2(map):
    operands = []
    results = []
    for x in range(len(map[0])):
        operand = ""
        for y in range(len(map)-1):
            operand += map[y][x]
        operands.append(operand.strip())
    operations = [s for s in map[len(map)-1] if s != " "]
    operation_id = 0
    curr_list = []
    for number_index in range(len(operands)):
        number = operands[number_index]
        if number == "" or number_index == len(operands)-1:
            if number_index == len(operands)-1:
                curr_list.append(int(number))
            op = operations[operation_id]
            if op == "+":
                results.append(sum(curr_list))
            elif op == "*":
                results.append(reduce(multiply, curr_list))
            operation_id += 1            
            curr_list = []
            continue
        curr_list.append(int(number))
    return sum(results)

def multiply(x, y):
    return x * y

def ExtractMap(f):
    grid = []
    for line in f:
        grid.append([s for s in line.strip().split(" ") if s != ""])
    return grid

def ReadAllMap(f):
    map = []
    for line in f:
        map.append(list(line.strip('\n')))
    return map

f = open(f"resources\day{day_no:02}.txt", "r")
grid = ExtractMap(f)
f.close()
f = open(f"resources\day{day_no:02}.txt", "r")
map = ReadAllMap(f)
f.close()
print(f"Day {day_no}/1: {P1(grid)}")
print(f"Day {day_no}/2: {P2(map)}")
