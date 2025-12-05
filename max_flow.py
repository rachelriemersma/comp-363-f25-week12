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
    """
    finds the minimum capacity of a path aka bottleneck
    Args:
        residual: residual graph as adjacency matrix
        path: list of verticies that make the path 
    Returns: minimum capacity of the path 
    """
    min_capacity = float('inf')
    # check each pair of verticies in the path 
    for u, v in get_path_edges(path):
        capacity = residual[u][v]
        # if the edge has a smaller capacity, update the capacity 
        if capacity < min_capacity:
            min_capacity = capacity
    return min_capacity    

def update_residual(residual: list[list[int]], path: list[int], flow: int):
    """
    move flow along the graph and update the residual.
    Args: 
        residual: residual graph as adjacency matrix
        path: list of verticies that make the path
        flow: amt being pushed through the graph      
    """
    for u, v in get_path_edges(path):
        # update forward and backwards capacities 
        residual[u][v] -= flow
        residual[v][u] += flow

def get_path_edges(path: list[int]) -> list[tuple[int, int]]:
    """
    convert a path into a list of edges 
    Args:
        path: list of verticies that make the path
    Returns: list of edges represented by tuples for that path     
    """
    edges = []
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        # make current and "next" node a tuple
        edges.append((u, v))
    return edges           

def find_reachable(residual: list[list[int]], source: int) -> set[int]:
    """
    find all the verticies that are reachable from the source in the residual 
    Args: 
        residual: residual graph as adjacency matrix
        source: the starting vertex 
    returns: set of vertex indices that can be reached from source     
    """
    n = len(residual)
    # start w source 
    reachable = set([source])
    # verticies to explore 
    stack = [source]
    while len(stack) > 0:
        # vertex to explore 
        u = stack.pop()
        # check neighbors and if we can reach v from u 
        for v in range(n):
            if residual[u][v] > 0 and v not in reachable:
                # its reachable and we need to explore it 
                reachable.add(v)
                stack.append(v)
    return reachable

def find_min_cut(graph: list[list[int]], residual: list[list[int]], source: int) -> list[tuple[int,int]]:
    """
    find the edges in the original graph to "cut"
    args: 
        residual: residual graph as adjacency matrix
        graph: original graph as adjacency matrix 
        source: the starting vertex 
    returns: list of edge tuples (the minimum cut)    
    """
    n = len(graph)
    # find the reachable verticies from the source 
    reachable = find_reachable(residual, source)
    # the edges in the OG graph 
    min_cut = []
    for u in range(n):
        for v in range(n):
            # edge between u and v where u is reachable and v is not 
            if graph[u][v] > 0 and u in reachable and v not in reachable:
                min_cut.append((u, v))
    return min_cut       

def ford_fulk(graph: list[list[int]], source: int, target: int) -> tuple[int, list[tuple[int, int]]]:
    """
    full implementation of the ford-fulkerson algo, finds the max flow and min cut
    finds augmenting paths, pushing flow through the graph until there are no longer paths
    args:
        graph: original graph as adjacency matrix 
        source: the starting vertex 
        target: target/sink vertex 
    returns: the max flow value from source to target and the "cut" edges     
    """
    # create copy of OG graph so when altering residual the OG remains in tact 
    residual = copy.deepcopy(graph)
    max_flow = 0
    # find augmenting paths
    path = find_path(residual, source, target)
    while path is not None:
        # find the min capacity for that path and add to max flow
        min_capacity = find_min_capacity(residual, path)
        max_flow += min_capacity
        # update the residual graph using that minimum capacity 
        update_residual(residual, path, min_capacity)
        # look for another path 
        path = find_path(residual, source, target)
    # find the minimum cut     
    min_cut = find_min_cut(graph, residual, source)
    return max_flow, min_cut    

G = [  
    [0, 20, 0, 0, 0],  
    [0, 0, 5, 6, 0],   
    [0, 0, 0, 0, 7],  
    [0, 0, 0, 0, 8],   
    [0, 0, 0, 0, 0],  
]

max_flow, min_cut = ford_fulk(G, 0, 4)

print(f"Max Flow: {max_flow}")

print(f"Min Cut Edges: {min_cut}")

cut_capacity = sum(G[u][v] for u, v in min_cut)
print(f"{max_flow} = {cut_capacity}")

