# Advent of Code 2025 - Day 2
def P1(ranges):
    validValues = []
    for r in ranges:
        validValues.extend(ValidValues(r))

    return sum(validValues)


def P2(ranges):
    return ""


def ExtractLimits(m):
    parts = m.split('-')
    return (int(parts[0]), int(parts[1])+1)


def ValidValues(r):
    validValues = []
    for i in range(r[0], r[1]):
        strValue = str(i)
        if (ValidValue(strValue)):
            validValues.append(i)
    return validValues


def ValidValue(strValue):
    if (len(strValue) % 2 != 0):
        return False
    h1 = strValue[:len(strValue)//2]
    h2 = strValue[len(strValue)//2:]
    if h1 == h2:
        return True
    return False


f = open("resources\day02.txt", "r")
allfile = f.read()
ranges = [ExtractLimits(m) for m in allfile.split(',')]

f.close()
print(f"Day 2/1: {P1(ranges)}")

print(f"Day 2/2: {P2(ranges)}")
f.close()
