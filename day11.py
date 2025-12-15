# advent of code 2025 - Day 11
day_no = 11

def P1(nodes):
    allPathsToExit = []
    Visit(nodes, 'you', 'out',[], allPathsToExit)
    return len(allPathsToExit)

def CountPathsThroughNodes(graph, start, end, must_visit, max_length=30):
    """
    Count paths from start to end that pass through all nodes in must_visit.
    Uses DP with memoization - only tracks current node and which required nodes visited.
    """
    from functools import lru_cache
    
    must_visit_set = frozenset(must_visit)
    
    # Create node to index mapping for bitmask
    all_nodes = set()
    for node in graph:
        all_nodes.add(node)
        all_nodes.update(graph[node])
    
    node_to_idx = {node: idx for idx, node in enumerate(sorted(all_nodes))}
    
    @lru_cache(maxsize=None)
    def dp(node, visited_mask, required_mask, depth):
        """
        Count paths from node to end.
        visited_mask: bitmask of all visited nodes (to prevent cycles)
        required_mask: bitmask of required nodes visited so far
        depth: current path length
        """
        if depth > max_length:
            return 0
        
        if node == end:
            # Check if all required nodes were visited
            target_mask = 0
            for req_node in must_visit_set:
                if req_node in node_to_idx:
                    target_mask |= (1 << node_to_idx[req_node])
            return 1 if required_mask == target_mask else 0
        
        if node not in graph:
            return 0
        
        total = 0
        node_idx = node_to_idx.get(node, -1)
        
        for neighbor in graph[node]:
            neighbor_idx = node_to_idx.get(neighbor, -1)
            if neighbor_idx == -1:
                continue
            
            # Check if already visited (cycle detection)
            if visited_mask & (1 << neighbor_idx):
                continue
            
            new_visited = visited_mask | (1 << neighbor_idx)
            new_required = required_mask
            
            # Update required mask if this neighbor is a required node
            if neighbor in must_visit_set:
                new_required |= (1 << neighbor_idx)
            
            total += dp(neighbor, new_visited, new_required, depth + 1)
        
        return total
    
    # Initialize
    start_idx = node_to_idx.get(start, -1)
    if start_idx == -1:
        return 0
    
    initial_visited = 1 << start_idx
    initial_required = 0
    if start in must_visit_set:
        initial_required = 1 << start_idx
    
    return dp(start, initial_visited, initial_required, 1)

def P2(nodes):
    # Single step: count all paths from svr to out that pass through both dac and fft
    # Try with increasing max_length if needed
    return CountPathsThroughNodes(nodes, 'svr', 'out', {'dac', 'fft'}, max_length=30)

def Visit(graph, start, end, visited, allPathsToExit):
    # Iterative approach using a stack
    # Stack contains tuples of (current_node, path_so_far)
    stack = [(start, [start])]
    
    while stack:
        current, path = stack.pop()
        
        # Found the end node
        if current == end:
            allPathsToExit.append(path)
            continue
        
        # Skip if node has no neighbors
        if current not in graph:
            continue
        
        # Explore all neighbors
        for next_node in graph[current]:
            if next_node not in path:  # Avoid cycles
                new_path = path + [next_node]
                stack.append((next_node, new_path))
    
    return len(allPathsToExit) > 0

def MapNodes(f):
    grid = {}
    for line in f:
        #grid.append(list(line.strip()))
        node = line.strip().split(': ')
        grid[node[0]] = node[1].split(' ')
    return grid

f = open(f"resources\day{day_no:02}.txt", "r")
nodes = MapNodes(f)
f.close()
print(f"Day {day_no}/1: {P1(nodes)}")
print(f"Day {day_no}/2: {P2(nodes)}")