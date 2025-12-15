# advent of code 2025 - day 10
import re
from collections import deque
import pulp
day_no = 10


class machine:
    def __init__(self, lights, buttons, len_lights, joltage):
        self.lights = lights
        self.buttons = buttons
        self.len_lights = len_lights
        self.joltage = joltage
    def __repr__(self):
        buttons_bin = [f"{b:0{self.len_lights}b}" for b in self.buttons]
        return f"machine(lights={self.lights:0{self.len_lights}b}, buttons={buttons_bin}, joltage={self.joltage}  )"


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
    total_min_presses = 0
    
    for machine in machines:
        min_presses = solve_joltage_puzzle(machine)
        total_min_presses += min_presses
    
    return total_min_presses


def solve_joltage_puzzle(machine):
    """
    Use Integer Linear Programming to find minimum button presses.
    Each button increments specific elements by 1.
    Find minimum total presses to reach exact target joltages.
    """
    num_elements = machine.len_lights
    num_buttons = len(machine.buttons)
    target = machine.joltage
    
    # Create the LP problem
    prob = pulp.LpProblem("MinButtonPresses", pulp.LpMinimize)
    
    # Decision variables: number of times each button is pressed (non-negative integers)
    button_presses = [pulp.LpVariable(f"button_{i}", lowBound=0, cat='Integer') 
                      for i in range(num_buttons)]
    
    # Objective: minimize total button presses
    prob += pulp.lpSum(button_presses)
    
    # Constraints: for each element, sum of increments must equal target
    for element_idx in range(num_elements):
        bit_position = num_elements - element_idx - 1
        # Sum of button presses that affect this element
        element_sum = pulp.lpSum([
            button_presses[btn_idx] 
            for btn_idx in range(num_buttons) 
            if machine.buttons[btn_idx] & (1 << bit_position)
        ])
        prob += element_sum == target[element_idx], f"Element_{element_idx}"
    
    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if prob.status == pulp.LpStatusOptimal:
        return int(pulp.value(prob.objective))
    else:
        return 0

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
            button = 0
            for pos in match2.group(1).split(','):
                button += (1 << (len_lights - int(pos) - 1))
            buttons.append(button)
        joltage = [int(x) for x in match.group(3).split(',') if x.strip().isdigit()]  
        machines.append(machine(lights, buttons, len_lights, joltage))
    return machines


with open(f"resources\\day{day_no:02}.txt", "r", encoding="utf-8") as fh:
    text = fh.read()
machines = ReadMap(text)
print(f"Day {day_no}/1: {P1(machines)}")

print(f"Day {day_no}/2: {P2(machines)}")
