# advent of code 2025 - day 10
import re
from collections import deque
day_no = 10


class machine:
    def __init__(self, lights, buttons, len_lights):
        self.lights = lights
        self.buttons = buttons
        self.len_lights = len_lights

    def __repr__(self):
        buttons_bin = [f"{b:0{self.len_lights}b}" for b in self.buttons]
        return f"machine(lights={self.lights:0{self.len_lights}b}, buttons={buttons_bin})"


def P1(machines):
    totalValidButtons = []
    rows = 0    
    for machine in machines:
        totalValidButtons.append(ValidateLights(machine))
        rows += 1
    return sum(totalValidButtons)


def ValidateLights(machine):
    # State: (current_lights, tuple of pressed buttons)
    queue = deque([(machine.lights, ())])
    visited = {(machine.lights, ())}
    solutions = []
    
    while queue:
        current_lights, pressed_tuple = queue.popleft()
        
        if current_lights == 0:
            solutions.append(len(pressed_tuple))
            continue
        
        # Early termination if we already have a solution and current path is too long
        if solutions and len(pressed_tuple) >= min(solutions):
            continue
        
        pressed_buttons = set(pressed_tuple)
        
        for buttonIndex in range(len(machine.buttons)):
            if buttonIndex not in pressed_buttons:
                new_lights = current_lights ^ machine.buttons[buttonIndex]
                new_pressed = pressed_tuple + (buttonIndex,)
                state = (new_lights, new_pressed)
                
                if state not in visited:
                    visited.add(state)
                    queue.append(state)
    
    return min(solutions) if solutions else 0


def P2(machines):

    return

def minSolutions(solutions):
    if not solutions:
        return 0
    return min([len(sol) for sol in solutions])

def ReadMap(f):
    regex = r"\[(.*)\](.*)\{(.*)\}"
    machines = []

    matches = re.finditer(regex, f, re.MULTILINE)
    for match in matches:
        buttons = []
        # lights = [(m=='#') for m in match.group(1)]
        strmatch = match.group(1).strip()
        len_lights = len(strmatch)
        lights = int(strmatch.replace('#', '1').replace('.', '0'), 2)
        buttonsList = match.group(2)
        regexButtons = r"\((.*?)\)"
        matches2 = re.finditer(regexButtons, buttonsList, re.MULTILINE)
        for match2 in matches2:
            # button = [False] * len(lights)
            # for pos in match2.group(1).split(','):
            #     buttonPos = int(pos)
            #     button[buttonPos] = True
            button = 0
            for pos in match2.group(1).split(','):
                button += (1 << (len_lights - int(pos) - 1))
            buttons.append(button)
        machines.append(machine(lights, buttons, len_lights))
    return machines


with open(f"resources\day{day_no:02}.txt", "r", encoding="utf-8") as fh:
    text = fh.read()
machines = ReadMap(text)
print(f"Day {day_no}/1: {P1(machines)}")

print(f"Day {day_no}/2: {P2(machines)}")
