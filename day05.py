# advent of code 2025 - day 5
day_no = 5

import copy

def P1(ranges, ingredients):
    freshIngredients = 0
    for i in ingredients:
        for r in ranges:
            if r[0] <= i <= r[1]:
                freshIngredients += 1
                break
    return freshIngredients

def P2(ranges, ingredients):
    ranges = MergeUntilStable(ranges)
    return CountRangesTotalSize(ranges)

def MergeUntilConvergence(ranges):
    i = 0
    while True:
        new_ranges = MergeRelatedToIndex(ranges, i)
        if len(new_ranges) == len(ranges) and i >= len(ranges) - 1:
            break
        i += 1
        ranges = new_ranges
    return ranges

def MergeUntilStable(ranges):
    while HasIntersaction(ranges):
        ranges = MergeUntilConvergence(ranges)
    return ranges

def MergeRelatedToIndex(ranges, i):
    if not ranges:
        return []
    if i >= len(ranges):
        return ranges
    preMerged = [ranges[j].copy() for j in range(i)]
    merged = ranges[i].copy()
    others = []
    for r in ranges[i+1:]:
        newRange, isMerged = MergeRanges(merged, r)
        if isMerged:
            merged = newRange
        else:
            others.append(r)
    return preMerged + [merged] + others

def CountRangesTotalSize(ranges):
    total = 0
    for r in ranges:
        total += r[1] - r[0] + 1
    return total    

def MergeRanges(r1, r2):
    if r1[0] <= r2[1] <= r1[1] or r2[0] <= r1[1] <= r2[1]:
        return [min(r1[0], r2[0]), max(r1[1], r2[1])], True
    return None, False

def HasIntersaction(ranges):
    for i in range(len(ranges)):
        for j in range(i+1, len(ranges)):
            if ranges[i][0] <= ranges[j][1] <= ranges[i][1] or ranges[j][0] <= ranges[i][1] <= ranges[j][1]:
                return True
    return False

def ParseIngredients(f):
    ranges = []
    ingredients = []
    secondSection = False
    for line in f:
        if line == "\n":
            secondSection = True
            continue
        if not secondSection:
            ranges.append([int(x) for x in line.strip().split('-')])
        else:
            ingredients.append(int(line.strip()))
    return ranges, ingredients

f = open(f"resources\day{day_no:02}.txt", "r")
ranges, ingredients = ParseIngredients(f)
print(f"Day {day_no}/1: {P1(ranges, ingredients)}")
print(f"Day {day_no}/2: {P2(ranges, ingredients)}")
f.close()