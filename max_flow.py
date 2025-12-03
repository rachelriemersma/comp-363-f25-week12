import copy 

def find_path(graph: list[list[int]], source: int, target: int):
    """Return a path -- any path -- from source to target in the graph"""

    # Initialize return item
    path: list[int] = None

    # Make sure inputs are ok
    if graph is not None:
        n: int = len(graph)
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            # Initialize DFS tools
            no_edge: int = graph[0][0]  # absence of edge
            marked: list[int] = [source]  # vertices already processed
            found: bool = False  # Flags detection of path

            # What vertex to explore next and what is the path
            # to it. The information is stored as a tuple in
            # the form:
            #  (vertex, path_to_this_vertex)
            # with path_to_this_vertex being a list of the
            # vertices alonγ the path.
            stack: list[(int, list[int])] = [(source, [source])]

            while len(stack) > 0 and not found:
                # Explore the next vertex from the stack
                (u, path_from_source_to_u) = stack.pop()
                found = (u == target)
                if found:
                    # u is the end of the path, so we got what we are 
                    # looking for
                    path = path_from_source_to_u
                else:
                    # Explore the neighbors of u, hopefully one of them
                    # will get us a stop closer to the target vertex.
                    v: int = n - 1
                    while v >= 0:
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1
    return path

def find_min_capacity(residual: list[list[int]], path: list[int]) -> int:
    min_capacity = 0
    # check each pair of verticies in the path 
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        capacity = residual[u][v]
        # if the edge has a smaller capacity, update the capacity 
        if capacity < min_capacity
        min_capacity = capacity
    return min_capacity    

def update_residual(residual: list[list[int]], path: list[int], flow: int):
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        # update forward and backwards capacities 
        residual[u][v] -= flow
        residual[v][u] += flow

def find_reachable(residual: list[list[int]], source: int) -> set[int]:
    n = len(residual)
    reachable = set()
    stack = [source]
    while len(stack) > 0:
        u = stack.pop()
        if u not in reachable:
            reachable.add(u)
            for v in range(n):
                if residual[u][v] > 0 and v not in reachable:
                    stack.append(v)
    return reachable                

# think abt later(redundant):
#
# for i in range(len(path)-1):
#        u = path[i]
#        v = path[i+1]
    
