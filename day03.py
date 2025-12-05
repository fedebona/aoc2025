# Advent of Code 2025 - Day 3
def CalculateJoltage(line, size=12):
    line = line.strip()
    joltage = ""
    while size > 0 and line:
        currJoltage = max(line[:len(line)-size + 1])
        line = line[line.index(currJoltage) + 1:]
        size -= 1
        joltage += currJoltage
    return int(joltage) if joltage else 0

def P1(f):
    joltages = []
    for line in f.readlines():
        joltages.append(CalculateJoltage(line, size=2))
    return sum(joltages)


def P2(f):
    joltages = []
    for line in f.readlines():
        joltages.append(CalculateJoltage(line, size=12))
    return sum(joltages)


f = open("resources\day03.txt", "r")
print(f"Day 3/1: {P1(f)}")
f.close()
f = open("resources\day03.txt", "r")
print(f"Day 3/2: {P2(f)}")
f.close()
