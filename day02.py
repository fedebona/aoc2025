# Advent of Code 2025 - Day 2
def P1(ranges):
    validValues = []
    for r in ranges:
        validValues.extend(ValidValuesP1(r))

    return sum(validValues)


def P2(ranges):
    validValues = []
    for r in ranges:
        validValues.extend(ValidValuesP2(r))
    return sum(validValues)


def ExtractLimits(m):
    parts = m.split('-')
    return (int(parts[0]), int(parts[1])+1)


def ValidValuesP1(r):
    validValues = []
    for i in range(r[0], r[1]):
        strValue = str(i)
        if (ValidValueP1(strValue)):
            validValues.append(i)
    return validValues


def ValidValueP1(strValue):
    if (len(strValue) % 2 != 0):
        return False
    h1 = strValue[:len(strValue)//2]
    h2 = strValue[len(strValue)//2:]
    if h1 == h2:
        return True
    return False


def ValidValueP2(strValue):
    if ValidValueP1(strValue):
        return True
    for i in range(0, len(strValue)//2):
        if (len(strValue) % (i+1) != 0):
            continue
        h1 = strValue[:i+1]
        h2 = strValue[i+1:]
        if (Fit(h1, h2)):
            return True
    return False


def Fit(h1, h2):
    for i in range(0, len(h2), len(h1)):
        if h1 != h2[i:i+len(h1)]:
            return False
    return True


def ValidValuesP2(r):
    validValues = []
    for i in range(r[0], r[1]):
        strValue = str(i)
        if (ValidValueP2(strValue)):
            validValues.append(i)
    return validValues


f = open("resources\day02.txt", "r")
allfile = f.read()
ranges = [ExtractLimits(m) for m in allfile.split(',')]

f.close()
print(f"Day 2/1: {P1(ranges)}")

print(f"Day 2/2: {P2(ranges)}")
f.close()
