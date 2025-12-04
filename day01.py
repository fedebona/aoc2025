# Advent of Code 2025 - Day 1
def P1(f):
    current = 50
    zeros = 0
    for line in f.readlines():
        if line[0] == 'R':
            increment = int(line[1:])
            current = Add(current, increment)
        elif line[0] == 'L':
            decrement = int(line[1:])
            current = Subtract(current, decrement)
        if current == 0:
            zeros += 1
    return zeros


def P2(f):
    current = 50
    zeros = 0
    for line in f.readlines():
        if line[0] == 'R':
            increment = int(line[1:])
            zeros += CountRoundsRight(current, increment)
            current = Add(current, increment)
        elif line[0] == 'L':
            increment = int(line[1:])
            zeros += CountRoundsLeft(current, increment)
            current = Subtract(current, increment)         
    return zeros


def Add(current, increment):
    return (current + increment) % 100

def Subtract(current, decrement):
    return (current - decrement + 100) % 100

def CountRoundsRight(current, increment):
    return (current + increment) // 100

def CountRoundsLeft(current, decrement):
    newCurrent = Subtract(current, decrement)
    loops = decrement // 100
    if current == 0:
        return loops
    return loops + (1 if newCurrent >= current else 0) + (1 if newCurrent == 0 else 0)

f = open("resources\day01.txt", "r")
print(f"Day 1/1: {P1(f)}")
f.close()
f = open("resources\day01.txt", "r")
print(f"Day 1/2: {P2(f)}")
f.close()
